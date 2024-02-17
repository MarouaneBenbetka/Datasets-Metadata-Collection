import json
import requests
import base64
import json

headers = {
    'Authorization': 'Bearer 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',
}



#################################  GetRepositories    ###############################

def GetRepositories():
    def save_to_json(data, filename):
        with open(filename, "w") as json_file:
            json.dump(data, json_file, indent=2)

    def fetch_paginated_data(url):
        all_data = []
        cpt = 1

        while cpt<11 : 
            params = {
            'q': 'dataset',
            'per_page': 100,
            'page': cpt,
            }
            response = requests.get(url,headers=headers,params=params)
            cpt+=1
            if response.status_code == 200:
                print("Fetched repos page : " +str(cpt-1))
                data = response.json()
                all_data.extend(data['items'])  # Adjust based on the API response structure
                save_to_json(all_data, "github_DATA.json")
            else:
                print(f"Failed to fetch data . Status code: {response.status_code}")


    repos_url = "https://api.github.com/search/repositories"
    fetch_paginated_data(repos_url)
    print("All data saved to github_DATA.json file")


#################################  Clean Repositories    ###############################
def CleaningRepositories():
    keys_to_delete = [
        'keys_url', 'collaborators_url', 'teams_url', 'hooks_url', 
        'git_tags_url', 'git_refs_url', 'trees_url', 'statuses_url', 
        'stargazers_url', 'contributors_url', 'subscribers_url', 
        'subscription_url', 'commits_url', 'git_commits_url', 
        'compare_url', 'merges_url', 'archive_url','milestones_url','notifications_url','labels_url',
        'issue_comment_url','comments_url','languages_url','blobs_url','tags_url','ssh_url',
        'branches_url','assignees_url','events_url','issue_events_url','git_url','clone_url',
        'svn_url','homepage','has_pages','has_wiki','web_commit_signoff_required','allow_forking','default_branch','permissions'
    ]

    keys_use_to_delete = [
        "avatar_url","gravatar_id","followers_url","following_url","gists_url",
        "subscriptions_url","organizations_url","events_url","received_events_url"
    ]

    # Read the JSON file
    with open('github_DATA.json', 'r') as file:
        data = json.load(file)

    # Loop through each object in the array
    for item in data:
        # Delete specified keys within 'item'
        for key in keys_to_delete:
            if key in item:
                del item[key]

        # Delete specified keys within 'owner' if it exists
        if 'owner' in item and isinstance(item['owner'], dict):
            owner = item['owner']
            for key in keys_use_to_delete:
                if key in owner:
                    del owner[key]

    # Write the modified data back to the file
    with open('github_DATA.json', 'w') as file:
        json.dump(data, file, indent=2)

    print("CLEANING FILE DONE  : github_DATA.json")

#################################  Get readMe files     ###############################

def readMeScrapping() : 
    with open('github_DATA.json', 'r') as file:
        data = json.load(file)
    # Loop through each element in the array
    cpt =0
    for item in data:
        # Extract the URL from the element
        repo_url = item.get('url')
        
        # Check if the repo URL exists
        if repo_url:
            # Only fetch the readme if the 'readme' key does not already exist
            if 'readme' not in item:
                # Fetch the readme file content using GitHub API
                response = requests.get(repo_url + '/readme',headers=headers)
                
                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    print(f"Fetched readme for {item['full_name']}: {cpt}")
                    cpt+=1
                    # Extract and decode the content of the readme file
                    readme_content = response.json().get('content', '')
                    readme_content_decoded = base64.b64decode(readme_content).decode('utf-8')
                    
                    # Add the readme content to the item
                    item['readme'] = readme_content_decoded
                else:
                    print(f"Failed to fetch readme for {item['full_name']}: {response.status_code}")
                    if response.status_code ==403 : break
            else : 
                print("readme exists")

    # Write the modified data back to the file
    with open('github_DATA.json', 'w') as file:
        json.dump(data, file, indent=2)

    print("READ ME SCRAPPING DONE  SUCCESSFULLY .")


#################################  Get Issues data     ###############################


def GetIssues():

    def fetch_issues(issues_url):
        issues = []
        page = 1
            # Construct the issues URL for the repository
        url = f"{issues_url}?page={page}&per_page=5"

            # Make a GET request to the issues URL
        response = requests.get(url, headers=headers)

            # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            # Check if there are issues returned
            issues.extend(data)
        else:
            print(f'Error: {response.status_code}')

        return issues


    # Function to fetch comments of an issue
    def fetch_comments(comments_url):
        comments = []
        url = f"{comments_url}?page={1}&per_page=100"
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            for comment in data:
                comment_info = {
                    'id': comment['id'],
                    'created_at': comment['created_at'],
                    'updated_at': comment['updated_at'],
                    'user': {
                        'login': comment['user']['login'],
                        'id': comment['user']['id']
                    },
                    'body': comment['body'],
                    'reactions': comment['reactions']
                }
                comments.append(comment_info)

        return comments

    # Function to extract relevant information from an issue
    def extract_issue_info(issue):
        info = {
            'url' : issue['url'],
            'title': issue['title'],
            'body': issue['body'],
            'reactions': issue['reactions'],  # Assuming reactions are available directly in the issue object
            'created_at': issue['created_at'],
            'updated_at': issue['updated_at'],
            'closed_at': issue['closed_at']
        }
        return info

    # Load repository data from the JSON file
    with open('github_DATA.json', 'r') as f:
        repositories = json.load(f)

    # Dictionary to store repository details and their issues
    repository_data = []

    # Fetch issues for each repository
    cpt = 0
    for repo_data in repositories:
        issues_url = repo_data.get('issues_url', '').replace('{/number}', '')  # Replace placeholder with empty string
        if issues_url:
            issues = fetch_issues(issues_url)
            i = 0
            repo_data['issues'] = []  # Add an 'issues' attribute inside repo_data
            for issue in issues:
                # Extract useful information from each issue
                if i == 3:
                    break
                issue_info = extract_issue_info(issue)
                # Fetch comments for the issue
                comments_url = issue.get('comments_url', '')
                if comments_url:
                    issue_info['comments'] = fetch_comments(comments_url)
                repo_data['issues'].append(issue_info)
                i += 1
        cpt += 1
        print(f"Getting issues of repo : {cpt}")

    # Save the repository data into a new JSON file
    with open('github_DATA.json', 'w') as outfile:
        json.dump(repositories, outfile, indent=2)


print('#################################  Getting repos data   ###############################')
GetRepositories();
print('#################################  Cleaning repos       ###############################')
CleaningRepositories();
print('#################################  Get readMe files     ###############################')
readMeScrapping();
print('#################################  Get Issues data      ###############################')
GetIssues();