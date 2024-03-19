data = read.csv("C:/Users/Anh Le/Desktop/ECS_260_v5/analysis/case_study_dev_3.csv", row.names=NULL)
# print(head(data))
# print(class(data$repo_count))
count_summary = summary(data$repo_count)
print(count_summary)
Q1 = count_summary[2]
Q3 = count_summary[5]
IQR = Q3-Q1
lower_bound = 1
upper_bound = Q3 + 1.5*IQR
cleaned_data <- data[data$repo_count > lower_bound & data$repo_count <= upper_bound, ]

summary(cleaned_data$repo_count)
hist(
    cleaned_data$repo_count,
    breaks = 10,
    main = "Histogram of frequency of count", 
    xlab = "Level of multitasking", 
    ylab = "Frequency"
)
