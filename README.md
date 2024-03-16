---
## Project direction
Influence of shared developers on project effectiveness. 


## Research questions

1. How does the commit contribution of multitasking developers differ from that of non-multitasking developers?
2. Does the level of multitasking in the project and commit activity associate with project maintainability and productivity, controlling for other factors?

 
## Methodology  
How it measure and defines stuff to study the [research questions](https://github.com/AlKun25/ECS_260/blob/master/README.md#research-questions) .  

## How to run   
First, install dependencies   
```bash
# clone project   
git clone https://github.com/AlKun25/ECS_260

# install project   
```bash
cd ECS_260 
pip install -e .   
pip install -r requirements.txt
```   
Next, run main.py in the same directory.   
 ```bash
# run module  
python main.py    
```

Please download the mining data for the organizations from : [Link to Drive](https://drive.google.com/drive/folders/1AH4hb1xKbMWxM76SaWQomqGC1tAPczmI?usp=sharing).<br>
Place these organization folders in `/project/db/orgs`

## Project Structure
<details>
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

</details>

## Team details
We are team 16, also known as  ""

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
