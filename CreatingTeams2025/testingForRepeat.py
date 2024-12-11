import pandas as pd 

no_interests = pd.read_csv("No interests recommendations.csv")
interests = pd.read_csv("Individual Recommendations.csv")
teams = pd.read_csv("Team Recommendations.csv")


team_emails = list(teams["team_admin"])
for email in no_interests["email_address"]:
    if email in team_emails:
        print(f"Uh oh: {email}")
    team_emails.append(email)

for email in interests["email_address"]:
    if email in team_emails:
        print(f"Uh oh: {email}")
    team_emails.append(email)


