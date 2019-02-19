"""SGD Approach"""
# ----------------------------------------------------------------------------
# convert Y to two classes
# ----------------------------------------------------------------------------
combined_monthly["spread_01"] = combined_monthly["SPREAD_DIFF1"].map(
        lambda x: 1 if x > 0 else 0)
# ----------------------------------------------------------------------------
# load and split the data 
# ----------------------------------------------------------------------------
from sklearn.model_selection import train_test_split
X_all = combined_monthly[features]
Y_all = combined_monthly["spread_01"]
num_test = 0.2
x_train, x_test, y_train, y_test = train_test_split(X_all, Y_all,
                                                    test_size=num_test,
                                                    random_state=250)
# ----------------------------------------------------------------------------
# scale the data
# ----------------------------------------------------------------------------
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
# ----------------------------------------------------------------------------
# fit SGD classifier
# ----------------------------------------------------------------------------
from sklearn.linear_model import SGDClassifier
sgd = SGDClassifier(random_state = 10)
sgd.fit(x_train_scaled,y_train)

from sklearn.model_selection import cross_val_score
cross_val_score(sgd,x_train_scaled,y_train,cv=5,scoring="accuracy")

from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix
y_train_predicted = cross_val_predict(sgd,x_train_scaled,y_train,cv=5)
c_matrix_train = confusion_matrix(y_train,y_train_predicted)

import seaborn as sns
import matplotlib.pyplot as plt
sns.heatmap(c_matrix_train)
plt.show()