DIR = "CreatingTeams2025/Data/"
# FILE_NAME = "11-04 People in Teams Tool.csv"
# HIRING_FILE_NAME = "11-04 Teams in Tool.csv"
# OUTPUT_NAME = "Updated Recommendations 11-4"
FOLLOW_UP = False
FILE_NAME = "Challenge Data 10-22-24.csv"
HIRING_FILE_NAME = "Team Data 10-22-24.csv"
OUTPUT_NAME = "Team Recommendations"
TEAM_SIZE = 4
SORT_BY = "interests"

NO_INTERESTS_EMAIL_HEADER = """
Dear {STUDENT_NAME},
I hope this email finds you well. As a participant in the Nittany AI Challenge, we're excited to have you on board!
We've noticed that you haven't added any interests to your bio yet. While this isn't mandatory, sharing your interests can be a great way to find common ground with your teammates and foster better collaboration.

If you're looking for a team, we're here to help! Here are {TEAM_SIZE} other students who are interested in joining/creating a team:

{MEMBER_LIST}

This could be the beginning of something great! We encourage you to reach out and start thinking about ideas!
"""


INTERESTS_EMAIL_HEADER = """
Dear {STUDENT_NAME},
I hope this email finds you well. As a participant in the Nittany AI Challenge, we're excited to have you on board!

If you're looking for a team, we're here to help! Here are {TEAM_SIZE} other students who are also interested in {INTERESTS}:

{MEMBER_LIST}

This could be the beginning of something great! We encourage you to reach out and start thinking about ideas!
"""


RECOMMEND_MEMBERS_EMAIl = """{SKILL_LIST}"""



CLOSER = "This could be the beginning of something great! We encourage you to reach out and introduce yourself!\n\nThese AI generated results are part of a pilot program to assist students form and find teams. You may receive multiple messages in the effort to find a best fit."



RECOMMENDATION_INDIVIDUAL_MESSAGE = """{RECOMMENDATIONS}"""



FILL_OUT_THE_TEAMS_TOOL = """We noticed you haven't yet filled out your info in the "Teams Tool." While this isn't mandatory, sharing your interests can be a great way to find common ground with your teammates and foster better collaboration. 

By completing it, you'll receive recommendations on how to strengthen your team or find the right group to join. Don't miss out on the chance to compete—take a moment to fill it out today! """


NO_INTEREST_RECOMMENDATIONS = """{CONTACTS}"""


# ===== FOLLOW UP EMAILS ======
TEAM_FOLLOW_UP = """Your team is getting close to the competition, and we're excited about your potential! To make your team even stronger, we recommend adding a mix of skills and interests. We've identified a few key areas—like {SKILLS}—that could give your project a boost, and we've matched you with students who bring those skills. 

{SKILL_LIST}

We encourage you to reach out to see if they'd be interested in joining your team. 

These AI-generated suggestions are part of a pilot program to help students form teams. You may get a few messages as we work to find the best fits. If you decide not to continue with the challenge, just reply to this email, and we'll take you off the list. 

Additionally, we have a great event coming up to help you get prepared: 

Thursday, November 7, 6 PM - 8 PM, Room 131 HUB - Academic Advising Unplugged: Understanding the Issues: This is your chance to connect with academic advisors and students interested in AI's impact on education. Whether you have an idea or just want to brainstorm, this event will be a great place to learn and collaborate. 

We hope to see you there! This event will give you valuable insights and help your team make the most of the challenge. 

Best of luck! 
"""

INDIVIDUAL_FOLLOW_UP = """Are you looking to compete in the Nittany AI Challenge but still need a team? Thanks for taking the first step and completing your profile in the "Team Tool!" Based on your interests, we've found some people who could be a great match for you:  

 
{RECOMMENDATIONS}
We encourage you to reach out to them and start building your team! 

 

These AI generated results are part of a pilot program to assist students form and find teams. You may receive multiple messages in the effort to find the best fit. If you do not intend to continue in the Nittany AI Challenge, please reply to this email so we can remove you from future mailing.  

 

Additionally, we have a great event coming up to help you get prepared: 

Thursday, November 7, 6 PM - 8 PM, Room 131 HUB - Academic Advising Unplugged: Understanding the Issues: This is your chance to connect with academic advisors and students interested in AI’s impact on education. Whether you have an idea or just want to brainstorm, this event will be a great place to learn and collaborate. 

 
We hope to see you there! This event will give you valuable insights and help your team make the most of the challenge. 
"""
