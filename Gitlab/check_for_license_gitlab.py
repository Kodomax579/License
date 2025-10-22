"""
Script to look for licenses in GitLab repos
"""
import time
import requests
import ssl
import socket


BASE_URL = "https://gitlab.insight-centre.org/api/v4"
result = []
headers = {}


def set_access_token(access_token):
    """
    set access header
    """
    with open('personal_access_token.txt', 'r', encoding="UTF-8") as github_token_file:
        github_token = github_token_file.read().strip()
    access_token = {
        "PRIVATE-TOKEN":github_token
    }
    return access_token

def request_gitlab_repo_license(project_id , request_session):
    """Request repo license info and store result"""
    start_request = time.time()

    repo = request_session.get(f"{BASE_URL}/projects/{project_id}?license=true", headers=headers).json()

    if "license" in repo and repo["license"]:
        license_name = repo["license"]["name"]
        result.append(f'{repo["namespace"]["web_url"]}/{repo["name"]}  --> License: {license_name}')
    else:
        result.append(f'{repo["namespace"]["web_url"]}/{repo["name"]}  --> License: not found')

    end_request = time.time()
    print("Request time:", round(end_request - start_request, 3), "s")

def request_gitlab_project(project_id, request_session,url):
    """Request project"""
    try:
        projects = request_session.get(f"{BASE_URL}/groups/{project_id}/projects", headers = headers).json()

        if not projects:
            result.append(f"{url}  --> No Projects found")
            return
        
        for project in projects:
            request_gitlab_repo_license(project["id"],request_session)
    except Exception as e:
        result.append(f"{url}  --> Error:{e}")

def start_checking_repos_from_list(request_session):
    """Request projects from user"""
    start = time.time()

    with open('gitlab_url.txt', 'r', encoding="UTF-8") as datei:
        gitlab_urls = datei.read().splitlines()

    for url in gitlab_urls:
        if "gitlab.insight-centre.org" not in url:
            result.append(f"{url}  --> Invalid URL")
            continue
        try:
            part = url.split("gitlab.insight-centre.org")[1].split('/')

            if len(part) > 1:
                url = f"{part[1]}%2F{part[2]}"
                request_gitlab_repo_license(url,request_session)

        except Exception as e:
            result.append(f"{url}  --> Error: {e}")

    with open("gitlab_url_license.txt", "w", encoding="utf-8") as f:
        for line in result:
            f.write(line + "\n")

    print("Total time:", round(time.time() - start, 2), "s")
    print("Done ✅")


def start_checking_all_repos(request_session):
    """Request the users und projects"""
    start = time.time()

    try:
        all_groups = request_session.get(f"{BASE_URL}/groups?all_available=true&per_page=100", headers = headers).json()
        
        for group in all_groups:
            request_gitlab_project(group["id"],request_session,group["web_url"])
            
    except Exception as e:
        result.append(f"Error: {e}")

    with open("gitlab_url_license.txt", "w", encoding="utf-8") as f:
        for line in result:
            f.write(line + "\n")

    print("Total time:", round(time.time() - start, 2), "s")
    print("Done ✅")

def menu():
    """Simple console menu"""
    print("GitLab License Checker")
    print("1. Check all repos")
    print("2. Check specific repos from the file")
    choice = input("press a number: (1 or 2): ").strip()
    return choice

if __name__ == "__main__":
    session = requests.Session()
    headers = set_access_token(headers)
    session.verify = "certificate.pem"
    choice = menu()
    if choice == "1":
        start_checking_all_repos(session)
    elif choice == "2":
        start_checking_repos_from_list(session)
    else:
        print("Invalid input!")
