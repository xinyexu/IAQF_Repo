library(survival)
library(nnet)
library(nlme)
library(BART)
data = read.csv("data.csv", header = T)
date = as.character(data$y_and_m)
num_total = length(date)
num_train = 200
num_test = num_total - num_train
feature1 = data$DGS10_DIFF1
feature2 = data$VIX_DIFF1
feature3 = data$SLOPE
feature4 = data$SKEW_DIFF1
feature5 = data$SP500_R
real_train_val = data$spread_01[2:c(num_train+1)]
real_test_val = data$spread_01[c(num_train + 2):num_total]
set.seed(20190220)
x_train = data.frame(
  DGS10_DIFF1 = feature1[1:num_train],
  VIX_DIFF1 = feature2[1:num_train],
  SLOPE = feature3[1:num_train],
  SKEW_DIFF1 = feature4[1:num_train],
  SP500_R = feature5[1:num_train]
)
x_test = data.frame(
  DGS10_DIFF1 = feature1[c(num_train + 1): c(num_total - 1)],
  VIX_DIFF1 = feature2[c(num_train + 1): c(num_total - 1)],
  SLOPE = feature3[c(num_train + 1): c(num_total - 1)],
  SKEW_DIFF1 = feature4[c(num_train + 1): c(num_total - 1)],
  SP500_R = feature5[c(num_train + 1): c(num_total - 1)]
)

yfit = pbart(
  x_train, real_train_val, x_test,
  ndpost=1000, nskip=100
)

yfit$prob.test.mean = apply(yfit$prob.test, 2, mean)
test_pre = as.double(yfit$prob.test.mean>0.5)
real_test_val - test_pre
train_pre = as.double(yfit$prob.train.mean > 0.5)
sum(abs(real_train_val-train_pre))

