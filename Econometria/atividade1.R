#Todos itens acima e mais
library(fpp3)
#Plot
library(ggplot2)
#Estatistica descritiva
library(dplyr)
library(psych)
#Estacionariedade
library(urca)
#Teste de modelos
library(forecast)

#Excel
library(writexl)

rm(list = ls(all = TRUE))
options(scipen = 99999)


glimpse(aus_retail)
#Transformacoes
food <- aus_retail %>%
    filter(Industry == "Food retailing") %>%
    summarise(Turnover = sum(Turnover))
food$Year <- format(food$Month, "%Y")

food <- food %>%
    filter(Year >= 2000)
    
ggplot(data=food, aes(x=Year, y=Turnover, group=1)) +
  geom_line()+
  geom_point() +
  labs(x = "Between Years")
#Como pode ser notado a tendencia do grafico eh crescente, com sazonalidade variante indicando uma heteroscesdacidade
#Os picos do grafico crescem a medida do tempo indicando um crescimento nao linear.

#Obtendo dados descritivos para o Turnover da industria Food retailing
describe(food$Turnover)

#FAC
food %>%
    ACF(Turnover, lag_max = 50) %>%
    autoplot() +
    theme_bw()
#Atraves do decaimento da FAC eh possivel perceber que eh lento, indicando assim uma tendencia
#Tambem eh notavel uma certa variacao nos intervalos de picos indicando uma sazonalidade nao muito expressiva
#Pois a altura dos picos variam pouco, mas variam.

#FACP
food %>%
    PACF(Turnover, lag_max = 50) %>%
    autoplot()

#TESTES DE ESTACIONARIEDADE
#ADF

teste_adf = ur.df(food$Turnover, type = "trend", lags = 6, selectlags = "AIC")
teste_adf
#Note que o valor esta acima de z-value 0.119 entao indica que talvez nao seja estacionaria
#Sugere a nao rejeicao da hipotese nula
t_diferencia = diff(food$Turnover)
teste_adf = ur.df(t_diferencia)
teste_adf
#Com uma diferenciacao ainda nao foi possivel transformar em estacionaria
#Ainda rejeita-se a hipotese nula de estacionariedade

#KPSS
teste_kpss = ur.kpss(food$Turnover, type = "tau", lags = "short")
teste_kpss
#Note que o valor esta acima de z-value 0.05 entao indica que talvez nao seja estacionaria
#Sugere a nao rejeicao da hipotese nula
t_diferencia = diff(food$Turnover)
teste_kpss = ur.kpss(t_diferencia)
teste_kpss
#Com uma diferenciacao ainda nao foi possivel transformar em estacionaria
#Ainda sugere a nao rejeitacao da hipotese nula de estacionariedade

#PP
teste_pp = ur.pp(food$Turnover, type="Z-tau", lags="short")
teste_pp
#O resultado do teste sugere nao rejeitar a hipotese nula de nao estacionariedade
t_diferencia = diff(food$Turnover)
teste_pp = ur.pp(t_diferencia)
teste_pp
#Apos a diferenciacao, o teste sugere rejeitar a hipotese de nao estacionariedade

#Modelos MA(1), MA(2). MA(3) ARIMA
ma1 = arima(food$Turnover, order=c(0,0,1))
ma1

ma2 = arima(food$Turnover, order=c(0,0,2))
ma2

ma3 = arima(food$Turnover, order=c(0,0,3))
ma3

#Funcoes de previsao
fma1 = predict(ma1,4)
fma2 = predict(ma2,4)
fma3 = predict(ma3,4)

#Grafico previsao
fma1 = Arima(food$Turnover, order = c(0,1,1),
                include.drift = T)
prev1 = forecast(fma1, h = 4)
autoplot(prev1)

fma2 = Arima(food$Turnover, order = c(0,0,2),
                include.drift = T)
prev1 = forecast(fma2, h = 4)
autoplot(prev1)

fma3 = Arima(food$Turnover, order = c(0,0,3),
                include.drift = T)
prev1 = forecast(fma3, h = 4)
autoplot(prev1)
#Escolhendo o melhor modelo e imprimindo variaveis de correlacao que eh o fma1
#Plota o remainder
fit_ARIMA <- auto.arima(food$Turnover, seasonal = TRUE)
summary(fit_ARIMA)
checkresiduals(fit_ARIMA)
#Forecast
fcast <- forecast(fit_ARIMA, h = 1)
plot(fcast)
summary(fcast)

#Eh possivel perceber que o melhor modelo eh o ma2 visto que tem os menores valores de erro
