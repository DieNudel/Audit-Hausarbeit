import pandas as pd
import numpy as np
from scipy.stats import ttest_ind, t, wilcoxon, ranksums, mannwhitneyu, norm
import matplotlib.pyplot as plt

TRIM = .05

# weekday dict
weekday_dict = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

df = pd.read_csv("data.csv")

# convert Date column to weekday

df['Date'] = pd.to_datetime(df['Date'])
df['Weekday'] = df['Date'].dt.dayofweek

# ln of Adj Close column

df['ln_Adj Close'] = df['Adj Close'].apply(lambda x: np.log(x))

# diff of ln of Adj Close column

df['diff_ln_Adj Close'] = df['ln_Adj Close'].diff()

# for each weekday, group by weekday and other days, and calculate t-test

for i in range(5):
    # print pretty name of weekday
    print(weekday_dict[i])
    
    # print t-test result
    t_stat, p = ttest_ind(df[df['Weekday'] == i]['diff_ln_Adj Close'].dropna(
    ), df[df['Weekday'] != i]['diff_ln_Adj Close'].dropna(), trim=TRIM)
    print("t-stat: ", t_stat)
    print("p-value: ", p)

    # critical = t.ppf(q=TRIM, df=len(
    #     df[df['Weekday'] == i]['diff_ln_Adj Close'].dropna()) - 2)
    # print("Critical stuff:", end=" ")
    # print(critical)

    # if (t_stat < critical and p < TRIM):
    if (p < TRIM):
        print("Reject null hypothesis")
    else:
        print("Fail to reject null hypothesis")

    # box plot into file

    df[df['Weekday'] == i]['diff_ln_Adj Close'].dropna().plot.box(
        title=weekday_dict[i])
    plt.savefig(weekday_dict[i] + ".png")
    plt.close()

    print("")

###Select all of Weekday 1 < Weekday 2, choose random same amount as Weekday 1 out of Weekday 2 

print(df[df['Weekday'] == 0].size)
print(df[df['Weekday'] == 4].size)
n=(min((df[df['Weekday'] == 0]['diff_ln_Adj Close'].dropna().size),(df[df['Weekday'] == 4]['diff_ln_Adj Close'].dropna().size)))

print(ranksums(df[df['Weekday'] == 0]['diff_ln_Adj Close'].dropna().sample(n=n), df[df['Weekday'] == 4 ]['diff_ln_Adj Close'].dropna().sample(n=n)))

pvalue = float((input("pvalue eingabe")))
#####R-(n(n1+1))/2

# zvalue = norm.ppf(pvalue/2)

# criticalranksum = t.ppf(q=TRIM, df=len(
#         df[df['Weekday'] == i]['diff_ln_Adj Close'].dropna()) - 2)
# print("Critical stuff:", end=" ")
# print(critical)
# if (pvalue < criticalranksum and p < TRIM):

if (pvalue < TRIM):
    print("Reject null hypothesis")
else:
    print("Fail to reject null hypothesis")


# print(mannwhitneyu(df[df['Weekday'] == 0]['diff_ln_Adj Close'].dropna().sample(n=n), df[df['Weekday'] == 4 ]['diff_ln_Adj Close'].dropna().sample(n=n)))

# if (pvalue < TRIM):
#         print("Reject null hypothesis")
# else:
#         print("Fail to reject null hypothesis")



############
#print(wilcoxon(df[df['Weekday'] == 0]['diff_ln_Adj Close'].dropna().sample(n=n), df[df['Weekday'] == 4 ]['diff_ln_Adj Close'].dropna().sample(n=n)))

##Unnötige Kack Statstiken

for i in range(5): 
    print(df[df['Weekday'] == i].size)
    print(np.nanmax(df[df['Weekday'] == i]["diff_ln_Adj Close"]))
    print(df["Date"][(df[df['Weekday'] == i]["diff_ln_Adj Close"].idxmax())])
    print(np.nanmin(df[df['Weekday'] == i]["diff_ln_Adj Close"]))
    print(df["Date"][(df[df['Weekday'] == i]["diff_ln_Adj Close"].idxmin())])
    print(np.mean(df[df['Weekday'] == i]["diff_ln_Adj Close"]))
    
    
   



