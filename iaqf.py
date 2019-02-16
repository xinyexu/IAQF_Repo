import numpy as np
import pandas as pd
import io
import requests
import matplotlib.pyplot as plt

def find_problem_dates(t_bill, corporate_dates):
    """
    This function checks if two list of dates match.
    input variables: two lists containing string data
    """
    in_t_not_cor = []
    in_cor_not_t = []
    for i in corporate_dates:
        if i not in t_bill:
            in_cor_not_t.append(i)
    for i in t_bill:
        if i not in corporate_dates:
            in_t_not_cor.append(i)
    return in_t_not_cor, in_cor_not_t
#in_t_not_cor, in_cor_not_t = find_problem_dates(list(t_bill_daily["DATE"]), 
#                                                list(corporate_daily["DATE"]))
"""Data Extraction"""
start_date = "1996-12-31" 
end_date = "2019-01-22"
# below are urls of csv data
# the last line shows the overall range of provided data
# the date in the middle shows the part we extract
# be sure not to extract data that exceeds the range
# 1996-12-31 to 2019-01-21
# ----------------------------------------------------------------------------
# read url
# ----------------------------------------------------------------------------
tbill_10year_daily_url = "https://fred.stlouisfed.org/graph/fredgraph.csv?bg"\
    "color=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23f"\
    "fffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&t"\
    "ts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&s"\
    "how_tooltip=yes&id=DGS10&scale=left&cosd"\
    "=" + start_date + "&coed=" + end_date + "&"\
    "line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&"\
    "mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Daily&fam=avg&fgst=lin&fg"\
    "snd=2009-06-01&line_index=1&transformation=&vintage_date=2019-01-21&rev"\
    "ision_date=2019-01-21&nd=1962-01-02"

corporate3A_effective_yield_url = "https://fred.stlouisfed.org/graph/fredgra"\
    "ph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgc"\
    "olor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%2344444"\
    "4&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_ti"\
    "tles=yes&show_tooltip=yes&id=BAMLC0A1CAAAEY&scale=left&cosd"\
    "=" + start_date + "&coed=" + end_date + "&"\
    "line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&"\
    "mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Daily%2C%20Close&fam=avg&"\
    "fgst=lin&fgsnd=2009-06-01&line_index=1&transformation=lin&vintage_date="\
    "2019-01-21&revision_date=2019-01-21&nd=1996-12-31"

vix_url = "https://raw.githubusercontent.com/israeldi/IAQF_Repo/master/VIX.c"\
    "sv?token=Adz3eDBWYvzwzvryfa2bkzbv8WVYZcacks5ccDzLwA%3D%3D"
    
sp500_url = "https://raw.githubusercontent.com/israeldi/IAQF_Repo/master/SP5"\
    "00.csv?token=Adz3eKtYe3cIRzh-uVepAn7hL5SxIW60ks5ccEU0wA%3D%3D"
    
tbill_10m2_url = "https://raw.githubusercontent.com/israeldi/IAQF_Repo/maste"\
    "r/T10Y2Y.csv?token=Adz3eLkLfrG89B485J_tlys8LmyiGB3uks5ccLZdwA%3D%3D"

skew_url = "https://raw.githubusercontent.com/israeldi/IAQF_Repo/master/skew"\
    "dailyprices.csv?token=Adz3eBMpEkTEFSGm2JyqVouIEAP8VPiMks5ccLakwA%3D%3D"
# ----------------------------------------------------------------------------
# convert url into dataframe
# ----------------------------------------------------------------------------
tbill_string_file = requests.get(tbill_10year_daily_url).content
t_bill_daily = pd.read_csv(io.StringIO(tbill_string_file.decode('utf-8')))

cor_3A_string_file = requests.get(corporate3A_effective_yield_url).content
corporate_daily = pd.read_csv(io.StringIO(cor_3A_string_file.decode('utf-8')))

vix_string_file = requests.get(vix_url).content
vix_daily = pd.read_csv(io.StringIO(vix_string_file.decode('utf-8')))

sp500_string_file = requests.get(sp500_url).content
sp500_daily = pd.read_csv(io.StringIO(sp500_string_file.decode('utf-8')))

t10m2_string_file = requests.get(tbill_10m2_url).content
t10m2_daily = pd.read_csv(io.StringIO(t10m2_string_file.decode('utf-8')))

skew_string_file = requests.get(skew_url).content
skew_daily = pd.read_csv(io.StringIO(skew_string_file.decode('utf-8')))

""" Data Cleaning """
# ----------------------------------------------------------------------------
# convert date into same standard
# ----------------------------------------------------------------------------
t_bill_daily["DATE"] = pd.to_datetime(t_bill_daily["DATE"])
corporate_daily["DATE"] = pd.to_datetime(corporate_daily["DATE"])
vix_daily["DATE"] = pd.to_datetime(vix_daily["Date"])
sp500_daily["DATE"] = pd.to_datetime(sp500_daily["Date"])
t10m2_daily["DATE"] = pd.to_datetime(t10m2_daily["DATE"])
skew_daily["DATE"] = pd.to_datetime(skew_daily["Date"])
# ----------------------------------------------------------------------------
# merge dataframes
# ----------------------------------------------------------------------------
combined = pd.merge(corporate_daily, t_bill_daily, 
                    how='inner', left_on=['DATE'], right_on=['DATE'])

combined = pd.merge(combined, vix_daily,
                    how = "inner", left_on = ["DATE"], right_on = ["DATE"])

combined = pd.merge(combined, sp500_daily,
                    how = "inner", left_on = ["DATE"], right_on = ["DATE"])

combined = pd.merge(combined, t10m2_daily,
                    how = "inner", left_on = ["DATE"], right_on = ["DATE"])

combined = pd.merge(combined, skew_daily,
                    how = "inner", left_on = ["DATE"], right_on = ["DATE"])
# ----------------------------------------------------------------------------
# select features
# ----------------------------------------------------------------------------
col_names = ["DATE", "BAMLC0A1CAAAEY", "DGS10", "VIX", "Adj Close", "T10Y2Y",
             "SKEW"]
combined = combined[col_names]
# ----------------------------------------------------------------------------
# deal with missing values, displayed as "." or "NA"
# ----------------------------------------------------------------------------
combined = pd.DataFrame.replace(combined, to_replace=".", value=float("NaN"))
combined = combined.fillna(method="ffill")
# ----------------------------------------------------------------------------
# deal with data type problem, convert all str to float
# ----------------------------------------------------------------------------
combined.BAMLC0A1CAAAEY = combined.BAMLC0A1CAAAEY.astype(float)
combined.DGS10 = combined.DGS10.astype(float)
combined.T10Y2Y = combined.T10Y2Y.astype(float)
# ----------------------------------------------------------------------------
# generate spread, defined as (BAMLC0A1CAAAEY - DGS10)
# ----------------------------------------------------------------------------
combined["SPREAD"] = combined["BAMLC0A1CAAAEY"] - combined["DGS10"]
# ----------------------------------------------------------------------------
# generate feature difference data
# defined as DIFF_{t} = DATA_{t} - DATA_{t-1}
# ----------------------------------------------------------------------------
combined["SPREAD_DIFF1"] = combined["SPREAD"] - combined["SPREAD"].shift(1)
combined["DGS10_DIFF1"] = combined["DGS10"] - combined["DGS10"].shift(1)
combined["VIX_DIFF1"] = combined["VIX"] - combined["VIX"].shift(1)
combined["SLOPE"] = combined["T10Y2Y"] - combined["T10Y2Y"].shift(1)
combined["SKEW_DIFF1"] = combined["SKEW"] - combined["SKEW"].shift(1)
combined["SP500_R"] = (combined["Adj Close"] - 
        combined["Adj Close"].shift(1)) / combined["Adj Close"].shift(1)
features = ["DGS10_DIFF1", "VIX_DIFF1", "SLOPE", "SKEW_DIFF1", "SP500_R"]
others = ["DATE", "SPREAD_DIFF1"]
combined = combined[features+others].dropna()


# ----------------------------------------------------------------------------
# below are two simple models
# ----------------------------------------------------------------------------
"""Regression"""
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

Y, X = combined["SPREAD_DIFF1"], combined[features]

reg_model = LinearRegression()
reg_model.fit(X,Y)
Y_predicted = reg_model.predict(X)

r2 = r2_score(Y,Y_predicted)
plt.plot(Y)
plt.plot(Y_predicted)



"""Transfer to Classification Problem"""

"""Logistic Regression"""
# if spread goes up or stays the same, define as 1
# if spread goes down, defines as 0
# defined as : today's spread - yesterday's spread
combined["spread_01"] = combined["SPREAD_DIFF1"].map(lambda x: 1 if x>=0 else 0)
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
scores = cross_val_score(log_reg, X_all, Y_all, scoring="accuracy", cv=5)
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
