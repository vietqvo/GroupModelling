library(sensitivity)

n_sample = 2000
random_sample<-function(){
  
  ve<-runif(n_sample,1,3)
  re<-runif(n_sample,0.2,2.0)
  rep_s<-runif(n_sample,1,4)
  rep_ra<-runif(n_sample,0.2,2.0)
  att_s<-runif(n_sample,1,4)
  att_ra<-runif(n_sample,0.2,2.0)
  return (c(ve,re,rep_s,rep_ra,att_s,att_ra))
}

a<-random_sample()
X1 <- data.frame(matrix(data=a, nrow = n_sample))

b<-random_sample()
X2 <- data.frame(matrix(data=b, nrow = n_sample))

write.csv(X1, file = "C:\\CrowdModelling\\analysis\\X1_new.csv",row.names=FALSE,quote = FALSE)
write.csv(X2, file = "C:\\CrowdModelling\\analysis\\X2_new.csv",row.names=FALSE,quote = FALSE)
sa <- sobol2002(model = NULL, X1 = X1, X2 = X2) 
write.csv(sa$X, file = "C:\\CrowdModelling\\analysis\\data.csv",row.names=FALSE,quote = FALSE)