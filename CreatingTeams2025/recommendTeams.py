import pandas as pd
from dotenv import load_dotenv
import json
import os
import numpy as np
# from openai import OpenAI
from config import FILE_NAME, HIRING_FILE_NAME, RECOMMEND_MEMBERS_EMAIl, CLOSER, FOLLOW_UP, TEAM_FOLLOW_UP
import chardet
load_dotenv()

"""
Plan of attack:
1. Look at list of skills in a team
2. Compare the skills to ideal skills (ui design, coding experience, subject expert)
3. Recommend qualified individuals
"""

TESTERS = ["Minseo Kim", "Zachary Walnock", "Ethan Sullivan"]
#defining skills we want to ensure are in each team
desirable_tech_skills = ["Amazon Web Services", "Google Cloud"]
IDEAL_NUMBER_OF_TECH_SKILLS = 2
desirable_design_skills = ["User Interface Design", "Graphic Design", "User Experience Design"]
IDEAL_NUMBER_OF_DESIGN_SKILLS = 2
MAX_RECS = 3
#depending on dir structure
DIR = "CreatingTeams2025/Data"

df = pd.read_csv(os.path.join(DIR, FILE_NAME), encoding = "ISO-8859-1")
df = df[~df["display_name"].isin(TESTERS)]


#=== getting csv that tells us if their recruiting ====
hiring_file_path = os.path.join(DIR, HIRING_FILE_NAME)
with open(hiring_file_path, 'rb') as file:  #getting encoding for csv
    raw_data = file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']
hiring = pd.read_csv(hiring_file_path, encoding=encoding)
#=============================================

ppl_not_in_teams = df[df["team_name"].isna()]
unique_teams = df[~df["team_name"].isna()]["team_name"].unique()

#getting recruiting teams
recruiting_teams = []
for team in unique_teams:
    if list(hiring[hiring["team_name"] == team]["recruiting"])[0].lower() == "yes":
        recruiting_teams.append(team)

possible_design_skills = []
for skills_list in ppl_not_in_teams["skills_design"]:
    if not pd.isna(skills_list):
        individual_skills = skills_list.split(", ")
        individual_skills = [skill for skill in individual_skills if not skill in possible_design_skills]
        possible_design_skills += individual_skills

def get_potential_ppl_by_skill(desired_skill_list):
    index_list = {}
    for desired_skill in desired_skill_list:
        index_list[desired_skill] = df[(df["skills_design"].str.contains(desired_skill, na=False) | df["skills_comp_sci"].str.contains(desired_skill, na=False))].index

    return index_list

def get_unique_skills(team):
    unique_team_skills = []
    team_skills = df[df["team_name"] == team]["skills_design"]
    for skills in team_skills:
        if pd.isna(skills):
            continue
        for skill in skills.split(", "):
            if not skill in team_skills:
                unique_team_skills.append(skill)
    return unique_team_skills

def teams_that_need_tech_skills():
    needs_tech_skills = []

    for team in recruiting_teams:
        unique_team_skills = get_unique_skills(team)
        if len(set(unique_team_skills).intersection(desirable_tech_skills)) < IDEAL_NUMBER_OF_TECH_SKILLS: #team doesn't have desired design skills
            needs_tech_skills.append(team)
    return needs_tech_skills

def teams_that_need_design_skills():
    needs_design_skills = []
    for team in recruiting_teams:
        unique_team_skills = get_unique_skills(team)
        if len(set(unique_team_skills).intersection(desirable_design_skills)) < IDEAL_NUMBER_OF_DESIGN_SKILLS: #team doesn't have desired design skills
            needs_design_skills.append(team)
    return needs_design_skills

tech_skill_pool = get_potential_ppl_by_skill(desirable_tech_skills)
design_skill_pool = get_potential_ppl_by_skill(desirable_design_skills)

team = recruiting_teams[0]
recomendations = {team: [] for team in recruiting_teams}

tech_skill_counter = 0 #to ensure that skills get recommended evenly
design_skill_counter = 0 #to ensure that design people get recommended evenly



teams_need_tech = teams_that_need_tech_skills()
total_tech_skills = sum([len(tech_skill_pool[skill_indices]) for skill_indices in tech_skill_pool])
current_skill = 0
i = 0
while i < total_tech_skills and teams_need_tech:

    team = teams_need_tech[i%len(teams_need_tech)]

    offset = sum( [len(tech_skill_pool[skill_indices]) for skill_indices in list(tech_skill_pool.keys())[:current_skill]] )
    index_to_rec = tech_skill_pool[desirable_tech_skills[current_skill]][i-offset]
    current_rec_list = recomendations[team]
    if len(recomendations[team]) < MAX_RECS:
        if not index_to_rec in current_rec_list:
            recomendations[team].append({index_to_rec: desirable_tech_skills[current_skill]})
    if i + 1 >= len(tech_skill_pool[desirable_tech_skills[current_skill]]) + offset:
        current_skill += 1
    i += 1

teams_need_design = teams_that_need_design_skills()
total_design_skills = sum([len(design_skill_pool[skill_indices]) for skill_indices in design_skill_pool])
current_skill = 0
offset = 0
i = 0
while i < total_design_skills:
    
    team = teams_need_design[i%len(teams_need_design)]

    offset = sum( [len(design_skill_pool[skill_indices]) for skill_indices in list(design_skill_pool.keys())[:current_skill]] )

    index_to_rec = design_skill_pool[desirable_design_skills[current_skill]][i-offset]
    current_rec_list = recomendations[team]
    if len(recomendations[team]) < MAX_RECS * 2: #beacuse we also have tech recs, so now we're thinking about twice the size
        if not (index_to_rec in current_rec_list):
            recomendations[team].append({index_to_rec: desirable_design_skills[current_skill]})
    if i + 1 >= len(design_skill_pool[desirable_design_skills[current_skill]]) + offset:
        current_skill += 1
    i += 1

def get_complementary_skill(team_recommendations):
    tech_skills = []
    design_skills = []
    i = 0
    while i < len(team_recommendations) and list(team_recommendations[i].values())[0] in desirable_tech_skills: #ew! probably should refactor this
        if not list(team_recommendations[i].values())[0] in tech_skills:
            tech_skills.append(list(team_recommendations[i].values())[0])
        i += 1
    while i < len(team_recommendations) and not list(team_recommendations[i].values())[0] in desirable_design_skills:
        if not list(team_recommendations[i].values())[0] in design_skills:
            design_skills.append(list(team_recommendations[i].values())[0])
        i += 1
    return tech_skills, design_skills

def format_skills_to_email(team_recommendations):
    skill_collection = {}
    for rec in team_recommendations:
        if not list(rec.values())[0] in skill_collection:
            skill_collection[list(rec.values())[0]] = [list(rec.keys())[0]]
        else:
            skill_collection[list(rec.values())[0]].append(list(rec.keys())[0])
    result_string = ""
    for skill in skill_collection:
        result_string += f"{skill}:\n"
        people = ["    * " + df.loc[i]["display_name"] + f" ({df.loc[i]['email']})" for i in skill_collection[skill]]

        result_string += "\n".join(people)
        result_string += "\n"
    
    return result_string

output = {"name": [], "email_address": [], "email": [], "recommendations": []}
for team in recomendations:
    tech_skills, design_skills = get_complementary_skill(recomendations[team])
    formatted_skills = format_skills_to_email(recomendations[team])

    rec_list = ','.join(list(map(lambda x: str(list(x.keys())[0]), recomendations[team])))
    email_content = ""
    if tech_skills and design_skills:
        email_content += RECOMMEND_MEMBERS_EMAIl.format(SKILLS=tech_skills[0] + " or " + design_skills[0], SKILL_LIST=formatted_skills) 
    elif tech_skills:
        if len(tech_skills) >= 2:
            email_content += RECOMMEND_MEMBERS_EMAIl.format(SKILLS=tech_skills[0] + " or " + tech_skills[1], SKILL_LIST=formatted_skills) 
        else:
            email_content += RECOMMEND_MEMBERS_EMAIl.format(SKILLS=tech_skills[0], SKILL_LIST=formatted_skills) 
    elif design_skills:
        if len(design_skills) >= 2:
            email_content += RECOMMEND_MEMBERS_EMAIl.format(SKILLS=design_skills[0] + " or " + design_skills[1], SKILL_LIST=formatted_skills) 
        else:
            email_content += RECOMMEND_MEMBERS_EMAIl.format(SKILLS=design_skills[0], SKILL_LIST=formatted_skills) 

    # Append values to the output dictionary
    output["name"].append(team)
    output["email_address"].append(list(df[df["team_name"] == team]["email"])[0])
    output["email"].append(email_content)
    output["recommendations"].append(rec_list)

# print(output)
output = pd.DataFrame.from_dict(output)
output.to_csv("Team Recommendations.csv")