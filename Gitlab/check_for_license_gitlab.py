"""
Script to look for licences in Github repos
"""
import time
import requests
session = requests.Session()
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"token {GITHUB_TOKEN}"
}

start = time.time()

with open('github_url.txt', 'r', encoding="UTF-8") as datei:
    urls = datei.read().splitlines()

result = []

def request_github(user, repo, original_url):
    """
    Requesting repo to look for a license
    If there is one or nothing, it will be saved
    """
    start_request = time.time()
    api_url = f"https://api.github.com/repos/{user}/{repo}"
    response = session.get(api_url,headers=headers)
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

for url in urls:
    if "github.com/" not in url:
        result.append(f"{url}  --> Invalid URL")
        continue
    try:
        part = url.split("github.com/")[1].split('/')

        if len(part) == 1:
            repos = session.get(f"https://api.github.com/users/{part[0]}/repos",headers=headers).json()
            for rep in repos:
                REPO_URL = f"https://github.com/{part[0]}/{rep['name']}"
                request_github(part[0], rep['name'], REPO_URL)
        else:
            request_github(part[0], part[1], url)
    except Exception as e:
        result.append(f"{url}  --> Error: {e}")

with open('github_url_license.txt', 'w', encoding="UTF-8") as f:
    for line in result:
        f.write(line + '\n')

end = time.time()

print("Time:", end - start)
print("Done ✅")
