# AdvanceRepo
Template for new Advance Projects

Includes:
- Pull Request Template
- Issues Template
- Branch Protection

# Individual Matching algorithm
The goal of this algorithm is to match individuals that are not currently in a team with each other. The over-arching idea is to encourage team formation and make it easier for students to get involved in the Nittany Ai Challenge.

## Matching philosophy
In order to create teams focused on solving similar problems, we match students based on interests.
### Step 1:
* Organize students by interest, from least popular interest to most popular. 
* Since students can have more than one interest, we prioritize students with less interests to those with more interests, since those with more interests have a higher liklihood of matching with someone.
    * For example, if student A only has interest I~1~, and student B has interests I~1~, and I~2~, then we will attempt to match student A to other first, since the pool of people that share common interests is smaller for student A.

### Step 2
* Match students together until no longer possible. 
    * If we can no longer create a full team, but students with only 1 interest remain, then we place the residue on pre-existing teams until there is no more students left with only 1 interest. This means that it is possible for there to be teams greater than the desired team size.
* For example, if interest I~1~ has 14 people with only interest I~1~ and we want to create teams of 4, there will be 2 people left over with only 1 interest. Then we will put those 2 remaining people on already created teams.
* If there is not enough people to create a full team at all, then we recommend everyone within the interest to each other, as well as people from other interests.

### Step 3
* Repeat the process until everyone that listed interests has been matched with a team. 
* Any remaining students can be randomly placed on a (least-membered) team that fulfills their listed interests

### Step 4
* Match students that didn't list interests. Since we have literally no infromation to go off of, we have no criteria to match the students. Therefore, we randomly pair students until we can no longer create a full team, after which we randomly place the remaining students on matched teams. 

### Step 5
* Generate email text from pre-written email prompt, and then load into excel sheet.s