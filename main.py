import url_parser
import preprocessor
from graph import graph


def main():

    url = input("Enter GitHub repository URL: ")

    parsed = url_parser.parse_url(url)

    owner = parsed["owner"]
    repo = parsed["repo"]
    branch = parsed["branch"]

    files = preprocessor.preprocess(owner, repo, branch, 1000)

    result = graph.invoke({"repo": files, "architecture_review": "", "code_quality_review": ""})

    print("\nArchitecture Review: \n")
    print(result["architecture_review"])

    print("\nCode Quality Review: \n")
    print(result["code_quality_review"])


if __name__ == "__main__":
    main()
