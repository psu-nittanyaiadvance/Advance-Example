import pandas as pd
from dotenv import load_dotenv
import numpy as np
from config import TEAM_SIZE, SORT_BY, FILE_NAME, NO_INTERESTS_EMAIL_HEADER, INTERESTS_EMAIL_HEADER
load_dotenv()

dir = "CreatingTeams2025/"
people = pd.read_csv(dir + FILE_NAME)
peopleWithoutTeams = people[people['team_name'].isna()]

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

def cosine_simularity(A, B):
    if A == 0 or B == 0:
        return 0
    return np.dot(A,B)/(np.linalg.norm(A)*np.linalg.norm(B))

# def main(df):
#     """
#     Ideal team size is 5, so we want to create lists of 6, and then send an email out to each person with the emails of the other 5 people. 

#     Since cosine simularity is communicative (i.e., cosine(a, b) = cosine(b, a)), the best approach would be to create a likely team of 6
#     and then remove them from the list.

#     Once the pool gets below a certain number of people (I'm calling it 10 for now), we put previously matched people back into the possible pool.
#     The idea is maybe person B doesn't rank very high on person A's matching list, but person A is really high on person B's matching list.   
#     """
#     all_interests = create_all_interests(df)
#     create_interests_columns(df, all_interests)
#     all_interests.sort(key=lambda x: df[x.lower()].sum()) #sorting the interests from least popular to most popular
#     interest_dfs = [df[df[interest.lower()] == 1] for interest in all_interests]
#     if not os.path.isfile(os.path.join(dir, "embeddings.json")):
#         #TODO parallelize embedding calc
#         bio = df["bio"]
#         embeds = map(get_bio_embedding, list(bio))
#         json_data = json.dumps({"embeddings": list(embeds), "index": list(bio.index)}, indent=2)
#         with open(os.path.join(dir, "embeddings.json"), 'w') as f:
#             f.write(json_data)
#     with open(os.path.join(dir, 'embeddings.json'), 'r') as f:
#         loaded_data = json.load(f)
#         matches = []
#         for embedding_index, index in enumerate(loaded_data["index"]):
#             embedding = loaded_data["embeddings"][embedding_index]
#             top_canidates_index = [0] * TEAM_SIZE 
#             top_canidates_simularity = [0] * TEAM_SIZE 
#             for df_index, interest in enumerate(all_interests):
#                 top_canidates_simularity.sort(reverse=True)
#                 if df.loc[index, interest] == 1:
#                     for person_b_embedding_index, interest_index in enumerate(interest_dfs[df_index].index):
#                         simularity = cosine_simularity(embedding, loaded_data["embeddings"][loaded_data["index"][person_b_embedding_index]])
#                         top = TEAM_SIZE -1
#                         found = False
#                         while top >= 0 and not found:
#                             if simularity > top_canidates_simularity[top]:
#                                 found = True
#                                 top_canidates_simularity[top] = simularity
#                                 top_canidates_index[top] = interest_index
#                             top -= 1
#                 # print(top_canidates_simularity)
#                 matches.append([index] + top_canidates_index)
#             break
#         print(matches[0])

def create_individual_email(team, df):
    """
    teams is a list of teams, each team is described as a list of indicies for their corresponding 
    entry in df. 
    """
    individual_info = df.loc[team]
    student_names = [individual_info.loc[ind]["display_name"] for ind in individual_info.index]
    student_emails = [individual_info.loc[ind]["email"] for ind in individual_info.index]
    emails = []
    if individual_info["interests"].isna().sum() != 0:
        for i, name in enumerate(student_names):
            counter = 1
            name_display = []
            for i in range(len(student_names)):
                if not student_names[i] == name:
                    name_display.append(f"{counter}. " + student_names[i] + " (" + student_emails[i] + ")")
                    counter += 1
            text = NO_INTERESTS_EMAIL_HEADER.format(STUDENT_NAME=name, TEAM_SIZE=len(name_display), MEMBER_LIST="\n".join(name_display))
            emails.append({"text": text, "student": name, "student_email": student_emails[i]})
    else:
        common_interests = individual_info.columns[(individual_info == 1).all()]
        common_interests_string = common_interests[0]
        for i in range(1, len(common_interests)): #non empty if common_interests is less than 2 elements, do
            if i == len(common_interests)-1 and i > 0:
                common_interests_string += ", and " + common_interests[i]
            else:
                common_interests_string += ", " + common_interests[i]
        for i, name in enumerate(student_names):
            name_display = []
            counter = 1
            for i in range(len(student_names)):
                if not student_names[i] == name:
                    name_display.append(f"{counter}. " + student_names[i] + " (" + student_emails[i] + ")")
                    counter += 1
            text = INTERESTS_EMAIL_HEADER.format(STUDENT_NAME=name, TEAM_SIZE=len(name_display), INTERESTS=common_interests_string, MEMBER_LIST="\n".join(name_display))
            emails.append({"text": text, "student": name, "student_email": student_emails[i]})
    return emails

def find_team_groups(filtered_df):
    teams = []
    i = 0
    while i < len(filtered_df) and TEAM_SIZE < len(filtered_df) - i:
        teams.append(list(filtered_df.index[i:i+TEAM_SIZE]))
        i += TEAM_SIZE

    remaining = filtered_df.loc[filtered_df.index[i:]]

    if not "num_"+SORT_BY in filtered_df.columns: #if we're using the "no interests" dataframe
        return {"full_teams": teams, "remaining": remaining}
    
    remaining_one_interest = remaining[remaining["num_" + SORT_BY] == 1] #placing anybody remaining with only one interest on a group 
    for j in range(len(remaining_one_interest)):
        teams[ j%(len(teams)) ].append(remaining_one_interest.index[j])
    remaining = remaining.drop(remaining_one_interest.index) #these people have multiple interests and will be placed on future teams
    return {"full_teams": teams, "remaining": remaining}

def create_teams(df):

    SORT_BY = "interests"

    all_interests = create_all_interests(df)
    create_interests_columns(df, all_interests)
    all_interests.sort(key=lambda x: df[x.lower()].sum()) #sorting the interests from least popular to most popular
    df["num_" + SORT_BY] = df[all_interests].sum(axis=1)

    no_interests_group = df[df[SORT_BY].isna()]
    df = df.dropna(subset=[SORT_BY])
    
    teams = []
    current_df = df #saving total df
    for group in all_interests[1:]:
        filtered_df = current_df[current_df[group] == 1]
        result = find_team_groups(filtered_df)
        teams += result["full_teams"]
        filtered_df = filtered_df.drop(result["remaining"].index)
        current_df = current_df.drop(filtered_df.index) #remove people who just got a team
    
    teams.sort(key=lambda x: len(x))
    for i, index in enumerate(current_df.index): #remaining people with interests who weren't placed on a team
        teams[i] += [index]
    
    no_interest_results = find_team_groups(no_interests_group)
    teams += no_interest_results["full_teams"]
    teams.sort(key=lambda x: len(x))

    for i, index in enumerate(no_interest_results["remaining"].index): #remaining people with interests who weren't placed on a team
        teams[i] += [index]

    return teams

def main(df):
    teams = create_teams(df)
    email_list = [] #name, email text, indicies, other group members
    for team in teams:
        emails = create_individual_email(team, df)
        for i, email in enumerate(emails):
            email_list.append({
                "student": email["student"],
                "student_email": email["student_email"],
                "email_body": email["text"],
                "team": ", ".join(list(df.loc[teams[i]]["display_name"])),
                "team_indices": ", ".join(map(lambda x: str(x), teams[i]))
            })
    df = pd.DataFrame(email_list)
    df.to_csv("Email List.csv")
main(peopleWithoutTeams)