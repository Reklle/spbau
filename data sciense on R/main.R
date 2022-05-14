# import exel
library(readxl)
data <- read_excel("C:/.xlsx")


# statistic library
library(stats)


# settings
pConf = 0.95             # Confidence probability


# define useful functions
u_a <- function(x) {sd(x, na.rm=TRUE)/sqrt(length(x))}
mean2 <- function(x) {sqrt(mean(x**2))}
powmean <- function(x, p) {mean(x**p)**(1/p)}
t <- function(x) {qt((1+pConf)/2,length(x)-1)} # Student coefficient
quickinfo <- function(x) {
  ret <- paste("Mean value:", mean(x), "±", t(x)*u_a(x))
  print(ret)}

    
#########################
#         Note          #
#########################
#  data$name --  extract "name" from data frame
#  mean(x)   --  mean value
#  u_a(x)    --  uncertainty of direct measurement
#  u(y)      --  uncertainty of indirect measurement


data <- read_excel("C:/.xlsx")
