---
## Project direction
Influence of shared developers on project effectiveness. 


## Research questions

<UNDER DEBATE & SCRUTINY BY HIGHER AUTHORITIES>
 
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

## Project Structure
<details>
<summary>This section provides details into specific important files in the project</summary>

```bash
.
├── project/
│   ├── db/
│   │   ├── devs/
│   │   │   ├── developer_activity_0.parquet 
│   │   │   ├── developer_activity_1.parquet
│   │   │   └── ...
│   │   ├── orgs/
│   │   │   ├── RedHatOfficial/
│   │   │   │   ├── RedHatOfficial_commits_0.parquet
│   │   │   │   ├── RedHatOfficial_commits_1.parquet
│   │   │   │   ├── ...
│   │   │   │   ├── RedHatOfficial_weekly.parquet
│   │   │   │   ├── releases.parquet
│   │   │   │   └── weekly_dev_activity.parquet
│   │   │   └── nodejs/
│   │   │       ├── nodejs_commits_0.parquet
│   │   │       ├── ...
│   │   │       ├── nodejs_weekly.parquet
│   │   │       ├── releases.parquet
│   │   │       └── weekly_dev_activity.parquet
│   │   ├── org_list.csv
│   │   └── selected_repos.parquet
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
We are team 16, also known as  "PublishOrPerish"

- Amy Vu
- Andrew Lee
- Dieu Anh Le
- Dong Hee Lee
- Kunal Mundada

### Citation   
```
@article{YourName,
  title={Your Title},
  author={Amy Vu, Andrew Lee, Dieu Anh Le, Donghee Lee, Kunal Mundada},
  journal={Location},
  year={Year}
}
```   
