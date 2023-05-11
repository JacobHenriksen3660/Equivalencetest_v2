# Equivalencetest_v2
Equivalence test at ibsen to test DE2 vs DE3 using scipy.

The .py file ttest_functions.py includes the follwoing funcitons:

transform_headers transforms Ibsens DE data headers to a structure that fits a data frame

two_one_sided_t_test uses scipy to calculate the p value and evaluate the p value according to the significance level for a equivalence test. The function requires two data sets and the choice of significance level.

levene_test uses scipy to calculate the p value and evaluate the p value according to the significance level for a Levene test that tests the difference in variance between two data sets. The function requires two data sets and the choice of significance level.

t-test_random_groups.ipynb is the notebook used to run the functions for equvalence test on each gratins with random split up in data.
