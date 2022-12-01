#Manipulacao de dados
library(tidyverse)
#Manipulacao de series temporais
library(tsibble)
#Funcoes de previsao
library(fable)
#Graficos e estatistitcas de series temporais
library(feasts)
#Series temporais tidy
library(tsibbledata)
#Todos itens acima e mais
library(fpp3)
#Plot
library(ggplot2)

#um tibble permite o armazenamento e manipulacao
#Ele contem? um index (info de tempo), variaveis medidas
#lendo um arquivo csv e convertendo para tsibble
url_data <- "https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv"
covid <- readr::read_csv(url_data)
covid

covid = readr::read_csv("https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv") %>%
  select(date, state, newDeaths, newCases )%>% #Seleciona apenas essas colunas
  as_tsibble( #converte em serie temporal
    index = date, #index referencia o tempo
    key = state #separa atraves de estados
  ) %>%
  group_by(state) %>% #Agrupa por estado
  mutate(MM_mortes = zoo::rollmean(newDeaths, k = 7, fill = NA, align = "right"),
  MM_casos = zoo::rollmean(newCases, k = 7, fill = NA, align = "right"))
#Visualizacao de dados

#Plota cada em caixas separadas cada media movel de cada estado
#covid %>%
#   filter(state != "TOTAL") %>% #Filtra o dataset covid para apenas os dados de states
#    autoplot(MM_mortes) + #plota as mortes
#    facet_wrap(~state, scales = "free") + #facet_wrap coloca  a variavel state com o operador ~ como default em cada caixinha e escala cada caixinha da melhor forma possivel
#    labs(x = "Dia", y = "Mortes", title = "Media Movel (7 dias)") #Muda as labels do plot

#Plota com interferencia da sazonalidade

covid %>%
    filter(state == "TOTAL") %>%
    gg_season(MM_mortes, period ="year") + #Plota com referencia a sazonalidade ou seja verificando o periodo(month) de cada grafico
    labs(x="Dia", y="Mortes (M_Movel)[7 dias]")

#componentes de uma Serie Temporal
# Tendencia: quando ha um aumento ou diminuicao, ou sjea, a tendencia do grafico eh crescer ou diminuir ou eh estacionaria
#  Sazonalidade: Quando uma serie eh influenciada por diferentes periodos de tempo, por ex, o mes de janeiro se comporta igual em todos os anos?
# Ciclo: Quando a serie apresenta padroes ciclicos isto eh que se repetem, por ex, as manchas solares repetem um padrao em periodos variaveis

#Sazonalidade vs Ciclo: O momento de picos eh mais facil de prever na sazonalidade do que no ciclo

#ST
#Verificar se tem sazonalidade e tendencia no plot
covid %>%
    filter(state == "TOTAL") %>%
    autoplot(newCases) +
    labs(x = "Dia", y = "Casos", title = "Numero de casos por dia no Brasil")
#Para o caso acima ha sazonalidade a cada semana e tem tendencia, por causa da subnotificacao

# Funcao de autocorrelacao (ou ACF): correlacao
# Verifica o quanto o tempo esta relacionado com a quantidade de dados, para esse caso especifico

covid %>%
    filter(state == "TOTAL") %>%
    ACF(newCases, lag_max = 100) #ACF autocorrelation function; lag se refere a pouquissimo tempos de diferenca
#analisando essa saida sabemos o quanto cada saida esta relacionada com a quantidade de dias anteriores
#por exemplo, a cada 7 dias ha uma forte correlacao entre os dias anteriores

covid %>%
    filter(state == "TOTAL") %>%
    ACF(newCases, lag_max = 50) %>% #ACF autocorrelation function; lag se refere a pouquissimo tempos de diferenca
    autoplot()

#Analisa o comportamento do grafico, percebemos que o decaimento das linhas eh bem lento, ou seja, isso indica que eh uma serie com tendencia
#Analisando os grandes picos do grafico, percebemos que a cada 7 dias ha um pico, ou seja, sazonalidade na semana

