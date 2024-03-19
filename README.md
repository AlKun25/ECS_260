---
## Project direction
Open source software developers frequently choose to multitask by contributing to many repositories in a short period of time, and GitHub’s various collaborative features makes it easier than ever before. However, previous research has identified both positive and negative consequences of multitasking in software development. In this project, we look at the relationship between multitasking developers and the quality of the repositories they contribute to by measuring repository maintainability and productivity.

**Research Question 1: How does the commit contribution of multitasking developers differ from that of non-multitasking developers?**
Research regarding multitasking developers does not directly compare them to those developers who do not multitask. Our first research question comparatively studies the differences in average commits per developer to quantify repository contribution, aiming to understand the potential association between multitasking and the development quality. 

**Research Question 2: Does the level of multitasking in the repository and commit activity associate with repository maintainability and productivity, controlling for other factors?**
Existing research on multitasking developers often treats all developers uniformly, overlooking personal traits. Our second research question investigates whether certain characteristics, such as developer level of multitasking and commit activity, are correlated with repository effectiveness, or specifically, maintainability and productivity

## Running instruction  
1. First, clone this repo
```bash
# clone project   
git clone https://github.com/AlKun25/ECS_260

2. Install the relevant project dependencies
```bash
cd ECS_260 
pip install -e .   
pip install -r requirements.txt
```
3. Please download the mining data for the organizations from : [Link to Drive](https://drive.google.com/drive/folders/1AH4hb1xKbMWxM76SaWQomqGC1tAPczmI?usp=sharing).<br>
Place these organization folders in `/project/db/orgs`.

4. Next, run main.py in the same directory.   
 ```bash
# run module  
python main.py    
```
 
## Methodology  
How variables are measured and defined to study the [research questions](https://github.com/AlKun25/ECS_260/blob/master/README.md#research-questions).  

### Data Collection
Repositories obtained from various GitHub organizations that fit the following requirements
1. Contains a release before 01/01/2022
2. At least 100 stars
3. Has a commit in the last 2 years
4. Most recent commit made within the last 3 months
- Repository Metrics - repo, org, stars, contributors, commits, released, created_at, updated_recently, url

All metrics on commits made to the repository during the observational period 01/01/2022 to 12/31/2023 are gathered, and are analyied weekly. Repository release information is also obtained.
- Commit Metrics - id, repo, org, name, email, year, month, day, week, unit_complexity, unit_size, lines, n_modified_files
- Release Metrics -id, date, version, repo_name

The commits are then analyzed on a weekly level. All GitHub users who created one of the gathered commits is considered as a developer. They are categorized into multitasking or non-multitasking developers, and additional metrics are gathered on multitasking developers.

> NOTE : n_shared corresponds to number of multitasking developers

- Weekly Commit Metrics - repo, org, week, unit_complexity, unit_size, lines, n_modified_files, total_contributors, n_shared, n_commits
- All Developer Metrics - name, username, repo, org, date, week, email, etag
- Multitasking Developer Metrics - name, emails, p_i, repo, outside_repo_commits, within_org_commits, shared, week

### Research Question 1
Independent Variable: proportion of multitasking developers (n_shared/total_contributors)
Dependent Variables: LOCAdded/developer, unit complexity, unit size
Methods: linear regression, T-tests

### Research Question 2
Independent Variables: average level of multitasking, max level of multitasking, average commits, total developers, commit activity (proportion of focus)
Dependent Variables: LOCAdded, average  unit complexity, average unit size, number of releases, frequency of commits, average LOCAdded per developer
Methods: mixed-methods explanatory sequential design, 1) multiple variable linear regression 2) case study

## Project Structure
<details open>
<summary>This section provides details into specific important files in the project</summary>

```bash
.
├── project/
│   ├── db/
│   │   ├── devs/
│   │   │   ├── developer_activity_0.csv 
│   │   │   ├── developer_activity_1.csv
│   │   │   └── ...
│   │   ├── orgs/
│   │   │   ├── RedHatOfficial/
│   │   │   │   ├── RedHatOfficial_commits_0.csv
│   │   │   │   ├── RedHatOfficial_commits_1.csv
│   │   │   │   ├── ...
│   │   │   │   ├── RedHatOfficial_weekly.csv
│   │   │   │   ├── releases.csv
│   │   │   │   └── weekly_dev_activity.csv
│   │   │   └── nodejs/
│   │   │       ├── nodejs_commits_0.csv
│   │   │       ├── ...
│   │   │       ├── nodejs_weekly.csv
│   │   │       ├── releases.csv
│   │   │       └── weekly_dev_activity.csv
│   │   ├── org_list.csv
│   │   └── selected_repos.csv
│   ├── logs
│   ├── repo_holder
│   ├── constants.py
│   ├── utils.py
│   ├── selector.py
│   ├── repo.py
│   ├── developer.py
│   └── ...
└── main.py
```

#### Data collection
- `/project/db/orgs/`: This directories holds folders, containing all the mined data, from each organization. We use the NodeJS organization, as an example, to explain the folder structure for each organization.
  - `orgs/nodejs/nodejs/nodejs_commits_0.csv`: It contains all the commits made to the specific organization within our observation period from Jan 2022 to Dec 2023.
  - `orgs/nodejs/nodejs/nodejs_weekly.csv`: It contains a summary of the weekly git activity of a specific repos.
  - `orgs/nodejs/nodejs/weekly_dev_activity.csv`: It contains all the relevant details about the developer activity within the observed repos
  - `orgs/nodejs/nodejs/releases.csv`: It contains all the releases that occured for all observed repos during the observation period
- `/project/db/devs/developer_activity_0.csv`: This kind of file will contain all the outside repo commits made by developers from all organizations under observation.
- `project/db/org_list.csv`: This stores the list of GitHub organization that we had initially decided to study
- `project/db/selected_repos.csv`: This stores the relevant repos from each organization that can be used based on our criteria.

#### Mining code
- `/project/repo.py`: It contains the code for downloading commits of a specific repo(using pyDriller) and for metric retrieval using the downloaded commits(using pyGitHub and pyDriller)
- `/project/selector.py`: It selects the relevant repos from each organization, and save that list in `selected_repos.csv`
- `/project/developer.py`: It handles the logic for calculating the metric involving developer's outside repo activity like S_FOCUS.
- `/project/utils.py`: It stores functions that are repeatedly used, across the codebase. This includes checking rate limit for the GitHub API token, adding/appending to the specific CSVs, and more ...
- `/project/constants.py`: It stores the constant values that are used across the codebase frequently. 

#### Misc.
- `/project/logs`: This stores the logs of the given run of mining data
- `/project/repo_holder`: This directory stores the cloned repository during the commit downloading phase of mining

</details>

## Team details
We are team 16, also known as  "Ottoke"

Everyone in the team has tried to participate in all parts of the process, the following is the list of the members and their main contributions:
- Amy Vu: Reports, Mining repos
- Andrew Lee: Data Analysis
- Dieu Anh Le: Everything, Driver for this project
- Dong Hee Lee: Data Analysis
- Kunal Mundada: Code for Git Activity Mining, Mining repos

### Citation   
```
@article{YourName,
  title={From Collaboration to Code: The Association between Multitasking Developers and GitHub Repositories Effectiveness},
  author={Amy Vu, Andrew Lee, Dieu Anh Le, Donghee Lee, Kunal Mundada},
  journal={---},
  year={2024}
}
```   
