# ----------------------------------------------------------------------------
# below are two simple models
# ----------------------------------------------------------------------------
"""Regression"""
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import statsmodels.api as sm

Y, X = combined_monthly["SPREAD_M_DIFF1"], combined_monthly[features]

reg_model = LinearRegression()
reg_model.fit(X,Y)
Y_predicted = reg_model.predict(X)

r2 = r2_score(Y,Y_predicted)
X2 = sm.add_constant(X)
est = sm.OLS(Y, X2)
est2 = est.fit()
print(est2.summary())


"""Transfer to Classification Problem"""

"""Logistic Regression"""
# if spread goes up or stays the same, define as 1
# if spread goes down, defines as 0
# defined as : today's spread - yesterday's spread
combined["spread_01"] = combined["SPREAD_SHIFT1"].map(lambda 
        x: 1 if x >= 0.5 else 0)
combined_monthly["spread_01"] = combined_monthly["SPREAD_M_DIFF1"].map(lambda 
                x: 1 if x >= 0 else 0)
# split the data
from sklearn.model_selection import train_test_split
X_all = combined[features]
Y_all = combined["spread_01"]
num_test = 0.2
x_train, x_test, y_train, y_test = train_test_split(X_all, Y_all,
                                                    test_size=num_test,
                                                    random_state=250)
# try logistic regression
from sklearn.linear_model import LogisticRegression
log_reg = LogisticRegression()
log_reg.fit(x_train, y_train)
from sklearn.model_selection import cross_val_score
scores = cross_val_score(log_reg, X_all, Y_all, scoring="accuracy", cv=10)
#using the model on test data
y_train_predicted = log_reg.predict_proba(x_train)
y_predicted = log_reg.predict(x_test)

#using ROC curve and precision recall curve to visualize the result
from sklearn.metrics import roc_curve,precision_recall_curve
fpr,tpr,roc_thresholds = roc_curve(y_train,y_train_predicted[:,1])
precisions, recalls, pr_thresholds = precision_recall_curve(
                                         y_train, y_train_predicted[:,1])

def plot_roc_curve(fpt,tpr):
    plt.plot(fpr,tpr,linewidth=2)
    plt.plot([0,1],[0,1],"k--")
    plt.axis([0,1,0,1])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    
def plot_precision_recall_curve_vs_threshold(precisions,recalls,thresholds):
    plt.plot(thresholds,precisions[:-1],"b--",label="Precision")
    plt.plot(thresholds,recalls[:-1],"g-",label="Recall")
    plt.xlabel("Threshold")
    plt.legend(loc="upper left")
    plt.ylim([0,1])
    
plt.subplot(1,2,1)
plot_roc_curve(fpr,tpr)
plt.subplot(1,2,2)
plot_precision_recall_curve_vs_threshold(precisions,recalls,pr_thresholds)
plt.show()