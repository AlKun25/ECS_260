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


df1 <- read.csv('final_final_rq1_data_reduced.csv', header=T)
df1$lines_added <- df1$total_lines_added
df1$lines_added_per_dev <- df1$lines_added / df1$total_devs
# df_subset <- df[c("multitask_ratio", "avg_total_unit_complexity", "avg_total_unit_size")]
df_subset <- df1[c("multitask_ratio", "avg_total_unit_complexity", "avg_total_unit_size", "lines_added_per_dev", "total_devs", "lines_added")]
df_subset <- subset(df_subset, avg_total_unit_complexity>0 & avg_total_unit_size>0) # 3970

summary(df_subset)

plot1 <- df_subset %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=multitask_ratio)) +
  theme_minimal() +
  ggtitle("Multitasking ratio(X) Distribution")

plot2 <- df_subset %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=avg_total_unit_complexity)) +
  theme_minimal() +
  ggtitle("Unit complexity (Y1) Distribution")

plot3 <- df_subset %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=avg_total_unit_size)) +
  theme_minimal() +
  ggtitle("Unit size (Y2) Distribution")

plot4 <- df_subset %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=lines_added_per_dev)) +
  theme_minimal() +
  ggtitle("LOCAdded per dev (Y3) Distribution")

plot5 <- df_subset %>% 
  ggplot() +
  geom_histogram(mapping=aes(x=total_lines_added)) +
  theme_minimal() +
  ggtitle("LOCAdded (Y4) Distribution")

grid.arrange(plot1, plot2, plot3, plot4, plot5, ncol = 3)



std_devs <- sapply(df_subset, sd)
print(std_devs)







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
  mutate_at(vars(multitask_ratio, lines_added), remove_outliers) %>%
  na.omit()
# 3970 -> 3136 # 3367

std <- sapply(df_clean, sd)
print(std)


summary(df_clean)

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


plot1 <- ggplot(df_clean, aes(x=multitask_ratio, y=avg_total_unit_complexity)) +
  geom_point() +
  theme_minimal() +
  ggtitle("Multitask Ratio vs Unit Complexity")

plot2 <- ggplot(df_clean, aes(x=multitask_ratio, y=avg_total_unit_size)) +
  geom_point() +
  theme_minimal() +
  ggtitle("Multitask Ratio vs Unit Size")

plot3 <- ggplot(df_clean, aes(x=multitask_ratio, y=lines_added_per_dev)) +
  geom_point() +
  theme_minimal() +
  ggtitle("Multitask Ratio vs LOCAdded per Dev")

plot4 <- ggplot(df_clean, aes(x=multitask_ratio, y=total_lines_added)) +
  geom_point() +
  theme_minimal() +
  ggtitle("Multitask Ratio vs LOCAdded")

# Combining the plots into a single figure
grid.arrange(plot1, plot2, plot3, ncol = 1)




# df_long <- df_clean %>%
#   gather(key = "independent_variable", value = "independent_value", multitask_ratio) %>%
#   gather(key = "dependent_variable", value = "dependent_value", avg_total_unit_complexity, avg_total_unit_size, log_lines_added_per_dev)

# # Plotting with facets
# ggplot(df_long, aes(x = independent_value, y = dependent_value)) +
#   geom_point(alpha = 0.5) +
#   # geom_smooth(method = lm, se = FALSE, color = "red") +
#   facet_grid(dependent_variable ~ independent_variable, scales = "free", labeller = label_both) +
#   labs(title = "Scatter plots of all X and Y combinations", x = "Multitask Ratio", y = "Dependent Variable Value") +
#   theme_bw() +
#   theme(strip.text.x = element_text(size = 10, angle = 45),
#         strip.text.y = element_text(size = 10))
# 
# # Step 3: Scatter plot for each X and Y (Example for one Y, repeat for others)
# ggplot(df_clean, aes(x = multitask_ratio, y = log_lines_added_per_dev)) +
#   geom_point(alpha = 0.5) +
#   labs(title = "Scatter plot of Multitasking ratio VS LOC per dev", x = "Multitasking ratio", y = "LOC per dev")


# df_subset <- subset(df_subset, avg_total_unit_complexity>0 & avg_total_unit_size>0) # 3970

df_clean$has_multitask_dev <- df_clean$multitask_ratio>0



df_0 <- subset(df_clean, multitask_ratio==0)
df_1 <- subset(df_clean, multitask_ratio>0 & multitask_ratio<0.5)
df_2 <- subset(df_clean, multitask_ratio>=0.5 & multitask_ratio<1)
df_3 <- subset(df_clean, multitask_ratio==1)

df_clean0 <- subset(df_clean, multitask_ratio<0.5)
df_clean1 <- subset(df_clean, multitask_ratio==0 | (multitask_ratio>=0.5 & multitask_ratio<1))
df_clean2 <- subset(df_clean, multitask_ratio==0 | multitask_ratio==1)





# Box-plot & T-test

boxplot(avg_total_unit_size~has_multitask_dev,data=df_clean)
boxplot(avg_total_unit_complexity~has_multitask_dev,data=df_clean)
boxplot(lines_added_per_dev~has_multitask_dev,data=df_clean)


# Create the boxplots, each as a separate plot object
plot1 <- ggplot(df_clean, aes(x=has_multitask_dev, y=avg_total_unit_size)) +
  geom_boxplot() +
  theme_minimal() +
  ggtitle("Boxplot of Unit Size by Multitask Dev Status")

plot2 <- ggplot(df_clean, aes(x=has_multitask_dev, y=avg_total_unit_complexity)) +
  geom_boxplot() +
  theme_minimal() +
  ggtitle("Boxplot of Unit Complexity by Multitask Dev Status")

plot3 <- ggplot(df_clean, aes(x=has_multitask_dev, y=lines_added_per_dev)) +
  geom_boxplot() +
  theme_minimal() +
  ggtitle("Boxplot of LOC per Dev by Multitask Dev Status")

# Combine the plots into one figure





# Create the boxplots, each as a separate plot object
plot1 <- ggplot(df_clean0, aes(x=has_multitask_dev, y=avg_total_unit_size)) +
  geom_boxplot() +
  theme_minimal() +
  ggtitle("Boxplot of Unit Size by Multitask Dev Status")

plot2 <- ggplot(df_clean0, aes(x=has_multitask_dev, y=avg_total_unit_complexity)) +
  geom_boxplot() +
  theme_minimal() +
  ggtitle("Boxplot of Unit Complexity by Multitask Dev Status")

plot3 <- ggplot(df_clean0, aes(x=has_multitask_dev, y=lines_added_per_dev)) +
  geom_boxplot() +
  theme_minimal() +
  ggtitle("Boxplot of LOC per Dev by Multitask Dev Status")

# Combine the plots into one figure
grid.arrange(plot1, plot2, plot3, ncol = 1)



# Create the boxplots, each as a separate plot object
plot1 <- ggplot(df_clean1, aes(x=has_multitask_dev, y=avg_total_unit_size)) +
  geom_boxplot() +
  theme_minimal() +
  ggtitle("Boxplot of Unit Size by Multitask Dev Status")

plot2 <- ggplot(df_clean1, aes(x=has_multitask_dev, y=avg_total_unit_complexity)) +
  geom_boxplot() +
  theme_minimal() +
  ggtitle("Boxplot of Unit Complexity by Multitask Dev Status")

plot3 <- ggplot(df_clean1, aes(x=has_multitask_dev, y=lines_added_per_dev)) +
  geom_boxplot() +
  theme_minimal() +
  ggtitle("Boxplot of LOC per Dev by Multitask Dev Status")

# Combine the plots into one figure
grid.arrange(plot1, plot2, plot3, ncol = 1)


# Create the boxplots, each as a separate plot object
plot1 <- ggplot(df_clean2, aes(x=has_multitask_dev, y=avg_total_unit_size)) +
  geom_boxplot() +
  theme_minimal() +
  ggtitle("Boxplot of Unit Size by Multitask Dev Status")

plot2 <- ggplot(df_clean2, aes(x=has_multitask_dev, y=avg_total_unit_complexity)) +
  geom_boxplot() +
  theme_minimal() +
  ggtitle("Boxplot of Unit Complexity by Multitask Dev Status")

plot3 <- ggplot(df_clean2, aes(x=has_multitask_dev, y=lines_added_per_dev)) +
  geom_boxplot() +
  theme_minimal() +
  ggtitle("Boxplot of LOC per Dev by Multitask Dev Status")

# Combine the plots into one figure
grid.arrange(plot1, plot2, plot3, ncol = 1)

# shared_repo <- dataset %>%
#   filter(has_shared_dev==TRUE)
# non_shared_repo <- dataset %>%
#   filter(has_shared_dev==FALSE)
# summary(shared_repo$avg_commit_per_dev)
# summary(non_shared_repo$avg_commit_per_dev)

# t-test


t.test(avg_total_unit_size~has_multitask_dev, data=df_clean) 
t.test(avg_total_unit_complexity~has_multitask_dev, data=df_clean)
t.test(lines_added_per_dev~has_multitask_dev, data=df_clean)



t.test(avg_total_unit_size~has_multitask_dev, data=df_clean0) 
t.test(avg_total_unit_complexity~has_multitask_dev, data=df_clean0)
t.test(lines_added_per_dev~has_multitask_dev, data=df_clean0)

t.test(avg_total_unit_size~has_multitask_dev, data=df_clean1) 
t.test(avg_total_unit_complexity~has_multitask_dev, data=df_clean1)
t.test(lines_added_per_dev~has_multitask_dev, data=df_clean1)

t.test(avg_total_unit_size~has_multitask_dev, data=df_clean2) 
t.test(avg_total_unit_complexity~has_multitask_dev, data=df_clean2)
t.test(lines_added_per_dev~has_multitask_dev, data=df_clean2)


# separate multitask_ratio=0,1 / 0<multitask<1
# multitasking01_df <- subset(df_clean, multitask_ratio==0 | multitask_ratio==1) # 5426
# multitasking_middle_df <- subset(df_clean, multitask_ratio <1 & multitask_ratio>0) # 1473
# 
# 
# boxplot(avg_total_unit_size~multitask_ratio,data=multitasking01_df)
# boxplot(avg_total_unit_complexity~multitask_ratio,data=multitasking01_df)
# boxplot(lines_added_per_dev~multitask_ratio,data=multitasking01_df)
# 
# t.test(avg_total_unit_size~multitask_ratio, data=multitasking01_df)
# t.test(avg_total_unit_complexity~multitask_ratio, data=multitasking01_df)
# t.test(lines_added_per_dev~multitask_ratio, data=multitasking01_df)
# 
# 
# df_valid_DMM <- subset(df_clean, avg_total_unit_complexity>0 & avg_total_unit_size>0) # 2693
# df_valid_DMM$has_multitask_dev <- df_valid_DMM$multitask_ratio>0
# df_valid_DMM$log_lines_added_per_dev <- log(df_valid_DMM$lines_added_per_dev)
# 
# boxplot(avg_total_unit_size~multitask_ratio,data=multitasking_middle_valid_DMM)
# boxplot(avg_total_unit_complexity~multitask_ratio,data=multitasking_middle_valid_DMM)
# boxplot(lines_added_per_dev~multitask_ratio,data=multitasking_middle_valid_DMM)
# 
# t.test(avg_total_unit_size~has_multitask_dev, data=df_valid_DMM)
# t.test(avg_total_unit_complexity~has_multitask_dev, data=df_valid_DMM)
# t.test(lines_added_per_dev~has_multitask_dev, data=df_valid_DMM)





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
