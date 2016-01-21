library(sensitivity)

epsilon = 0.001

custom_model<-function(Input){
  #browser()
  Y <- NULL
  
  for (i in 1:NROW(Input[,1])){
    record_v<-Input[,1][i]
    #print(record_v)
    record_re<-Input[,2][i]
    #print(record_re)
    record_rep_s<-Input[,3][i]
    #print(record_rep_s)
    record_rep_ra<-Input[,4][i]
    #print(record_rep_ra)
    record_att_s<-Input[,5][i]
    #print(record_att_s)
    record_att_ra<-Input[,6][i]
    #print(record_att_ra)
  
    cohesion.sub1<-subset(cohesion, abs(v- record_v)<=epsilon &  abs(re- record_re) <=epsilon & 
                          abs(rep_s- record_rep_s) <=epsilon & abs(rep_ra - record_rep_ra)<=epsilon &
                          abs(att_s- record_att_s) <=epsilon & abs(att_ra - record_att_ra)<=epsilon)
    Y<-c(Y, cohesion.sub1[1,7])
  }
  
  output <- matrix(unlist(Y), ncol = 1, byrow = TRUE)
  return(output)
}

X11<-read.csv(file="C:\\CrowdModelling\\analysis\\X1.csv",head=TRUE,sep=",")
X22<-read.csv(file="C:\\CrowdModelling\\analysis\\X2.csv",head=TRUE,sep=",")
cohesion<- read.csv(file = "C:\\CrowdModelling\\analysis\\group_cohesion_output.csv",head=TRUE,sep=",")
sa <- sobol2002(model = custom_model, X1 = X11, X2 = X22) 
print(sa)

