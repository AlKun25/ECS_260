# Load necessary libraries
library(tidyverse)  # For data manipulation and visualization
library(broom)      # For tidying up model outputs
library(dplyr)
install.packages("corrplot")
library(corrplot)
install.packages("gridExtra")
library(ggplot2)
library(gridExtra)


# Step 1: Preliminary Cleaning
# Remove rows with missing values
# X: median_avg_multitasking_repos_count, max_multitasking_repos_count, median_avg_total_commits, total_devs, sum_s_focus
# Y: lines_added, avg_unit_complexity, avg_unit_size, lines_added_per_dev

df2 <- read.csv('f6_rq2_data_reduced.csv', header=T)
df2$lines_added_per_dev <- df2$lines_added / df2$multitask_devs
df_subset <- df2[c("median_multitasking_repos_count", "max_multitasking_repos_count", "median_total_shared_dev_commits", "lines_added", "avg_unit_complexity", "avg_unit_size", "lines_added_per_dev", "total_devs", "sum_s_focus", "created_since", "multitask_devs")]
df_subset <- subset(df_subset, avg_unit_complexity>0 & avg_unit_size>0) # 2412


# week since creation
df_subset %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=created_since)) +
  theme_minimal() +
  ggtitle("Weeks Since Creation Distribution")

summary(df_subset$created_since) # min 10, 1st Qu 162, median 280.5, 3rd Qu 423, max 787
#





# Histogram
summary(df_subset)

std <- sapply(df_subset, sd)
std

plot1 <- df_subset %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=median_multitasking_repos_count)) +
  theme_minimal() +
  ggtitle("Number of multitasking repos(X1) Distribution")

plot2 <- df_subset %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=max_multitasking_repos_count)) +
  theme_minimal() +
  ggtitle("Number of max multitasking repos(X2) Distribution")

plot3 <- df_subset %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=median_total_shared_dev_commits)) +
  theme_minimal() +
  ggtitle("Multitasking developers commits (X3) Distribution")

plot4 <- df_subset %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=total_devs)) +
  theme_minimal() +
  ggtitle("Total number of developers (X4) Distribution")

plot5 <- df_subset %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=sum_s_focus)) +
  theme_minimal() +
  ggtitle("S_focus (X5) Distribution")


plot6 <- df_subset %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=lines_added)) +
  theme_minimal() +
  ggtitle("LOC added (Y1) Distribution")

plot7 <- df_subset %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=avg_unit_complexity)) +
  theme_minimal() +
  ggtitle("Unit complexity (Y2) Distribution")

plot8 <- df_subset %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=avg_unit_size)) +
  theme_minimal() +
  ggtitle("Unit size (Y3) Distribution")

plot9 <- df_subset %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=lines_added_per_dev)) +
  theme_minimal() +
  ggtitle("LOC added per dev (Y4) Distribution")

plot10 <- df_subset %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=lines_added_per_dev)) +
  theme_minimal() +
  ggtitle("Weeks since creation Distribution")



grid.arrange(plot1, plot2, plot3, plot4, plot5, plot6, plot7, plot8, plot9,plot10, ncol = 5)




df_clean <- na.omit(df_subset)

# Remove outliers (generic function)
remove_outliers <- function(x) {
  qnt <- quantile(x, probs=c(.25, .75), na.rm = T)
  H <- 1.5 * IQR(x, na.rm = T)
  y <- x
  y[x < (qnt[1] - H)] <- NA
  y[x > (qnt[2] + H)] <- NA
  return(y)
} 

df_clean <- df_clean %>%
  mutate_at(vars(median_multitasking_repos_count, max_multitasking_repos_count, median_total_shared_dev_commits, total_devs, sum_s_focus, lines_added), remove_outliers) %>%
  na.omit()

df_clean$lines_added_per_dev <- df_clean$lines_added/df_clean$total_devs
summary(df_clean)

std <- sapply(df_clean, sd)
std

plot1 <- df_clean %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=median_multitasking_repos_count)) +
  theme_minimal() +
  ggtitle("Number of multitasking repos(X1) Distribution")

plot2 <- df_clean %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=max_multitasking_repos_count)) +
  theme_minimal() +
  ggtitle("Number of max multitasking repos(X2) Distribution")

plot3 <- df_clean %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=median_total_shared_dev_commits)) +
  theme_minimal() +
  ggtitle("Multitasking developers commits (X3) Distribution")

plot4 <- df_clean %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=total_devs)) +
  theme_minimal() +
  ggtitle("Total number of developers (X4) Distribution")

plot5 <- df_clean %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=sum_s_focus)) +
  theme_minimal() +
  ggtitle("S_focus (X5) Distribution")


plot6 <- df_clean %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=lines_added)) +
  theme_minimal() +
  ggtitle("LOC added (Y1) Distribution")

plot7 <- df_clean %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=avg_unit_complexity)) +
  theme_minimal() +
  ggtitle("Unit complexity (Y2) Distribution")

plot8 <- df_clean %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=avg_unit_size)) +
  theme_minimal() +
  ggtitle("Unit size (Y3) Distribution")

plot9 <- df_clean %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=lines_added_per_dev)) +
  theme_minimal() +
  ggtitle("LOC added per dev (Y4) Distribution")

plot10 <- df_clean %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=created_since)) +
  theme_minimal() +
  ggtitle("Weeks since creation Distribution")


grid.arrange(plot1, plot2, plot3, plot4, plot5, plot6, plot7,plot8,plot9,plot10, ncol = 5)




df_clean$log_median_multitasking_repos_count <- log(df_clean$median_multitasking_repos_count)
df_clean$log_max_multitasking_repos_count <- log(df_clean$max_multitasking_repos_count)
df_clean$log_median_total_shared_dev_commits <- log(df_clean$median_total_shared_dev_commits)
df_clean$log_total_devs <- log(df_clean$total_devs)
df_clean$log_sum_s_focus <- log(df_clean$sum_s_focus)

df_clean$lines_added_per_dev <- df_clean$lines_added / df_clean$multitask_devs



plot1 <- df_clean %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=log_median_multitasking_repos_count)) +
  theme_minimal() +
  ggtitle("Number of multitasking repos(X1) Distribution (log)")

plot2 <- df_clean %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=log_max_multitasking_repos_count)) +
  theme_minimal() +
  ggtitle("Number of max multitasking repos(X2) Distribution (log)")

plot3 <- df_clean %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=log_median_total_shared_dev_commits)) +
  theme_minimal() +
  ggtitle("Multitasking developers commits (X3) Distribution (log)")

plot4 <- df_clean %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=log_total_devs)) +
  theme_minimal() +
  ggtitle("Total number of developers (X4) Distribution (log)")

plot5 <- df_clean %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=log_sum_s_focus)) +
  theme_minimal() +
  ggtitle("S_focus (X5) Distribution (log)")


grid.arrange(plot1, plot2, plot3, plot4, plot5, ncol = 5)







# Scatter plot


df_long <- df_clean %>%
  gather(key = "independent_variable", value = "independent_value", log_median_multitasking_repos_count, log_max_multitasking_repos_count, log_median_total_shared_dev_commits, log_total_devs, log_sum_s_focus) %>%
  gather(key = "dependent_variable", value = "dependent_value", lines_added, avg_unit_complexity, avg_unit_size, lines_added_per_dev)


library(ggplot2)
library(gridExtra)
library(dplyr)

plots <- list()

for(indep_var in unique(df_long$independent_variable)){
  for(dep_var in unique(df_long$dependent_variable)){
    plots[[paste(indep_var, dep_var, sep = "_")]] <- df_long %>%
      filter(independent_variable == indep_var, dependent_variable == dep_var) %>%
      ggplot(aes(x = independent_value, y = dependent_value)) +
      geom_point(alpha = 0.5) +
      labs(title = paste(dep_var, "vs", indep_var),
           x = indep_var, 
           y = dep_var) +
      theme_bw() +
      theme(plot.title = element_text(size = 10),
            axis.text.x = element_text(size = 8, angle = 45, hjust = 1),
            axis.text.y = element_text(size = 8))
  }
}

do.call(grid.arrange, c(plots, ncol = length(unique(df_long$independent_variable))))



# Plotting with facets
# ggplot(df_long, aes(x = independent_value, y = dependent_value)) +
#   geom_point(alpha = 0.5) +
#   # geom_smooth(method = lm, se = FALSE, color = "red") +
#   facet_grid(dependent_variable ~ independent_variable, scales = "free", labeller = label_both) +
#   labs(title = "Scatter plots of all X and Y combinations", x = "Independent Variable Value", y = "Dependent Variable Value") +
#   theme_bw() +
#   theme(strip.text.x = element_text(size = 10, angle = 45),
#         strip.text.y = element_text(size = 10))

# Step 3: Scatter plot for each X and Y (Example for one Y, repeat for others)
# ggplot(df_scaled, aes(x = avg_multitasking_repos_count, y = lines_added)) +
#   geom_point(alpha = 0.5) +
#   geom_smooth(method = lm, se = FALSE, color = "red") +
#   labs(title = "Scatter plot of Lines Added vs. Avg Multitasking Repos Count", x = "Avg Multitasking Repos Count (Scaled)", y = "Lines Added (Scaled)")

# Repeat the plotting for other Y variables adjusting aes(x=, y=)











# Step 4: Correlation Matrix

cor_matrix <- cor(df_clean[, c("log_median_multitasking_repos_count", "log_max_multitasking_repos_count", "log_median_total_shared_dev_commits", "log_total_devs", "log_sum_s_focus", "lines_added", "avg_unit_complexity", "avg_unit_size", "lines_added_per_dev")], use = "complete.obs")
print(cor_matrix)
cor_matrix <- cor(df_clean[, c("log_median_multitasking_repos_count", "log_max_multitasking_repos_count", "log_median_total_shared_dev_commits", "log_total_devs", "log_sum_s_focus")], use = "complete.obs")
print(cor_matrix)
corrplot(cor_matrix, type='upper', title = "Correlation Matrix")


# Assuming df_clean is your data frame and cor_matrix is calculated as you've described


# Your specific variables for x and y axes
x_vars <- c("lines_added", "avg_unit_complexity", "avg_unit_size", "lines_added_per_dev")
y_vars <- c("log_median_multitasking_repos_count", "log_max_multitasking_repos_count", "log_median_total_shared_dev_commits", "log_total_devs", "log_sum_s_focus")

# Subset the correlation matrix
sub_cor_matrix <- cor_matrix[y_vars, x_vars]
corrplot(sub_cor_matrix, type='upper', title = "Correlation Matrix")





# Step 2: Standardization
# df_scaled <- as.data.frame(scale(df_clean))







## clustering
summary(df_clean$total_devs)
df_clean1 <- subset(df_clean, total_devs <2)
df_clean2 <- subset(df_clean, total_devs >= 2 & total_devs<3)
df_clean3 <- subset(df_clean, total_devs >=3 & total_devs<5)
df_clean4 <- subset(df_clean, total_devs >= 5)


df_clean11 <- subset(df_clean, created_since <162) # 475
df_clean22 <- subset(df_clean, created_since >= 162 & created_since<280) # 445
df_clean33 <- subset(df_clean, created_since >=280 & created_since<423.2) # 494
df_clean44 <- subset(df_clean, created_since >= 423.2) # 491







# Step 5: Fit Linear Regression (Example for one Y, repeat for others)
# model1 <- lm(log(lines_added+1) ~ avg_multitasking_repos_count + max_multitasking_repos_count + log_avg_total_shared_dev_commits, data = df_clean)
# summary(model1)
# plot(model1)


model1 <- lm(lines_added ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean)
summary(model1)
plot(model1)



model1 <- lm(lines_added ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean1)
summary(model1)
model1 <- lm(lines_added ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean2)
summary(model1)
model1 <- lm(lines_added ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean3)
summary(model1)
model1 <- lm(lines_added ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean4)
summary(model1)




model1 <- lm(lines_added ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean11)
summary(model1)
model1 <- lm(lines_added ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean22)
summary(model1)
model1 <- lm(lines_added ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean33)
summary(model1)
model1 <- lm(lines_added ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean44)
summary(model1)



# model2 <- lm(avg_unit_complexity ~ avg_multitasking_repos_count + max_multitasking_repos_count + log_avg_total_shared_dev_commits, data = df_clean)
# summary(model2)
# plot(model2)

model2 <- lm(avg_unit_complexity ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean)
summary(model2)
plot(model2)


model2 <- lm(avg_unit_complexity ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean1)
summary(model2)
model2 <- lm(avg_unit_complexity ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean2)
summary(model2)
model2 <- lm(avg_unit_complexity ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean3)
summary(model2)
model2 <- lm(avg_unit_complexity ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean4)
summary(model2)

model2 <- lm(avg_unit_complexity ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean11)
summary(model2)
model2 <- lm(avg_unit_complexity ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean22)
summary(model2)
model2 <- lm(avg_unit_complexity ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean33)
summary(model2)
model2 <- lm(avg_unit_complexity ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean44)
summary(model2)



# model3 <- lm(avg_unit_size ~ avg_multitasking_repos_count + max_multitasking_repos_count + log_avg_total_shared_dev_commits, data = df_clean)
# summary(model3)
# plot(model3)

model3 <- lm(avg_unit_size ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean)
summary(model3)
plot(model3)

model3 <- lm(avg_unit_size ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean1)
summary(model3)
plot(model3)
model3 <- lm(avg_unit_size ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean2)
summary(model3)
plot(model3)
model3 <- lm(avg_unit_size ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean3)
summary(model3)
plot(model3)
model3 <- lm(avg_unit_size ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean4)
summary(model3)
plot(model3)


model3 <- lm(avg_unit_size ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean11)
summary(model3)
plot(model3)
model3 <- lm(avg_unit_size ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean22)
summary(model3)
plot(model3)
model3 <- lm(avg_unit_size ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean33)
summary(model3)
plot(model3)
model3 <- lm(avg_unit_size ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean44)
summary(model3)
plot(model3)


# model4 <- lm(log(lines_added_per_dev+1) ~ avg_multitasking_repos_count + max_multitasking_repos_count + log_avg_total_shared_dev_commits, data = df_clean)
# summary(model4)
# plot(model4)

model4 <- lm(lines_added_per_dev ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean)
summary(model4)
plot(model4)


model4 <- lm(lines_added_per_dev ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean1)
summary(model4)
model4 <- lm(lines_added_per_dev ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean2)
summary(model4)
model4 <- lm(lines_added_per_dev ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean3)
summary(model4)
model4 <- lm(lines_added_per_dev ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean4)
summary(model4)



model4 <- lm(lines_added_per_dev ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean11)
summary(model4)
model4 <- lm(lines_added_per_dev ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean22)
summary(model4)
model4 <- lm(lines_added_per_dev ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean33)
summary(model4)
model4 <- lm(lines_added_per_dev ~ log(median_multitasking_repos_count)*log(max_multitasking_repos_count)*log(median_total_shared_dev_commits)*log(total_devs)*log(sum_s_focus), data = df_clean44)
summary(model4)


# Optionally, visualize model summaries using broom
tidy(model1)
