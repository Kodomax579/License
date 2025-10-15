# Github License Checker

A Python script that checks public GitHub repositories for their licenses.

## Function
- Checks a single GitHub repository for a license
    - Example: (`https://github.com/{name}/{repo}`)
- Checks all public repositories of a user of their licenses
    - Example: (`https://github.com/{name}`)
- Uses a personal access token to allow more API requests
- Handles errors when a URL is invalid 
- Saves all results in a text file

## Set up
### Requirement
- Python 3.xx
- `request` package

### Installation
- clone or download this repository
- install dependecies:
    - `pip install request`

### Configuration
- create two text files in the same directory as the the script
    1. `github_url.txt`
    2. `personal_access_token`
- Create a personal access token on Github
    - https://www.geeksforgeeks.org/git/how-to-generate-personal-access-token-in-github/
    - *(You only need repo access)*

## How it Works
- Write your personal access token into `personal_access_token.txt` 
    -> No extra lines, no spaces!
- Add all you GitHub URLs to `github_url.txt`
    -> One URL per line
- Run the script
    -> The console will show the request time for each repository
- A new File will be created 
    - `github_url_license.txt`
    -> It contains all URLs with their detected licenses