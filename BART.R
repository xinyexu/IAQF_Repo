library(survival)
library(nnet)
library(nlme)
library(BART)
data = read.csv("combinedData.csv", header = T)
num_total = length(data$X)
num_train = 3700
num_test = num_total - num_train
feature1 = data$DGS10_DIFF1
feature2 = data$VIX_DIFF1
feature3 = data$SLOPE
feature4 = data$SKEW_DIFF1
feature5 = data$SP500_R
feature6 = data$SWAPSPREAD_DIFF1
real_train_val = data$SPREAD[4:c(num_train+3)]
real_test_val = data$SPREAD[c(num_train + 4):num_total]
real_val = data$SPREAD[4:num_total]
set.seed(20190225)
x_train = data.frame(
  DGS10_DIFF1 = feature1[3:c(num_train + 2)],
  VIX_DIFF1 = feature2[3:c(num_train + 2)],
  SLOPE = feature3[3:c(num_train + 2)],
  SKEW_DIFF1 = feature4[3:c(num_train + 2)],
  SP500_R = feature5[3:c(num_train + 2)],
  SWAPSPREAD_DIFF1 = feature6[3:c(num_train + 2)],
  SPREAD = data$SPREAD[3:c(num_train + 2)],
  SPREAD_1DAY_BEFORE = data$SPREAD[2:c(num_train + 1)],
  SPREAD_2DAY_BEFORE = data$SPREAD[1:num_train]
)
x_test = data.frame(
  DGS10_DIFF1 = feature1[c(num_train + 3): c(num_total - 1)],
  VIX_DIFF1 = feature2[c(num_train + 3): c(num_total - 1)],
  SLOPE = feature3[c(num_train + 3): c(num_total - 1)],
  SKEW_DIFF1 = feature4[c(num_train + 3): c(num_total - 1)],
  SP500_R = feature5[c(num_train + 3): c(num_total - 1)],
  SWAPSPREAD_DIFF1 = feature6[c(num_train + 3): c(num_total - 1)],
  SPREAD = data$SPREAD[c(num_train + 3): c(num_total - 1)],
  SPREAD_1DAY_BEFORE = data$SPREAD[c(num_train + 2): c(num_total - 2)],
  SPREAD_2DAY_BEFORE = data$SPREAD[c(num_train + 1): c(num_total - 3)]
)

yfit = wbart(
  x_train, real_train_val, x_test,
  nskip=500,ndpost=5000
)

x_axis_train = data$X[3: c(num_train + 2)]

x_axis_test = data$X[c(num_train + 3): c(num_total - 1)]

x_axis = data$X[3: c(num_total - 1)]

plot(x_axis_train,real_train_val,
     cex=.3,cex.axis=.8,cex.lab=.7, mgp=c(1.3,.3,0),tcl=-.2,lty=1)
lines(x_axis_train,apply(yfit$yhat.train,2,mean),col="red",lwd=1.5,lty=2)

#qm = apply(yfit$yhat.train,2,quantile,probs=c(.025,.975)) # post quantiles
#lines(x_axis_train,qm[1,],col="grey",lty=1,lwd=1.0)
#lines(x_axis_train,qm[2,],col="grey",lty=1,lwd=1.0)
legend("topleft",legend=c("real train data","prediction of train data"),
       col=c("black","red"), lwd=c(2,2), lty=c(1,2), bty="n",cex=.8,seg.len=3)

plot(x_axis_test,real_test_val,
     cex=.3,cex.axis=.8,cex.lab=.7, mgp=c(1.3,.3,0),tcl=-.2,lty=1)
lines(x_axis_test,apply(yfit$yhat.test,2,mean),col="red",lwd=1.5,lty=2)

#qm = apply(yfit$yhat.test,2,quantile,probs=c(.025,.975)) # post quantiles
#lines(x_axis,qm[1,],col="grey",lty=1,lwd=1.0)
#lines(x_axis,qm[2,],col="grey",lty=1,lwd=1.0)
legend("bottomright",legend=c("real test data","prediction of test data"),
       col=c("black","red"), lwd=c(2,2), lty=c(1,2), bty="n",cex=.8,seg.len=3)

plot(x_axis,real_val,
     cex=.3,cex.axis=.8,cex.lab=.7, mgp=c(1.3,.3,0),tcl=-.2,lty=1, col="blue")
lines(x_axis_train,apply(yfit$yhat.train,2,mean),col="orange",lwd=1.5,lty=2)
lines(x_axis_test,apply(yfit$yhat.test,2,mean),col="green",lwd=1.5,lty=2)

#qm = apply(yfit$yhat.train,2,quantile,probs=c(.025,.975)) # post quantiles
#lines(x_axis_train,qm[1,],col="grey",lty=1,lwd=1.0)
#lines(x_axis_train,qm[2,],col="grey",lty=1,lwd=1.0)
legend("topleft",legend=c("real train data","prediction of train data", "prediction of test data"),
       col=c("blue","orange", "green"), lwd=c(2,2,2), lty=c(1,2,2), bty="n",cex=.8,seg.len=3)


MSE = mean((yfit$yhat.test.mean - real_test_val)^2)
MSE_train = mean((yfit$yhat.train.mean - real_train_val)^2)
pred_train = apply(yfit$yhat.train,2,mean)
pred_test = apply(yfit$yhat.test,2,mean)
diff_pred_test = diff(pred_test)
diff_real_test = diff(real_test_val)
sum(diff_pred_test > 0 & diff_real_test > 0)
sum(diff_pred_test > 0 & diff_real_test <= 0)
sum(diff_pred_test <= 0 & diff_real_test > 0)
sum(diff_pred_test <= 0 & diff_real_test <= 0)

#yfit$prob.test.mean = apply(yfit$prob.test, 2, mean)
#test_pre = as.double(yfit$prob.test.mean>0.5)
#real_test_val - test_pre
#train_pre = as.double(yfit$prob.train.mean > 0.5)
#sum(abs(real_train_val-train_pre))
predict_train= data.frame(
  TIME = time[4:c(num_train + 3)],
  REAL_TRAIN = real_train_val,
  PRED_TRAIN = pred_train
)
predict_test = data.frame(
  TIME = time[c(num_train + 4): num_total],
  REAL_TEST = real_test_val,
  PRED_TEST = pred_test
)

write.csv(predict_train, file="PRED_TRAIN_BART.csv")
write.csv(predict_test, file="PRED_TEST_BART.csv")
