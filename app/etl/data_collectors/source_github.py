import requests
import base64
import os

from app.utils.extract import save_raw_data_to_json


repos_url = "https://api.github.com/search/repositories"
NB_PAGES = 1

auth_token = os.getenv("GITHUB_AUTH_TOKEN")
headers = {
    f"Authorization": f'Bearer {auth_token}',
}


def get_datasets_metadata_github():
    repos = get_repos_datasets(repos_url)
    repos_clean = clean_repos(repos)

    repos_with_readme = readme_collection(repos_clean)

    repos_with_issues = get_issues(repos_with_readme)
    save_raw_data_to_json(repos_with_issues, 'github')
    return repos_with_issues


def clean_repos(data):
    keys_to_delete = [
        'keys_url', 'collaborators_url', 'teams_url', 'hooks_url',
        'git_tags_url', 'git_refs_url', 'trees_url', 'statuses_url',
        'stargazers_url', 'contributors_url', 'subscribers_url',
        'subscription_url', 'commits_url', 'git_commits_url',
        'compare_url', 'merges_url', 'archive_url', 'milestones_url', 'notifications_url', 'labels_url',
        'issue_comment_url', 'comments_url', 'languages_url', 'blobs_url', 'tags_url', 'ssh_url',
        'branches_url', 'assignees_url', 'events_url', 'issue_events_url', 'git_url', 'clone_url',
        'svn_url', 'homepage', 'has_pages', 'has_wiki', 'web_commit_signoff_required', 'allow_forking', 'default_branch', 'permissions'
    ]

    keys_use_to_delete = [
        "avatar_url", "gravatar_id", "followers_url", "following_url", "gists_url",
        "subscriptions_url", "organizations_url", "events_url", "received_events_url"
    ]

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
    return data


def readme_collection(data):

    # Loop through each element in the array
    cpt = 0
    for item in data:
        # Extract the URL from the element
        repo_url = item.get('url')

        # Check if the repo URL exists
        if repo_url:
            # Only fetch the readme if the 'readme' key does not already exist
            if 'readme' not in item:
                # Fetch the readme file content using GitHub API
                response = requests.get(repo_url + '/readme', headers=headers)

                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    print(f"Fetched readme for {item['full_name']}: {cpt}")
                    cpt += 1
                    # Extract and decode the content of the readme file
                    readme_content = response.json().get('content', '')
                    readme_content_decoded = base64.b64decode(
                        readme_content).decode('utf-8')

                    # Add the readme content to the item
                    item['readme'] = readme_content_decoded
                else:
                    print(
                        f"Failed to fetch readme for {item['full_name']}: {response.status_code}")
                    if response.status_code == 403:
                        break
            else:
                print("readme exists")

    return data


def get_issues(data):

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
            'url': issue['url'],
            'title': issue['title'],
            'body': issue['body'],
            # Assuming reactions are available directly in the issue object
            'reactions': issue['reactions'],
            'created_at': issue['created_at'],
            'updated_at': issue['updated_at'],
            'closed_at': issue['closed_at']
        }
        return info

    # Load repository data from the JSON file

    # Dictionary to store repository details and their issues
    repository_data = []

    # Fetch issues for each repository
    cpt = 0
    for repo_data in data:
        issues_url = repo_data.get('issues_url', '').replace(
            '{/number}', '')  # Replace placeholder with empty string
        if issues_url:
            issues = fetch_issues(issues_url)
            i = 0
            # Add an 'issues' attribute inside repo_data
            repo_data['issues'] = []
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

    return data


def get_repos_datasets(url):
    datasets = []
    cpt = 0

    while cpt < NB_PAGES:
        params = {
            'q': 'dataset',
            'per_page': 100,
            'page': cpt+1,
        }
        response = requests.get(url, headers=headers, params=params)
        cpt += 1
        print("Fetched repos page : " + str(cpt))
        if response.status_code != 200:
            print(f"Failed to fetch repos: {response.status_code}")
            continue

        data = response.json()
        datasets.extend(data['items'])

    return datasets


if __name__ == "__main__":
    data = get_datasets_metadata_github()
