library(sensitivity)

n_sample = 1000
random_sample<-function(){
  
  ve<-runif(n_sample,1.2,1.6)
  re<-runif(n_sample,0.3,0.7)
  rep_s<-runif(n_sample,2.5,3.0)
  rep_ra<-runif(n_sample,0.3,0.5)
  att_s<-runif(n_sample,0.5,1.0)
  att_ra<-runif(n_sample,0.6,0.8)
  return (c(ve,re,rep_s,rep_ra,att_s,att_ra))
}

a<-random_sample()
X1 <- data.frame(matrix(data=a, nrow = n_sample))

b<-random_sample()
X2 <- data.frame(matrix(data=b, nrow = n_sample))

write.csv(X1, file = "C:\\CrowdModelling\\analysis\\analysis_rk_new_with_desired_force\\X1_new.csv",row.names=FALSE,quote = FALSE)
write.csv(X2, file = "C:\\CrowdModelling\\analysis\\analysis_rk_new_with_desired_force\\X2_new.csv",row.names=FALSE,quote = FALSE)
sa <- sobol2002(model = NULL, X1 = X1, X2 = X2) 
write.csv(sa$X, file = "C:\\CrowdModelling\\analysis\\analysis_rk_new_with_desired_force\\data.csv",row.names=FALSE,quote = FALSE)