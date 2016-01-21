library(sensitivity)

cohesion <- read.csv(file="C:\\CrowdModelling\\analysis\\MCC_Data_iso_final\\group_cohesion_output_sobol.csv",head=TRUE,sep=",")

epsilon = 0.1
ishigami <- function(xx, a=7, b=0.1)
{
  ##########################################################################
  #
  # INPUTS:
  #
  # xx = c(x1, x2, x3)
  # a = coefficient (optional), with default value 7
  # b = coefficient (optional), with default value 0.1  
  #
  ##########################################################################
  
  x1 <- xx[1]
  x2 <- xx[2]
  x3 <- xx[3]

  term1 <- sin(x1)
  term2 <- a * (sin(x2))^2
  term3 <- b * x3^4 * sin(x1)
  
  y <- term1 + term2 + term3
  return(y)
}

specify_decimal <- function(x, k) {
  return (round(x, k))
}

custom_model<-function(Input){
  #browser()
  Y <- NULL

  for (i in 1:NROW(Input[,1])){
    record_v<-Input[,1][i]
    record_re<-Input[,2][i]
    record_s<-Input[,3][i]
    record_ra<-Input[,4][i]
    
    #arround input function
    record_v<-specify_decimal(record_v,1)
    record_re<-specify_decimal(record_re,1)
    record_s<-specify_decimal(record_s,1)
    record_ra<-specify_decimal(record_ra,1)
    
    #t<- record_v + record_re + record_s + record_ra
    #Y<-c(Y, t)
    #cohesion.sub1<-subset(cohesion, v == record_v &  re == record_re & s == record_s & ra == record_ra )
    cohesion.sub1<-subset(cohesion, abs(v- record_v)<=epsilon &  abs(re- record_re) <=epsilon  & abs(s- record_s) <=epsilon & abs(ra - record_ra)<=epsilon)
    Y<-c(Y, cohesion.sub1[1,5])

  }
  
  output <- matrix(unlist(Y), ncol = 1, byrow = TRUE)
  return(output)
  
  #list(out=input[1]+ 2*input[2]+ 3*input[3]+ 4*input[4]); 
}


#X1 <- data.frame(matrix(runif(3 * n, -pi, pi), nrow = n))
#X2 <- data.frame(matrix(runif(3 * n, -pi, pi), nrow = n))
#x <- sobol(model = ishigami, X1 = X1, X2 = X2, order = 2, nboot = 100)
#print(x)


#n <- 1000
#X1 <- data.frame(matrix(runif(8 * n), nrow = n)) #Random uniform samples
#X2 <- data.frame(matrix(runif(8 * n), nrow = n))
# sensitivity analysis
#x <- sobol(model = sobol.fun, X1 = X1, X2 = X2, order = 2, nboot = 100)
#print(x)

n <- 2900 #sobol sequence will generate , sobol2002 will measure (p+2)*n samples
parameter_num = 4 
X1 <- data.frame(matrix(runif(parameter_num * n), nrow = n))
X2 <- data.frame(matrix(runif(parameter_num * n), nrow = n)) 
sa <- sobol2002(model = custom_model, X1 = X1, X2 = X2) 
#print(sa$y)
print(sa)


