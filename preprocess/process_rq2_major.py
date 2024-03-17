import pandas as pd
from datetime import datetime
import numpy as np
import ast
import csv
from tqdm import tqdm
import os
import re

def convert_and_access_key(row, key):
    try:
        # Attempt to convert the string to a dictionary if it's not already one
        dict_val = row if isinstance(row, dict) else ast.literal_eval(row)
        # Access the specified key
        return dict_val.get(key)  # Using .get() is safer as it won't raise a KeyError if the key doesn't exist
    except (ValueError, SyntaxError, TypeError):
        # In case of any error, return a placeholder (None, or you could choose an appropriate default value)
        return None

def convert_to_week(date_str):
    date_obj = datetime.strptime(date_str, "%d/%m/%Y")
    year_week = date_obj.isocalendar()[:2]

    return str(year_week)

def extract_version_parts(version):
    # Remove all non-numeric characters except for dots
    cleaned_version = re.sub(r'[^0-9.]', '', version)
    parts = cleaned_version.split('.')
    
    # Assign parts to major, minor, and bug, handling cases with missing parts
    major = parts[0] if len(parts) > 0 else 0
    minor = parts[1] if len(parts) > 1 else 0
    bug = parts[2:] if len(parts) > 2 else 0
    new_bug = []
    if type(bug) != type([]):
        bug = [bug]
    for b in bug:
        if b == '':
            pass
        else:
            new_bug.append(b)
    new_bug = [int(s) for s in new_bug]
    major = sum([int(s) for s in major])
    try:
        minor = sum([int(s) for s in minor])
    except:
        minor = sum([int(s) for s in [minor]])
    sum_bug = sum(new_bug)

    major_count = 0
    minor_count = 0
    bug_count = 0

    if sum_bug == 0:
        if minor == 0:
            major_count = 1
        else:
            minor_count = 1
    else:
        bug_count = 1
    
    return major, minor, sum_bug, major_count, minor_count, bug_count

def apply_log(value):
    return np.log2(value)

def main(org):
    df_devs = pd.read_csv('devs/combined_developer_activity.csv')
    df_devs_nodup = pd.read_csv('devs/combined_developer_nodup_activity_major_idx.csv')

    df_created = pd.read_csv('repos/selected_repos_created_week.csv')

    # org = input("Org name: ")

    df_commits = pd.read_csv(f'orgs/{org}/{org}_commits_0_bots_removed_nodup_major_idx.csv')
    df_weekly = pd.read_csv(f'orgs/{org}/{org}_weekly_nodup_major_idx.csv')
    df_weekly_devs = pd.read_csv(f'orgs/{org}/weekly_dev_activity_bots_removed_nodup_major_idx.csv')
    # df_releases = pd.read_csv(f'orgs/{org}/releases_nodup.csv')
    df_releases = pd.read_csv('release/major-major-idx.csv')

    df_devs_nodup['date'] = pd.to_datetime(df_devs_nodup['date'], utc=True)

    df_devs_nodup['new_week'] = df_devs_nodup.apply(lambda row: (row['date'].year, row['week']), axis=1)
    df_devs_nodup['new_week'] = df_devs_nodup['new_week'].apply(str)

    # df_releases_sorted = df_releases.sort_values(by=['repo_name', 'version'], ascending=[True, True])


    # df_releases_sorted['date'] = df_releases_sorted['date'].apply(convert_to_week)
    # df_releases_sorted['week'] = df_releases_sorted['date']


    # df_releases_filtered = df_releases_sorted[['repo_name', 'week', 'version']]
    # df_releases_filtered['repo'] = df_releases_filtered['repo_name']

    # df_releases_filtered['major_v'], df_releases_filtered['minor_v'], df_releases_filtered['bug_v'], df_releases_filtered['major_c'], df_releases_filtered['minor_c'], df_releases_filtered['bug_c'] = zip(*df_releases_filtered['version'].apply(extract_version_parts))
    # df_release = df_releases_filtered[['repo', 'week', 'version', 'major_c', 'minor_c', 'bug_c']]

    unique_repos = df_weekly['repo'].unique()


    headers = ['org', 'repo', 'weeks_between_major_major','total_devs', 'multitask_devs',
            'total_commits', 'multitask_commits', 'frequency_multitask_commits','avg_unit_complexity', 'avg_unit_size',
            'avg_shared_dev_commits', 'avg_total_shared_dev_commits', 'median_total_shared_dev_commits', 'lines_added', 'modified_files', 'multitask_ratio', 'avg_multitasking_repos_count', 'max_multitasking_repos_count', 'median_multitasking_repos_count', 'sum_s_focus']


    data = []

    for idx in range(1, 173):
        lines = 0
        modified_files = 0
        idx = float(idx)
        filtered_df_release = df_releases[df_releases['unique_idx'] == idx]
        
        unique_repo = filtered_df_release['repo']
        if not unique_repo.empty:
            unique_repo = unique_repo.item()
        else:
            unique_repo = None

        weeks_between_major = filtered_df_release['weeks_between_major_releases']
        if not weeks_between_major.empty:
            weeks_between_major = weeks_between_major.item()
        else:
            weeks_between_major = None
        # filtered_df_weekly_devs = df_weekly_devs[(df_weekly_devs['repo'] == unique_repo) & (df_weekly_devs['week'] ==  f"({year}, {week})")]
        # filtered_df_weekly = df_weekly[(df_weekly['repo'] == unique_repo) & (df_weekly['week'] ==  f"({year}, {week})")]
        # filtered_df_commits = df_commits[(df_commits['repo'] == unique_repo) & (df_commits['week'] ==  f"({year}, {week})")]
        filtered_df_weekly_devs = df_weekly_devs[df_weekly_devs['assigned_idx'] == idx]
        filtered_df_weekly = df_weekly[df_weekly['assigned_idx'] == idx]
        filtered_df_commits = df_commits[df_commits['assigned_idx'] == idx]



        # filtered_df_release = df_release[(df_release['repo'] == unique_repo) & (df_release['week'] ==  f"({year}, {week})")]
#             if len(filtered_df_weekly) > 0:
        unique_names = filtered_df_weekly_devs['name'].unique()
        total_devs = len(unique_names)
        total_commits = len(filtered_df_weekly_devs)
        shared_commits_df = filtered_df_weekly_devs[filtered_df_weekly_devs['shared'] == True]
        shared_commits = len(shared_commits_df)
        unique_shared_emails = shared_commits_df['name'].unique()
        shared_devs = len(unique_shared_emails)

        # created_date = df_created[df_created['repo'] == unique_repo]
        # created_date = created_date['created_week'].values[0]
        # created_year = int(''.join(created_date.split(',')[0][1:]))
        # created_week = int(''.join(created_date.split(',')[1][:-1]))
        # # print(int(year), created_year, week, created_week)
        # created_since = (int(year) - created_year - 1) * 52 + (week +  52 - created_week)


        # if len(filtered_df_weekly) > 0:
        #     avg_unit_complexity = ast.literal_eval(filtered_df_weekly['unit_complexity'].iloc[0])['avg']
        #     avg_unit_size =  ast.literal_eval(filtered_df_weekly['unit_size'].iloc[0])['avg']
        # else:
        #     avg_unit_complexity = 'NA'
        #     avg_unit_size = 'NA'

        filtered_df_shared_commits = filtered_df_commits[filtered_df_commits['name'].isin(unique_shared_emails)]
        filtered_df_weekly_shared_devs = filtered_df_weekly_devs[filtered_df_weekly_devs['name'].isin(unique_shared_emails)]
        


        # if len(filtered_df_release) > 0:
        #     release_major = filtered_df_release['major_c'].values[0]
        #     release_minor = filtered_df_release['minor_c'].values[0]
        #     release_patch = filtered_df_release['bug_c'].values[0]
        #     release_major_minor = release_major + release_minor
        #     # release = {
        #     #     'major' : release_major,
        #     #     'minor' : release_minor,
        #     #     'bug' : release_bug,
                
        #     # }
        #     release_score = release_major * 10 + release_minor * 5 + release_patch * 2
        #     # release_score = 'NA'
        # else:
        #     release_major = 0
        #     release_minor = 0
        #     release_patch = 0
        #     release_major_minor = 0
        #     # release = {
        #     #     'major' : 0,
        #     #     'minor' : 0,
        #     #     'bug' : 0,
                
        #     # }
        #     release_score = 'NA'



        # lines = filtered_df_commits['lines'].sum()
        modified_files = filtered_df_commits['n_modified_files'].sum()

        if len(filtered_df_shared_commits) > 0:
            freq_commits = 1 / (shared_commits / shared_devs)
            avg_unit_complexity = filtered_df_shared_commits['unit_complexity'].sum() / shared_devs
            avg_unit_size = filtered_df_shared_commits['unit_size'].sum() / shared_devs
            lines = filtered_df_shared_commits['lines'].sum()
        else:
            freq_commits = 'NA'
            avg_unit_complexity = 'NA'
            avg_unit_size = 'NA'
            lines = 'NA'

        if len(filtered_df_weekly_shared_devs) > 0:
            filtered_df_weekly_shared_devs['log_s_focus'] = filtered_df_weekly_shared_devs['s_focus'].apply(apply_log)
            s_focus = filtered_df_weekly_shared_devs['s_focus'] * filtered_df_weekly_shared_devs['log_s_focus']
            sum_s_focus = -1 * sum(s_focus)

        else:
            sum_s_focus = 'NA'

        if len(filtered_df_weekly_shared_devs) > 0:
            total_shared_dev_commits = filtered_df_weekly_shared_devs['outside_repo_commits'].sum() + shared_commits
            median_shared_dev_commits = np.median(filtered_df_weekly_shared_devs['outside_repo_commits']) + 1

            avg_total_shared_dev_commits = total_shared_dev_commits / shared_devs
            # avg_s_focus = filtered_df_weekly_shared_devs['s_focus'].sum() / shared_devs
        else:
            # avg_s_focus = 'NA'
            avg_total_shared_dev_commits = 'NA'
            median_shared_dev_commits = 'NA'

        multitasking_repos = {}

        shared_dev_commits = 0

        if not filtered_df_release.empty:
            # Create the 'first_release_week' string with zero-padding for week
            first_release_week = filtered_df_release.apply(lambda x: f"{x['first_release_year']}-{int(x['first_release_week']):02d}", axis=1).str.strip()
            second_release_week = filtered_df_release.apply(lambda x: f"{x['second_release_year']}-{int(x['second_release_week']):02d}", axis=1).str.strip()
            first_release_week = first_release_week.item()
            second_release_week = second_release_week.item()
        else:
            first_release_week = pd.Series(dtype='str')
            second_release_week = pd.Series(dtype='str')


        # first_release_week = f"{filtered_df_release['first_release_year']}-{filtered_df_release['first_release_week']:02d}".strip()
        # second_release_week = f"{filtered_df_release['second_release_year']}-{filtered_df_release['second_release_week']:02d}".strip()

        # print(first_release_week)
        # print(second_release_week)
        if len(filtered_df_weekly_shared_devs) > 0:
            for unique_name in unique_shared_emails:
                condition1 = df_devs_nodup['new_new_week'] > first_release_week
                condition2 = df_devs_nodup['new_new_week'] <= second_release_week
                shared_dev_commits += (filtered_df_weekly_shared_devs['name'] == unique_name).sum()
                filtered_df_devs_nodup = df_devs_nodup[(df_devs_nodup['name'] == unique_name) & condition1 & condition2]
                multitasking_repos[unique_name] = len(filtered_df_devs_nodup['repo'].unique())

            avg_shared_dev_commits = shared_dev_commits / shared_devs
        else:
            avg_shared_dev_commits = 'NA'

        for k in multitasking_repos.keys():
            if multitasking_repos[k] == 0:
                multitasking_repos[k] = 1
        
        if shared_devs > 0:
            avg_multitasking_repos = sum([v for v in multitasking_repos.values()]) / shared_devs
            max_multitasking_repos = max([v for v in multitasking_repos.values()])
            median_multitasking_repos = np.median([v for v in multitasking_repos.values()])
        else:
            avg_multitasking_repos = 'NA'
            max_multitasking_repos = 'NA'
            median_multitasking_repos = 'NA'


        if total_devs == 0:
            multitask_ratio = 'NA'
        else:
            multitask_ratio = shared_devs / total_devs


        data.append([org, unique_repo, weeks_between_major, total_devs, shared_devs, total_commits, shared_commits, freq_commits, avg_unit_complexity, avg_unit_size, avg_shared_dev_commits, avg_total_shared_dev_commits, median_shared_dev_commits, lines, modified_files, multitask_ratio, avg_multitasking_repos, max_multitasking_repos, median_multitasking_repos, sum_s_focus])


    with open(f'output/_rq2/major/{org}_processed.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow(headers)
        
        # Write data rows
        for row in data:
            writer.writerow(row)
        print(f'Process_complete: {org}_processed.csv')

if __name__ == "__main__":

    # orgs = ['artsy', 'cfpb', 'Esri', 'ExpediaGroup', 'godaddy', 'nodejs', 'proyecto26', 'RedHatOfficial', 'Yelp', 'zalando']
    orgs = os.listdir('orgs')
    # orgs = ['nodejs']
    for org in tqdm(orgs):
        main(org)