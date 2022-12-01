#Manipulacao de dados
library(tidyverse)
#Manipulacao de series temporais
library(tsibble)
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
library(readxl)
rm(list = ls(all = TRUE))
options(scipen = 99999)
url_archive = "C:\\Users\\Beats\\Desktop\\Estudos\\Econometria\\Atividades\\dados-ac2.csv"

data_pib <- read_csv(url_archive)
glimpse(data_pib)
data_pib[data_pib$X15 == "X15", c("Total")]
data_cambio <- read_csv(url_archive, sheet=2)
plot(data_cambio$Periodo, data_cambio$Valor, type = "l", lty = 1)
lines(data_cambio$Periodo, data_cambio$Valor, type = "l", lty = 1)
#Eh possivel perceber uma tendencia estacionaria