# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 10:28:00 2023

@author: jhe
"""
from scipy.stats import ttest_ind, f_oneway, levene #statistical tool to calculate the desired p-value
import numpy as np

#desired to transform ibsens DE sheets into a dataframe structure that makes sense
def transform_headers(df):
    # initialize a variable to store the previous column name
    prev_col = ''
    
    # loop over the column names and replace "Unnamed:" with "std" followed by the previous column name
    for i, col_name in enumerate(df.columns):
        if col_name.startswith('Unnamed:'):
            new_col_name = f'std{prev_col}_{col_name.split(":")[1]}'
            new_col_name = new_col_name.split("_")[0] # remove the "_number" from the column name
            df.rename(columns={col_name: new_col_name}, inplace=True)
        else:
            prev_col = col_name
    
    return df

def equivalence_test(data1, data2):
    # Calculate the mean and standard deviation of the two data sets
    mean1 = np.mean(data1)
    mean2 = np.mean(data2)
    std1 = np.std(data1, ddof=len(data1)-1)
    std2 = np.std(data2, ddof=len(data2)-1)

    # Calculate the critical value for the specified significance level
    n1 = len(data1)
    n2 = len(data2)
    df = n1 + n2 - 2
    alpha = 0.05 #5% significance = 95% confidence
    t_stat, p_value = ttest_ind(data1, data2)  # Get the t-value and p-value from a t-test
    t_crit = np.abs(t_stat)  # Take the absolute value

    # Calculate the equivalence bounds
    equivalence_range = 0.005  # 0.5% range
    equivalence_bound = equivalence_range * np.sqrt((std1 ** 2 + std2 ** 2) / 2)

    # Calculate the confidence interval
    conf_interval = np.abs(mean1 - mean2) - t_crit * np.sqrt((std1 ** 2 / n1) + (std2 ** 2 / n2))

    # Perform the equivalence test
    if conf_interval <= equivalence_bound:
        return "The mean of the data sets are equivalent.", p_value
    else:
        return "The mean of the data sets are not equivalent.", p_value

#perform a two one-sided equivalence test (TOST) for equivalence
def two_one_sided_t_test(data1, data2, alpha=0.05): #alpha is significance level
    tost_low = -0.0025 #define the pre defined range
    tost_high = 0.0025 #is between -0.25% and +0.25%. which is a total of 0.5%
     
    #calculate p-value
    t_stat_low, p_value_low = ttest_ind(data1, data2-tost_low)
    t_stat_high, p_value_high = ttest_ind(data1-tost_high, data2)
    p_value_tost = p_value_low + p_value_high
    
    #compare p-value to significance
    if p_value_tost < alpha:
        return ['True', p_value_tost]
    else:
        return ['Fail to reject H_0', p_value_tost]

    
#Compare the variance of the two data sets using Levene's test
def levene_test(data1,data2,alpha=0.05):
    levene_stat, p_value_levene = levene(data1, data2)
    if p_value_levene < alpha:
        why_string = ("The variances of the two populations are significantly different")
    else:
        why_string = ("No-significant difference between the variances of the two populations")
    return ['levene_stat',levene_stat,
            'p_value_levene',p_value_levene,
            'explanation',why_string
           ] 

#I make a function that removes outliers in data
def remove_outliers(df):
    # Calculate z-score for each group
    z_scores = df.groupby("Grating")["DE"].transform(lambda x: (x - x.mean()) / x.std())
    # Define threshold for outliers (e.g., z-score > 3 or z-score < -3)
    threshold = 3
    # Filter out rows with z-score exceeding the threshold
    filtered_df = df[abs(z_scores) <= threshold]
    return filtered_df
