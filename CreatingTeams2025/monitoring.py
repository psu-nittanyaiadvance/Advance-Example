"""
Metrics to track: 
    - Number of new teams formed
    - Recommendations linked within newly created teams
        - How many people in the team were a recommendation to someone else in the team
    - Number of people who joined existing teams
        - Number of new joins that were recommended to the team
    - Mix of interests
        - How many teams have one common interest
        - How many teams dont have a common interest
    - Graphing when people fill out the teams tool
        - Adding the time component
"""

import pandas as pd
import os

TEAMDATA_DIR = "CreatingTeams2025/Data"
RECOMMENDATIONS_DIR = "Emails/SentEmailsFormatted"

individual_recs = pd.read_csv(os.path.join(RECOMMENDATIONS_DIR, "Individual Recommendations.csv"))
no_interest_recs = pd.read_csv(os.path.join(RECOMMENDATIONS_DIR, "No interests recommendations.csv"))
team_recs = pd.read_csv(os.path.join(RECOMMENDATIONS_DIR, "Team Recommendations.csv"))
new_data = pd.read_csv(os.path.join(TEAMDATA_DIR, "11-04 People in Teams Tool.csv"), encoding="ISO-8859-1")
old_data = pd.read_csv(os.path.join(TEAMDATA_DIR, "Challenge Data 10-22-24.csv"), encoding="ISO-8859-1")

def unique_teams(df):
    return df[~df["team_name"].isna()]["team_name"].unique()

def get_new_members(team):
    old_members = old_data[old_data["team_name"] == team]["email"]
    new_members = new_data[new_data["team_name"] == team]["email"]
    return new_members[~new_members.isin(old_members)]

def get_percentage_of_existing_studnets(list_of_student_emails):
    if len(list_of_student_emails) == 0:
        return -1
    total = 0
    for email in list_of_student_emails:
        if email in list(old_data["email"]):
            total += 1
    return total / len(list_of_student_emails)

def check_if_recommended_to_team(new_emails, team):
    if len(new_emails) == 0:
        return -1
    rec_indices = team_recs[team_recs["name"] == team].iloc[0]["recommendations"]
    rec_indices = list(map(int, rec_indices.split(',')))
    rec_emails = old_data.loc[rec_indices, "email"].to_list()
    recommended_and_joined = 0
    for email in new_emails:
        if email in rec_emails:
            recommended_and_joined += 1
    return recommended_and_joined / len(new_emails)

def check_recs_in_new_team(team):
    members_emails = new_data[new_data["team_name"] == team]["email"]
    print(team)
    successfull_recommendations = 0
    new_team_tool_entries = 0
    num_ppl_in_teams_tool = 0
    for target_email in members_emails:
        if not target_email in old_data["email"].to_list():
            print("Skipping")
            new_team_tool_entries += 1
            continue
        num_ppl_in_teams_tool += 1
        for email in members_emails:
            if email == target_email:
                continue
            if email in individual_recs["email_address"].to_list():
                print("In individual recs")
                recommendations = individual_recs[individual_recs["email_address"] == email]["recommendations"].iloc[0].split(",")
                print(recommendations)
                if target_email in recommendations:
                    successfull_recommendations += 1
            elif email in no_interest_recs["email_address"].to_list():
                print("In no interest recs")
                recommendations = no_interest_recs[no_interest_recs["email_address"] == email]["recommendations"].iloc[0].split(",")
                print(recommendations)
                if target_email in recommendations:
                    successfull_recommendations += 1
            else:
                print("Neither")
                continue
    return successfull_recommendations, new_team_tool_entries, num_ppl_in_teams_tool


if __name__ == "__main__":
    # === Finding number of new teams formed ===
    old_teams = unique_teams(old_data)
    updated_teams = unique_teams(new_data)
    num_new_teams = len(updated_teams) - len(old_teams)
    # ==========================================

    # === Number of people who joined existing teams ===
    new_members = map(get_new_members, old_teams)
    percent_returning = map(get_percentage_of_existing_studnets, new_members)
    # ==================================================

    # === Percentage of people that joined that were recommended ===
    percent_successful_recs = map(check_if_recommended_to_team, new_members, old_teams)
    # print(list(percent_successful_recs)) #nobody we recommended joined :(
    # ==============================================================

    # === Number of people in new teams that were recommended to each other ===
    new_teams = [team for team in updated_teams if team not in old_teams]
    dropped_teams = [team for team in old_teams if team not in updated_teams]
    individual_rec_results = list(map(check_recs_in_new_team, new_teams)) 
    """
    1 team renamed themselves and none of the new team members were in the teams tool
    1 team had its members in the team tool but weren't recommended to each other
    2 teams only had 1 or 0 people in the teams tool  
    """
    # =========================================================================
    


    