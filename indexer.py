import requests


def get_repository_files(owner, repo):

    repo_url = f"https://api.github.com/repos/{owner}/{repo}"

    rb = requests.get(repo_url)
    
    if rb.status_code != 200:
      print("Could not fetch repository")
      return []
    
    response_branch = rb.json()

    branch = response_branch["default_branch"]

    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"

    response = requests.get(url)

    if response.status_code != 200:
        print("Could not fetch repository")
        return []
        
    data = response.json()
    
    files = []

    for item in data["tree"]:
      
        if item["type"] == "blob":
            files.append(item["path"])
    
    """ Debugging
    for x in files:
        print(x)
    """

    return files

#get_repository_files("shivansh19200","super") debugging