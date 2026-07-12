from urllib.parse import urlparse
import requests


def parse_url(url):
    parsed = urlparse(url)

    parts = parsed.path.strip("/").split("/")

    if len(parts) < 2:
        raise ValueError("Invalid GitHub repository URL")

    owner = parts[0]
    repo = parts[1]

    branch = None

    if len(parts) >= 4 and parts[2] == "tree":
        branch = parts[3]
    
    if branch is None:
        u = f"https://api.github.com/repos/{owner}/{repo}"

        response = requests.get(u)

        if response.status_code != 200:
            print("Invalid URL")
        
        else:
            branch = response.json()["default_branch"]

    return {
        "owner": owner,
        "repo": repo,
        "branch": branch
    }

