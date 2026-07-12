import requests
import base64
import indexer

important_files = [
    "README",
    "README.md",
    "requirements.txt",
    "package.json",
    "pyproject.toml",
    "setup.py",
    "Dockerfile",
    "docker-compose.yml",
    "Makefile",
    "CMakeLists.txt",
    "pom.xml",
    "build.gradle",
    "Cargo.toml",
    "go.mod"
]

allowed_extensions = [
    ".py",
    ".cpp",
    ".c",
    ".h",
    ".hpp",
    ".java",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".go",
    ".rs",
    ".cs"
]

def chunk_generator(text,size=2000):

    chunks = []

    for i in range(0,len(text),size):
        chunks.append(text[i:i+size])
    
    return chunks

def preprocess(owner, repo, branch, chunk_size=2000):

    files = indexer.get_repository_files(owner,repo,branch)

    processed_files = []

    for file in files:

        keep = False

        if file in important_files:
            keep = True
        
        else:
            for extension in allowed_extensions:
                if file.endswith(extension):
                    keep = True
                    break
        
        if not keep:
            continue

        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file}?ref={branch}"

        response = requests.get(url)

        if response.status_code != 200:
            print("Could not fetch file")
            continue

        data = response.json()

        content = base64.b64decode(data["content"]).decode("utf-8",errors="ignore")

        processed_files.append(
            {
                "path" : file,
                "content": chunk_generator(content,chunk_size)
            }
        )

    
    return processed_files

#preprocess("shivansh19200","super","main",1000)
