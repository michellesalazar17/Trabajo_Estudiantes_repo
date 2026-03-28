library(tidyverse)
library(dplyr)
library(readr)

estudiantes <- read_csv("C:/Users/Maikelvins/Downloads/4. Estudiantes.csv")

#Estructura
str(estudiantes)
glimpse(estudiantes)
class(estudiantes)

#Renombrar colummnas

estudiantes <- estudiantes %>% 
  rename(pais = Country,
         nivel_academico = Academic_Level,
         promedio_uso_diario = Avg_Daily_Usage_Hours,
         red_social = Most_Used_Platform,
         rendimiento_acm = Affects_Academic_Performance,
         horas_sueño = Sleep_Hours_Per_Night,
         salud_mental = Mental_Health_Score,
         adiccion = Addicted_Score)

estudiantes <- estudiantes %>% 
  select(pais,
         nivel_academico,
         promedio_uso_diario,
         red_social,
         rendimiento_acm,
         horas_sueño,
         salud_mental,
         adiccion )

#Diagnostico de valores nulos
summary(estudiantes)
colSums(is.na(estudiantes))

#conversion de datos 

estudiantes <- estudiantes %>% 
  mutate(nivel_academico = as.factor(nivel_academico),
         salud_mental = as.integer(round(salud_mental)),
         adiccion = as.integer(round(adiccion)))

