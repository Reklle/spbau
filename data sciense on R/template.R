# import exel
library(readxl)
data <- read_excel("C:/.xlsx")


# statistic library
library(stats)


# define useful functions
u_a <- function(x) {sd(x, na.rm=TRUE)/sqrt(length(x))}
mean2 <- function(x) {sqrt(mean(x**2))}
powmean <- function(x, p) {mean(x**p)**(1/p)}

# settings
pConf = 0.95             # Confidence probability
t = qt((1+pConf)/2,5)    # Student coeffitiend


#########################
#         Note          #
#########################
#  data$name --  extract "name" from data frame
#  mean(x)   --  mean value
#  u_a(x)    --  uncertainty of direct measurement
#  u(y)      --  uncertainty of indirect measurement

data <- read_excel("C:/.xlsx")

mC <- mean(data$Ci, na.rm=TRUE)
dC <- SE(data$Ci)


