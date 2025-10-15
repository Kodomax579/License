"""
Script to look for licences in Github repos
"""
import time
import requests

result = []


def set_access_token(access_token):
    """
    set access header
    """
    with open('PersonalAccessToken.txt', 'r', encoding="UTF-8") as github_token_file:
        github_token = github_token_file.read().strip()
    access_token = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"token {github_token}"
    }
    return access_token

def request_github_license(user, repo, original_url,request_session,request_header):
    """
    Requesting repo to look for a license
    If there is one or nothing, it will be saved
    """
    start_request = time.time()
    api_url = f"https://api.github.com/repos/{user}/{repo}"
    response = request_session.get(api_url,headers=request_header)
    if response.status_code == 200:
        data = response.json()
        if "license" in data and data["license"]:
            license_name = data["license"]["name"]
            result.append(f"{original_url}  --> License: {license_name}")
        else:
            result.append(f"{original_url}  --> License: not Found")
    else:
        result.append(f"{original_url}  --> Error: Status {response.status_code}")
    end_request = time.time()
    print("Request time:", end_request-start_request)

def start_checking_repos(github_urls,request_urls,request_headers):
    """
    Check urls
    """
    start = time.time()
    for url in github_urls:
        if "github.com/" not in url:
            result.append(f"{url}  --> Invalid URL")
            continue
        try:
            part = url.split("github.com/")[1].split('/')

            if len(part) == 1:
                repos = request_urls.get(f"https://api.github.com/users/{part[0]}/repos",headers=request_headers).json()
                for rep in repos:
                    repo_url = f"https://github.com/{part[0]}/{rep['name']}"
                    request_github_license(part[0], rep['name'], repo_url,request_urls,request_headers)
            else:
                request_github_license(part[0], part[1], url,request_urls, request_headers)
        except Exception as e:
            result.append(f"{url}  --> Error: {e}")

    with open('github_url_license.txt', 'w', encoding="UTF-8") as f:
        for line in result:
            f.write(line + '\n')

    end = time.time()

    print("Time:", end - start)
    print("Done ✅")


if __name__ == "__main__":
    session = requests.Session()
    headers = {}
    headers = set_access_token(headers)
    with open('github_url.txt', 'r', encoding="UTF-8") as datei:
        urls = datei.read().splitlines()

    start_checking_repos(urls,session,headers)
