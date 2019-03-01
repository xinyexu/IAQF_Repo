# IAQF_Repo

### MODEL LEARN WEB
https://machinelearningmastery.com/time-series-prediction-lstm-recurrent-neural-networks-python-keras/

### IAQF Report Link
https://www.overleaf.com/4993599915ftffjshfbfkz

### Leverage and Spread 

Main conclusion: <br />
The effect of future leverage is large, generally exceeding the effect of contemporaneous leverage to predict spread.

Contemporaneous leverage: 
1. Market value of debt / (Market value of debt + Market value of equity)
2. Book value of debt / Book value of debt and equity 

To investigate leverage prediction by investors, we construct 3 proxies for leverage changes, based on 3 theoretical perspectives on firm capital structure:
1. LEV(t+1), (LEV(t),a vector of firm characteristics: lots of financial statement data), linear model; relies on the trade-off theory, 
2. FINDEFA, (cash dividends, net investment, working capital, net cash flow) relies on the pecking order theory, 
3. Dummy variable CRPOM: firms with a “plus or minus” credit rating (CRPOM = 1) more frequently choose equity over debt financing, ceteris paribus.derives from Kisgen’s (2006) hypothesis that firms close to the next higher rating (e.g., BBB+ is close to A–) prefer to avoid issuing new debt.

A vector of firm characteristics to predict LEV: <br />
EBIT TA is earnings before interest and taxes scaled by total assets, MB is the ratio of market-to-book value of assets, DEP TA is depreciation expense to total assets, lnTA is the natural log of total assets, FA TA is the ratio of fixed-to-total assets, R&D DUM is an indicator variable for whether the firm reports an R&D expenditure or not, R&D TA is R&D expenditures scaled by total assets, RATED is an indicator for whether the firm has rated debt, and IND MED is the median leverage for each firm’s industry.

![alt text](https://github.com/xinyexu/Enrollment-Workshop/blob/master/Leverage%20Expectations%20and%20Bond%20Credit%20Spreads.png)

Main model for spread: mixed linear modeld with quadratic term of LEV and dummy variable EXP INCR, <br />
EXP DECR (EXP INCR) equals unity when a firm’s (LEV∗j,t+1 − LEVj,t) is in the bottom (top) tercile for a given quarter. For the pecking order hypothesis, EXP DECR (EXP INCR) equals unity when a firm’s Et(FINDEFAj,t+1) is in the bottom (top) tercile for a given quarter.

Data: on the quarterly accounting data, <br />
Main reference: Leverage Expectations and Bond Credit Spreads.pdf
