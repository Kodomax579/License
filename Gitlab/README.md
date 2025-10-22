from pathlib import Path

readme_content = """# GitLab License Checker

A Python script that checks GitLab repositories for their licenses.

## Function
- Checks a **single GitLab repository** for a license  
  - Example: `https://gitlab.insight-centre.org/{group}/{project}`
- Checks **all repositories from a group or user**  
  - Uses the GitLab API (`/groups?all_available=true`)
- Uses a **personal access token** for authentication and higher rate limits  
- Requires a manually exported SSL certificate (CA chain) for connecting to self-hosted instances (like `gitlab.{organisation}.org`)
- Handles invalid URLs or missing licenses gracefully  
- Saves all results in a text file(`gitlab_url_license.txt`)

---

## Set up

### Requirements
- Python 3.xx  
- `requests` package  

---

### Installation

Clone or download this repository and install dependencies:

```bash
pip install requests
```
### Configuration
Before starting the script, you must create three files in the same directory:
1. `personal_access_token.txt`
  - Create a Personal [Access Token](https://www.google.com/search?q=gitlab+personal+access+token&sca_esv=fbaa7d3b9c35fdd6&sxsrf=AE3TifMKcRXaJ0c6mgR_Xc5eRX4OHerN3g%3A1761049577587&ei=6Xv3aLzNI7udhbIP_6yXiQs&oq=gitla+perso&gs_lp=Egxnd3Mtd2l6LXNlcnAiC2dpdGxhIHBlcnNvKgIIADIHECMYsAIYJzIHEAAYgAQYDTIGEAAYDRgeMgYQABgNGB4yBhAAGA0YHjIGEAAYDRgeMgYQABgNGB4yBhAAGA0YHjIGEAAYDRgeMgYQABgNGB5IwDtQAFjpLXACeACQAQCYAX-gAdsKqgEEMTQuMrgBA8gBAPgBAZgCEqACrwyoAgrCAgcQIxgnGOoCwgIKECMY8AUYJxjqAsICChAjGIAEGCcYigXCAgoQABiABBhDGIoFwgIQEC4YgAQY0QMYQxjHARiKBcICBRAuGIAEwgIFEAAYgATCAgQQIxgnwgILEC4YgAQY0QMYxwHCAggQLhiABBjUAsICBxAuGIAEGArCAgcQABiABBgKwgIIEAAYgAQYywHCAgcQIxixAhgnwgIKEAAYgAQYChjLAcICCRAAGIAEGAoYDZgDEPEFACJaIXvr6aqSBwQxMi42oAfgugGyBwQxMC42uAeQDMIHBjItNi4xMsgHnQE&sclient=gws-wiz-serp) in your GitLab profile.
  - The token requires at least the `read_api` scope.
  - Copy the token and paste it into this file.
2. `gitlab_url.txt`
  - If you only want to check specific repositories, add the full URLs here, one per line
  - Example:
  ```
  https://gitlab.insight-centre.org/group1/project-a
  https://gitlab.insight-centre.org/group2/project-b
  ```
3. `certificate.txt`
  - You must manually export the trust chain (Certificate Chain) from your browser after you have logged into GitLab there
  - Instruction
    1. Open `https://gitlab.{organisation}.org` in you browser and log in
    2. Click the lock icon 🔒 in the address bar
    3. Go to "Connection is secure" (or similar wording)
    4. A window will open. Select "show Certificate"
    5. Scroll down, there are 2 links. Click on the "Certificat chain"
    6. Copy paste the content in the `certificate.txt` file