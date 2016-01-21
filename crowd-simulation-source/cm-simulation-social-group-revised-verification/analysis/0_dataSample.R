library(sensitivity)

n_sample = 500
random_sample<-function(){

  rep_s<-runif(n_sample,1,4)
  rep_ra<-runif(n_sample,0.2,2.0)
  att_s<-runif(n_sample,1,4)
  att_ra<-runif(n_sample,0.2,2.0)
  return (c(rep_s,rep_ra,att_s,att_ra))
}

a<-random_sample()
X1 <- data.frame(matrix(data=a, nrow = n_sample))

b<-random_sample()
X2 <- data.frame(matrix(data=b, nrow = n_sample))

write.csv(X1, file = "C:\\CrowdModelling\\crowd-simulation-source\\cm-simulation-social-group-revised-verification\\analysis\\X1_new.csv",row.names=FALSE,quote = FALSE)
write.csv(X2, file = "C:\\CrowdModelling\\crowd-simulation-source\\cm-simulation-social-group-revised-verification\\analysis\\X2_new.csv",row.names=FALSE,quote = FALSE)
sa <- sobol2002(model = NULL, X1 = X1, X2 = X2) 
write.csv(sa$X, file = "C:\\CrowdModelling\\crowd-simulation-source\\cm-simulation-social-group-revised-verification\\analysis\\data.csv",row.names=FALSE,quote = FALSE)