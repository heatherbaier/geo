# Instructions for working on GEO

## Reading the [tasks chart](https://github.com/users/heatherbaier/projects/5/views/1?visibleFields=%5B%22Title%22%2C%22Status%22%2C%22Assignees%22%2C73950250%2C%22Linked+pull+requests%22%2C%22Reviewers%22%2C%22Repository%22%5D)

Columns  
*Title:* Description of the task  
*Status:*   
* Backlog: Not ready to be taken  
* Ready: Available for taking  
* In Progress: Assignee is working on it  
* In Review: Heather is checking  
* Done: Finito!  

*Assignees:* Person assigned to/working on the task  
*Estimate:* Number of hours estimated to complete  
*Linked Pull Request:* The pull request submitted when the task is finished  
*Reviewers:* Heather  
*Repository:* Should generally be GEO  


## Setup
1. Open a terminal and clone the repository to your computer:
```git clone https://github.com/heatherbaier/geo```
2. Download the gh clinet
```brew install gh```
3. Authenticate gh
```gh auth login```


## Process

**1. Look over tasks and see what you want to do**
First thing you will look at is the task name. There are 3 main task types:  
* List variables: This will require going through each of the spreadsheets in the repository for the assigned country, looking through the websites listed in the metadata, and listing out detailed description of each of the variables, as well as what years they are available for.
    - Script example:
    - General time estimate: 2-4 hours
* Assign geoB ID’s: This will entail assigning each school to every ADM level available in the geoBoundaries database.
    - Script example:
    - General time estimate: 1-2 hours
* Assign GEO ID’s: A simple task entailing assigning a GEO database specific ID to each school for the given country
    - Script example: 
    - General time estimate: 30 minutes

**2. Assign yourself to a task**
Clip the dropdown arrow in the Assignee column and assign yourself to the task!

**3. Complete the task**
* Check to see if there are any branches already associated with the issue: if there are, reach out to the team and see if someone has already done work on it.
    - ```gh issue develop --list <issue_numer>```
* Create a branch for the issue based on the current master branch and switch to it
- ```gh issue develop <issue_numer> --base master --checkout```
* See the task specific instructions 
    - Assign geoB ID’s:
    - Assign GEO ID’s:
    - List variables:

## Specific instructions for tasks
