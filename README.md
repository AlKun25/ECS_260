---
## Project direction
Influence of shared developers on project effectiveness. 


## Research questions

1. How does the commit contribution of multitasking developers differ from that of non-multitasking developers?
2. Does the level of multitasking in the project and commit activity associate with project maintainability and productivity, controlling for other factors?

## How to run   
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
How it measure and defines stuff to study the [research questions](https://github.com/AlKun25/ECS_260/blob/master/README.md#research-questions) .  

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
