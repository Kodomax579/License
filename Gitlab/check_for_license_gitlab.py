"""
Script to look for licenses in GitLab repos
"""
import time
import requests

result = []

def set_access_token(header):
    """Request new access token"""
    # Falls du später OAuth oder PAT benutzt:
    # header["Authorization"] = "Bearer <TOKEN>"
    return header


def request_gitlab_repo_license(project_id, original_url, request_session, request_header):
    """Request repo license info and store result"""
    start_request = time.time()
    api_url = f"https://gitlab.com/api/v4/projects/{project_id}"
    response = request_session.get(api_url, headers=request_header)

    if response.status_code == 200:
        data = response.json()
        if "license" in data and data["license"]:
            license_name = data["license"]["name"]
            result.append(f"{original_url}  --> License: {license_name}")
        else:
            result.append(f"{original_url}  --> License: not found")
    else:
        result.append(f"{original_url}  --> Error: Status {response.status_code}")

    end_request = time.time()
    print("Request time:", round(end_request - start_request, 3), "s")


def start_checking_repos(request_urls, request_session, request_header):
    """Request the users und projects"""
    start = time.time()

    for url in request_urls:
        if "gitlab.com/" not in url:
            result.append(f"{url}  --> Invalid URL")
            continue

        try:
            parts = url.split("gitlab.com/")[1].split("/")
            username = parts[0]

            # request userId
            user_resp = request_session.get(
                f"https://gitlab.com/api/v4/users?username={username}", headers=request_header
            )
            user_data = user_resp.json()
            if not user_data:
                result.append(f"{url}  --> Error: user not found")
                continue
            user_id = user_data[0]["id"]

            # request projects
            projects_resp = request_session.get(
                f"https://gitlab.com/api/v4/users/{user_id}/projects", headers=request_header
            )
            projects = projects_resp.json()

            if len(parts) > 1:
                repo_name = parts[1]
                project = next((p for p in projects if p["name"] == repo_name), None)
                if project:
                    request_gitlab_repo_license(project["id"], url, request_session, request_header)
                else:
                    result.append(f"{url}  --> Repo not found")
            else:
                for project in projects:
                    request_gitlab_repo_license(project["id"], project["web_url"], request_session, request_header)

        except Exception as e:
            result.append(f"{url}  --> Error: {e}")

    # Ergebnisse speichern
    with open("gitlab_url_license.txt", "w", encoding="utf-8") as f:
        for line in result:
            f.write(line + "\n")

    print("Total time:", round(time.time() - start, 2), "s")
    print("Done ✅")


if __name__ == "__main__":
    session = requests.Session()
    headers = {}
    headers = set_access_token(headers)

    with open("gitlab_url.txt", "r", encoding="utf-8") as file:
        urls = file.read().splitlines()

    start_checking_repos(urls, session, headers)
