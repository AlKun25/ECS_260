library(tidyverse)
library(stats)
library(olsrr)
library(car)

data_path = NULL #
dataset <- read_csv(data_path)

# Step 0: Exploring the data
summary(dataset)
temp %>% ggplot() + geom_histogram(mapping=aes(x=num_shared_developers)) + theme_minimal()

# Step 1: Preprocess
# handle outliers
# identify influential points

# Step 1: Correlation: understand data and how each variable relates to the other 
# cor: calculates the Pearson's correlation coefficient for two random variables
correlations_all <- cor(dataset)
# visualization
corrplot(correlations_all, type='upper')
corrplot.mixed(correlations_all)


# Step 2: Regression
# Simple linear regression
# RQ1
rq1_model1 <- lm(data=dataset, acceptance_rate ~ num_shared_developer)
rq1_model1
summary(rq1_model1) # Check coefficients, significance, r-squared, f-statistics

# Multiple linear regression (multiple independent variable)
rq1_model2 <- lm(data=dataset, acceptance_rate ~ num_shared_developer + multitasking_size)
summary(rq1_model2) # Check coefficients, significance, r-squared, f-statistics

ols_plot_resid_hist(rq1_model2) # check normality of residuals
ols_plot_resid_fit(rq1_model2) # check homoscedasticity of residuals
durbinWatsonTest(rq1_model2) # check residual autocorrelation

# (optional)
# influential point analysis
ols_plot_cooksd_chart(rq1_model2)
cooks_outliers <- ols_plot_cooked_chart(rq1_model2)$outliers
arrange(cooks_outliers, desc(cooks_distance))


# Step 3: Improving model
# Consider nonlinear relationships
dataset2 <- dataset2 %>% mute(num_shared_developer2 = num_shared_developer^2)
rq1_model3 <- lm(data=dataset2, acceptance_rate ~ num_shared_developer2 + multitasking_size)
summary(rq1_model3)

# (optional) considering categorical variables if any
# (optional) considering interactions between variables
