# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 10:28:00 2023

@author: jhe
"""
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 10:28:00 2023
#only functions

@author: jhe
"""
from scipy import stats
from scipy.stats import ttest_ind, f_oneway, levene #statistical tool to calculate the desired p-value
import numpy as np
from scipy.stats import ttest_ind
import statsmodels.stats.weightstats as st

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




#perform a two one-sided equivalence test (TOST) for equivalence ye
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

    
    


def two_sample_equivalence_test(data1, data2):
    alpha = 0.05
    acceptable_range = 0.0025  # Minimum acceptable range for difference in mean
    mean = abs(np.mean(data1)-np.mean(data2))
    
    low = mean-acceptable_range
    upp = mean+acceptable_range

    # Perform the equivalence test
    result = st.ttost_ind(data1, data2, low, upp, usevar='unequal', weights=(None, None), transform=None)

    p_value = result[0]

    if p_value < alpha:
        is_equivalent = True
    else:
        is_equivalent = False

    return [is_equivalent, p_value]


# Function to round a number to 4 decimal xD
def round_to_4_decimals(num):
    return round(num, 4)
