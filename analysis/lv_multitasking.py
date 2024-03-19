import csv
import os
from datetime import datetime

# def list_repos_for_each_name(csv_file, output_file):
#     name_week_repos = {}  # Dictionary to store repositories for each name and each week

#     with open(csv_file, 'r', newline='', encoding='utf-8') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             name = row['name']
#             repo = row['repo']
#             date = row['date']
#             week = row['week']
            
#             if 'bot' in name.lower():
#                 continue
#             # Initialize inner dictionary for the name if not already present
#             if name not in name_week_repos:
#                 name_week_repos[name] = {}
            
#             # Initialize set for the week if not already present
#             if week not in name_week_repos[name]:
#                 name_week_repos[name][week] = set()
            
#             # Add the repository to the set for the name and week
#             name_week_repos[name][week].add(repo)

#     # Write the names, counts of unique repositories, and their respective repositories to the output CSV file
#     with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
#         writer = csv.writer(outfile)
#         writer.writerow(['name', 'week', 'repo_count', 'unique_repo', 'date'])  # Write header
#         for name, week_data in name_week_repos.items():
#             for week, repos in week_data.items():
#                 unique_repo_count = len(repos)
#                 writer.writerow([
#                     name, 
#                     week, 
#                     int(unique_repo_count), 
#                     ', '.join(repos),
#                     date,
#                 ])

#     return name_week_repos

def list_repos_for_each_name(csv_file, output_file):
    name_week_repos = {}  # Dictionary to store repositories for each name and each week

    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['name']
            username = row['username']
            repo = row['repo']
            date = row['date']
            week = row['week']

            # Extract year from the date
            year = datetime.strptime(date, '%Y-%m-%d %H:%M:%S%z').year
            
            if 'bot' in name.lower():
                continue
            # Initialize inner dictionary for the name if not already present
            if name not in name_week_repos:
                name_week_repos[name] = {}
            
            # Initialize set for the week if not already present
            if week not in name_week_repos[name]:
                name_week_repos[name][week] = {'repos': set(), 'year': year, 'username': set()}
            
            # Add the repository to the set for the name and week
            name_week_repos[name][week]['repos'].add(repo)
            name_week_repos[name][week]['username'].add(username)

    # Write the names, counts of unique repositories, and their respective repositories to the output CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['name', 'username', 'week', 'year', 'repo_count', 'unique_repo'])  # Write header
        for name, week_data in name_week_repos.items():
            for week, week_info in week_data.items():
                unique_repo_count = len(week_info['repos'])
                writer.writerow([
                    name, 
                    username,
                    week, 
                    week_info['year'],
                    int(unique_repo_count), 
                    ', '.join(week_info['repos']),
                ])

    return name_week_repos

if __name__ == "__main__":
    csv_file = './combined_developer_nodup_activity.csv'
    output_file = './case_study_dev_3.csv'  # Path to the output CSV file
    list_repos_for_each_name(csv_file, output_file)
    print("Unique repositories listed for each name and each week and written to", output_file)
