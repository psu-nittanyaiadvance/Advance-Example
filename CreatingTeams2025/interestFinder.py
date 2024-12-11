import pandas as pd
from dotenv import load_dotenv
import json
import os
import numpy as np
from config import RECOMMENDATION_INDIVIDUAL_MESSAGE, FILE_NAME, FILL_OUT_THE_TEAMS_TOOL, NO_INTEREST_RECOMMENDATIONS, DIR, OUTPUT_NAME, INDIVIDUAL_FOLLOW_UP, FOLLOW_UP
import sys
load_dotenv()

def create_all_interests(df): #expecting "interests" column
    all_interests = []
    for ind in df.index:
        interests = df.loc[ind, "interests"]
        if not isinstance(interests, str):
            continue
        interests = interests.split(", ")
        for interest in interests:
            if not interest.lower() in all_interests:
                all_interests.append(interest.lower())
    return all_interests

def create_interests_columns(df, all_interests):
    for interest in all_interests:
        df[interest.lower()] = df["interests"].apply(lambda x: 1 if isinstance(x, str) and (interest in x.lower()) else 0)

TESTERS = ["Minseo Kim", "Zachary Walnock", "Ethan Sullivan", "Andy Gatto", "Devan Patel", "Jeff Remington", "Landen Warner"]
df = pd.read_csv(DIR + FILE_NAME, encoding = "ISO-8859-1")
df = df[df["team_name"].isna()]
df = df[~df["display_name"].isin(TESTERS)]
uninterested = df[df["interests"].isna()] #people who didn't fill it out
unique_interests = create_all_interests(df)
create_interests_columns(df, unique_interests)
df["times_recommended"] = 0
df = df[~df["interests"].isna()]
df = df.drop_duplicates(subset="email", keep="first")

"""
1. Loop through each person
2. Recommend them 3 people for each of their interests
3. Increment "times recommended" for each person recommended
4. Go to next person
"""
# print(df["interests"])

def get_three_from_interest(interest):
    # Get the pool of students with the given interest
    interest_df = df[df[interest] == 1]
    
    
    # Sort by 'times_recommended' and pick the top 3
    df_sorted = interest_df.sort_values("times_recommended")
    df.loc[df_sorted.iloc[:3, :].index, "times_recommended"] += 1
    
    return df_sorted.iloc[:3, :].index


def format_interest_recs(recommendations):
    result_str = ""
    for interest in recommendations:
        result_str += f"People interestd in {interest}:\n"
        people = [f"    * {df.loc[i, 'display_name']} ({df.loc[i, 'email']})" for i in recommendations[interest]]
        result_str += "\n".join(people) + "\n\n"
    return result_str

def get_total_recs_by_email(recommendations):
    indices = []
    for interest in recommendations:
        if interest == "email":
            continue
        indices.extend(recommendations[interest])
    return ','.join(list(map(lambda x: str(x), indices)))

#create the recommendations based on the algorithm above
recommendations = {}
output = {}
for i in df.index:
    interests = [col for col in df.columns if df.loc[i][col] == 1 and col != "times_recommended"]
    recommendations[i] = {}
    total_recs = []
    for interest in interests:
        three_from_interest = list(get_three_from_interest(interest))
        recommendations[i][interest] = three_from_interest

        if i in three_from_interest:
            #remove the current student from the recommendations
            three_from_interest.remove(i)
        total_recs.extend(list(three_from_interest))

    if FOLLOW_UP:
        EMAIL_TO_FORMAT = INDIVIDUAL_FOLLOW_UP
    else:
        EMAIL_TO_FORMAT = RECOMMENDATION_INDIVIDUAL_MESSAGE

    email = EMAIL_TO_FORMAT.format(RECOMMENDATIONS=format_interest_recs(recommendations[i]))
    recommendations[i]["email"] = email


#format everything for csv
output = {"name": [], "email_address": [], "email": [], "recommendations": []}
for index in recommendations:
    output["name"].append(df.loc[index, "display_name"])
    output["email_address"].append(df.loc[index, "email"])
    recs = []
    # for interest in recommendations[index]:
    #     recs.extend(list(recommendations[index][interest]))
    # output["recommendations"].append(recommendations[index]["recommendations"])
    rec_list = get_total_recs_by_email(recommendations[index])
    output["email"].append(recommendations[index]["email"])
    output["recommendations"].append(rec_list)

output = pd.DataFrame.from_dict(output)
output.to_csv(OUTPUT_NAME + " Ind Rec.csv")

"""
People who didn't fill out the interests part, no recommendations option
"""

output = {"name": [], "email_address": [], "email": []}
for index in uninterested.index:
    output["name"].append(uninterested.loc[index, "display_name"])
    output["email_address"].append(uninterested.loc[index, "email"])
    output["email"].append(FILL_OUT_THE_TEAMS_TOOL)

output = pd.DataFrame.from_dict(output)
# output.to_csv("Didn't fill out the teams tool.csv")

"""
People who didn't fill out the interests part, giving recommendations anyway option
"""

def create_email_from_group(group_indices):
    emails = {}
    for index in group_indices:
        emails[index] = {}
        contacts = [f"  * {uninterested.loc[i, 'display_name']} ({uninterested.loc[i, 'email']})" for i in group_indices if i != index]
        emails[index]["email"] = NO_INTEREST_RECOMMENDATIONS.format(CONTACTS="\n".join(contacts))
        emails[index]["recommendations"] = ",".join([ uninterested.loc[i, "email"] for i in group_indices if i != index])
    return emails

groups = []
tmp_df = uninterested
email_info = {}
while len(tmp_df) != 0:
    group = tmp_df.iloc[:3, :].index
    if len(group) < 3:
        group.append(pd.Index([uninterested.index[0]]))
    groups.append( tmp_df.iloc[:3, :].index )
    tmp_df = tmp_df.iloc[3:, :]
    
    email_info.update(create_email_from_group(group))

output = {"name": [], "email_address": [], "email": [], "recommendations": []}
for index in email_info:
    output["name"].append(uninterested.loc[index, "display_name"])
    output["email_address"].append(uninterested.loc[index, "email"])
    output["email"].append(email_info[index]["email"])
output = pd.DataFrame.from_dict(output)
output.to_csv(f"{OUTPUT_NAME} No Interests.csv")
