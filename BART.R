library(survival)
library(nnet)
library(nlme)
library(BART)
data = read.csv("combinedData.csv", header = T)
num_total = length(data$X)
num_train = 3800
num_test = num_total - num_train
feature1 = data$DGS10_DIFF1
feature2 = data$VIX_DIFF1
feature3 = data$SLOPE
feature4 = data$SKEW_DIFF1
feature5 = data$SP500_R
feature6 = data$SWAPSPREAD_DIFF1
real_train_val = data$SPREAD[2:c(num_train+1)]
real_test_val = data$SPREAD[c(num_train + 2):num_total]
set.seed(20190225)
x_train = data.frame(
  DGS10_DIFF1 = feature1[1:num_train],
  VIX_DIFF1 = feature2[1:num_train],
  SLOPE = feature3[1:num_train],
  SKEW_DIFF1 = feature4[1:num_train],
  SP500_R = feature5[1:num_train],
  SWAPSPREAD_DIFF1 = feature6[1:num_train]
)
x_test = data.frame(
  DGS10_DIFF1 = feature1[c(num_train + 1): c(num_total - 1)],
  VIX_DIFF1 = feature2[c(num_train + 1): c(num_total - 1)],
  SLOPE = feature3[c(num_train + 1): c(num_total - 1)],
  SKEW_DIFF1 = feature4[c(num_train + 1): c(num_total - 1)],
  SP500_R = feature5[c(num_train + 1): c(num_total - 1)],
  SWAPSPREAD_DIFF1 = feature6[c(num_train + 1): c(num_total - 1)]
)

yfit = wbart(
  x_train, real_train_val, x_test,
  nskip=100,ndpost=1000
)

x_axis = data$X[c(num_train + 1): c(num_total - 1)]

plot(x_axis,real_test_val,
     cex=.3,cex.axis=.8,cex.lab=.7, mgp=c(1.3,.3,0),tcl=-.2,pch=".")
lines(x_axis,apply(yfit$yhat.test,2,mean),col="red",lwd=1.5,lty=2) #post mean of $f(x_j)$

#qm = apply(yfit$yhat.test,2,quantile,probs=c(.025,.975)) # post quantiles
#lines(x_axis,qm[1,],col="grey",lty=1,lwd=1.0)
#lines(x_axis,qm[2,],col="grey",lty=1,lwd=1.0)
legend("bottomright",legend="prediction of test data",
       col="red", lwd=2, lty=1, bty="n",cex=.8,seg.len=3)


MSE = mean((yfit$yhat.test.mean - real_test_val)^2)
pred_train = apply(yfit$yhat.train,2,mean)
pred_test = apply(yfit$yhat.test,2,mean)
#yfit$prob.test.mean = apply(yfit$prob.test, 2, mean)
#test_pre = as.double(yfit$prob.test.mean>0.5)
#real_test_val - test_pre
#train_pre = as.double(yfit$prob.train.mean > 0.5)
#sum(abs(real_train_val-train_pre))
write.csv(pred_train, file="PRED_TRAIN_BART.csv")
write.csv(pred_test, file="PRED_TEST_BART.csv")
