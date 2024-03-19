import csv

def divider(input_csv, output_csv):
    subset1 = {}
    subset2 = {}
    subset3 = {}

    with open(input_csv, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            org = row['org']
            repo = row['repo']
            complexity_str = row['avg_unit_complexity']
            
            # Skip empty strings in avg_unit_complexity
            if complexity_str == '':
                continue
            
            complexity = float(complexity_str)
            if complexity < 2:
                subset1[(org, repo)] = complexity
            elif 2 <= complexity < 5:
                subset2[(org, repo)] = complexity
            elif complexity >= 5:
                subset3[(org, repo)] = complexity

    # Find values that are unique to each range
    low_complexity_repos = set(subset1.keys()) - set(subset2.keys()) - set(subset3.keys())
    medium_complexity_repos = set(subset2.keys()) - set(subset1.keys()) - set(subset3.keys())
    high_complexity_repos = set(subset3.keys()) - set(subset1.keys()) - set(subset2.keys())

    with open(output_csv, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Org', 'Repo', 'Complexity'])
        
        writer.writerow(['Low Complexity Repos'])
        for org, repo in low_complexity_repos:
            writer.writerow([org, repo, subset1[(org, repo)]])

        writer.writerow(['Medium Complexity Repos'])
        for org, repo in medium_complexity_repos:
            writer.writerow([org, repo, subset2[(org, repo)]])

        writer.writerow(['High Complexity Repos'])
        for org, repo in high_complexity_repos:
            writer.writerow([org, repo, subset3[(org, repo)]])
        
        print("Successful conversion to file ", output_csv)
    
    
if __name__ == "__main__":
    input_csv = './read_from/final_final_rq2_data_reduced.csv'
    output_csv = './write_to/unique_complexity_repos.csv'
    divider(input_csv, output_csv)
    