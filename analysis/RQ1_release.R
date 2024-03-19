# Load necessary libraries
library(tidyverse)  # For data manipulation and visualization
library(broom)      # For tidying up model outputs
library(dplyr)
install.packages("gridExtra")
library(ggplot2)
library(gridExtra)

# Step 1: Preliminary Cleaning
# X: multitask_ratio
# Y: avg_total_unit_complexity, avg_total_unit_size, lines_added_per_dev


df1_r_major <- read.csv('release_major_rq1_data_reduced.csv', header=T)
df1_r_minor <- read.csv('release_minor_rq1_data_reduced.csv', header=T)

# df_subset <- df[c("multitask_ratio", "avg_total_unit_complexity", "avg_total_unit_size")]

df1_r_major$major_release <- df1_r_major$weeks_between_major_major
df1_r_minor$minor_release <- df1_r_minor$weeks_between_minor_minor

df_subset1 <- df1_r_major[c("multitask_ratio", "major_release")]
df_subset2 <- df1_r_minor[c("multitask_ratio", "minor_release")]

count(df_subset1) # 90
count(df_subset2) # 786




df_subset1 %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=multitask_ratio)) +
  theme_minimal() +
  ggtitle("Multitasking ratio(X) (major) Distribution")


df_subset2 %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=multitask_ratio)) +
  theme_minimal() +
  ggtitle("Multitasking ratio(X) (minor) Distribution")



summary(df_subset1)

plot1 <- df_subset1 %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=multitask_ratio)) +
  theme_minimal() +
  ggtitle("Multitasking ratio(X) Distribution")

plot2 <- df_subset1 %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=major_release)) +
  theme_minimal() +
  ggtitle("Time between major releases (week) (Y1) Distribution")


grid.arrange(plot1, plot2, ncol = 2)

std_devs <- sapply(df_subset1, sd)
print(std_devs)


summary(df_subset2)

plot1 <- df_subset2 %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=multitask_ratio)) +
  theme_minimal() +
  ggtitle("Multitasking ratio(X) Distribution")

plot2 <- df_subset2 %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=minor_release)) +
  theme_minimal() +
  ggtitle("Time between minor releases (week) (Y1) Distribution")


grid.arrange(plot1, plot2, ncol = 2)

std_devs <- sapply(df_subset2, sd)
print(std_devs)









df_clean <- na.omit(df_subset)


df_clean1 <- na.omit(df_subset1)
df_clean2 <- na.omit(df_subset2)

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
  mutate_at(vars(multitask_ratio), remove_outliers) %>%
  na.omit()
# 3970 -> 3136 # 3367


df_clean1 <- df_clean1 %>%
  mutate_at(vars(multitask_ratio), remove_outliers) %>%
  na.omit()

df_clean2 <- df_clean2 %>%
  mutate_at(vars(multitask_ratio), remove_outliers) %>%
  na.omit()


summary(df_clean)

count(df_clean1) # no outlier # 90
count(df_clean2) # no outlier # 786

plot1 <- df_clean %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=multitask_ratio)) +
  theme_minimal() +
  ggtitle("Multitasking ratio(X) Distribution")

plot2 <- df_clean %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=avg_total_unit_complexity)) +
  theme_minimal() +
  ggtitle("Unit complexity (Y1) Distribution")

plot3 <- df_clean %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=avg_total_unit_size)) +
  theme_minimal() +
  ggtitle("Unit size (Y2) Distribution")

plot4 <- df_clean %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=lines_added_per_dev)) +
  theme_minimal() +
  ggtitle("LOCAdded per dev (Y3) Distribution")

plot5 <- df_clean %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=lines_added)) +
  theme_minimal() +
  ggtitle("LOCAdded (Y4) Distribution")

grid.arrange(plot1, plot2, plot3, plot4, ncol = 2)


# take log
# df_clean$log_lines_added_per_dev <- log(df_clean$lines_added_per_dev+1)


ggplot(df_clean1, aes(x=multitask_ratio, y=major_release)) +
  geom_point() +
  theme_minimal() +
  ggtitle("Multitask Ratio vs Time between Major releases")

ggplot(df_clean2, aes(x=multitask_ratio, y=minor_release)) +
  geom_point() +
  theme_minimal() +
  ggtitle("Multitask Ratio vs Time between Minor releases")





df_clean1$has_multitask_dev <- df_clean1$multitask_ratio>0
df_clean2$has_multitask_dev <- df_clean2$multitask_ratio>0






df_clean11 <- subset(df_clean1, multitask_ratio<0.5)
df_clean12 <- subset(df_clean1, multitask_ratio==0 | (multitask_ratio>=0.5 & multitask_ratio<1))
df_clean13 <- subset(df_clean1, multitask_ratio==0 | multitask_ratio==1)


df_clean21 <- subset(df_clean2, multitask_ratio<0.5)
df_clean22 <- subset(df_clean2, multitask_ratio==0 | (multitask_ratio>=0.5 & multitask_ratio<1))
df_clean23 <- subset(df_clean2, multitask_ratio==0 | multitask_ratio==1)





# Box-plot & T-test

boxplot(major_release~has_multitask_dev,data=df_clean1)
boxplot(minor_release~has_multitask_dev,data=df_clean2)



boxplot(major_release~has_multitask_dev,data=df_clean11)
boxplot(major_release~has_multitask_dev,data=df_clean12)
boxplot(major_release~has_multitask_dev,data=df_clean13)


library(ggplot2)

# Assuming df_clean1, df_clean11, df_clean12, and df_clean13 are already defined

# Add a new 'group' column to identify the groups
df_clean1$group <- ifelse(df_clean1$has_multitask_dev, "Group 1", "Group 0")
df_clean11$group <- "Group 2"
df_clean12$group <- "Group 3"
df_clean13$group <- "Group 4"

# Combine the dataframes
combined_df <- rbind(df_clean1, df_clean11, df_clean12, df_clean13)

ggplot(combined_df, aes(x = factor(group, levels = c("Group 0", "Group 1", "Group 2", "Group 3", "Group 4")), y = major_release, fill = group)) +
  geom_boxplot() +
  scale_fill_manual(values = c(
    "Group 0" = "#a6cee3", # soft blue
    "Group 1" = "#fdbf6f", # soft orange
    "Group 2" = "#b2df8a", # soft green
    "Group 3" = "#fb9a99", # soft pink
    "Group 4" = "#cab2d6"  # soft purple
  )) +
  labs(x = "Multitasking Developer Ratio", y = "Major Release") +
  theme_minimal() +
  theme(legend.title = element_blank()) # Remove the legend title






plot1 <- ggplot(df_clean11, aes(x=has_multitask_dev, y=major_release)) +
  geom_boxplot() +
  theme_minimal() +
  ggtitle("Group 1 vs 2 Boxplot of Major release by Multitask Dev Status")

plot2 <- ggplot(df_clean12, aes(x=has_multitask_dev, y=major_release)) +
  geom_boxplot() +
  theme_minimal() +
  ggtitle("Group 1 vs 3 Boxplot of Major release by Multitask Dev Status")

plot3 <- ggplot(df_clean13, aes(x=has_multitask_dev, y=major_release)) +
  geom_boxplot() +
  theme_minimal() +
  ggtitle("Group 1 vs 4 Boxplot of Major release by Multitask Dev Status")


grid.arrange(plot1, plot2, plot3, ncol = 3)


boxplot(minor_release~has_multitask_dev,data=df_clean21)
boxplot(minor_release~has_multitask_dev,data=df_clean22)
boxplot(minor_release~has_multitask_dev,data=df_clean23)


# t-test


t.test(major_release~has_multitask_dev, data=df_clean1) 
t.test(major_release~has_multitask_dev, data=df_clean11) 
t.test(major_release~has_multitask_dev, data=df_clean12) 
t.test(major_release~has_multitask_dev, data=df_clean13)


t.test(minor_release~has_multitask_dev, data=df_clean2) 
t.test(minor_release~has_multitask_dev, data=df_clean21) 
t.test(minor_release~has_multitask_dev, data=df_clean22) 
t.test(minor_release~has_multitask_dev, data=df_clean23)









df_clean$log_total_devs <- log(df_clean$total_devs)

# Step 4: Correlation Matrix
cor_matrix <- cor(df_clean[, c("multitask_ratio", "avg_total_unit_complexity", "avg_total_unit_size", "lines_added_per_dev")], use = "complete.obs")
print(cor_matrix)
corrplot(cor_matrix, type='upper', title = "Correlation Matrix")


# cor_matrix <- cor(multitasking_middle_df[, c("multitask_ratio", "avg_total_unit_complexity", "avg_total_unit_size", "log_lines_added_per_dev")], use = "complete.obs")
# print(cor_matrix)
# corrplot(cor_matrix, type='upper', title = "Correlation Matrix")



# cor_matrix <- cor(multitasking_middle_valid_DMM[, c("multitask_ratio", "avg_total_unit_complexity", "avg_total_unit_size", "log_lines_added_per_dev")], use = "complete.obs")
# print(cor_matrix)
# corrplot(cor_matrix, type='upper', title = "Correlation Matrix")


# cor_matrix <- cor(df_valid_DMM[, c("multitask_ratio", "avg_total_unit_complexity", "avg_total_unit_size", "log_lines_added_per_dev")], use = "complete.obs")
# print(cor_matrix)
# corrplot(cor_matrix, type='upper', title = "Correlation Matrix")







# Step 5: Fit Linear Regression (Example for one Y, repeat for others)
model1 <- lm(avg_total_unit_complexity ~ multitask_ratio, data = df_clean)
summary(model1)
plot(model1)

# 
model1 <- lm(avg_total_unit_complexity ~ multitask_ratio, data = df_1)
summary(model1)
model1 <- lm(avg_total_unit_complexity ~ multitask_ratio, data = df_2)
summary(model1)





# 
model2 <- lm(avg_total_unit_size ~ multitask_ratio, data = df_clean)
summary(model2)

model2 <- lm(avg_total_unit_size ~ multitask_ratio, data = df_1)
summary(model2)

model2 <- lm(avg_total_unit_size ~ multitask_ratio, data = df_2)
summary(model2)
# 
# plot(model2)




model3 <- lm(lines_added_per_dev ~ multitask_ratio, data = df_clean)
summary(model3)
plot(model3)


model3 <- lm(lines_added_per_dev ~ multitask_ratio, data = df_1)
summary(model3)

model3 <- lm(lines_added_per_dev ~ multitask_ratio, data = df_2)
summary(model3)



# 
# model4 <- lm(avg_total_unit_complexity ~ multitask_ratio, data = multitasking_middle_df)
# summary(model4)
# plot(model4)
# 
# model5 <- lm(avg_total_unit_size ~ multitask_ratio, data = multitasking_middle_df)
# summary(model5)
# plot(model5)
# 
# model6 <- lm(log_lines_added_per_dev ~ multitask_ratio, data = multitasking_middle_df)
# summary(model6)
# plot(model6)
# 
# 
# 
# model7 <- lm(avg_total_unit_complexity ~ multitask_ratio, data = multitasking_middle_valid_DMM)
# summary(model7)
# plot(model7)
# 
# model8 <- lm(avg_total_unit_size ~ multitask_ratio, data = multitasking_middle_valid_DMM)
# summary(model8)
# plot(model8)
# 
# model9 <- lm(log_lines_added_per_dev ~ multitask_ratio, data = multitasking_middle_valid_DMM)
# summary(model9)
# plot(model9)
# 
# 
# 
# 
# 
# model10 <- lm(avg_total_unit_complexity ~ multitask_ratio, data = df_valid_DMM)
# summary(model10)
# plot(model10)
# 
# model11 <- lm(avg_total_unit_size ~ multitask_ratio, data = df_valid_DMM)
# summary(model11)
# plot(model11)
# 
# model12 <- lm(log_lines_added_per_dev ~ multitask_ratio, data = df_valid_DMM)
# summary(model12)
# plot(model12)





# model4 <- lm(lines_added_per_dev ~ multitask_ratio, data = df_clean)
# summary(model4)
# plot(model4)

# take log # not effective
# model3 <- lm(log(avg_total_unit_complexity+1) ~ multitask_ratio, data = df_clean)
# summary(model3)
# plot(model3)
# 
# model4 <- lm(log(avg_total_unit_size+1) ~ multitask_ratio, data = df_clean)
# summary(model4)
# plot(model3)


# Optionally, visualize model summaries using broom
tidy(model1)
