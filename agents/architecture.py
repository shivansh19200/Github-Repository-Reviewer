from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


llm = ChatOpenAI(model="gpt-4o",temperature=0)


def architecture_agent(state):

    files = state["repo"]

    file_list = ""

    for file in files:
        file_list += file["path"] + "\n"

    reviews = []

    for file in files:

        path = file["path"]

        chunks = file["content"]

        for chunk in chunks:

            prompt = f"""
            You are an Architecture Reviewer. This is the complete repository structure.

            Repository Files: {file_list}

            Now review ONLY this code.

            File: {path}

            Code: {chunk}

            Focus on:

            - Folder organization
            - Modularity
            - Scalability
            - Whether this file is placed properly and logically

            Keep the review short.
            """

            response = llm.invoke([HumanMessage(content=prompt)])

            reviews.append(f"""File: {path}
                           {response.content}""")

    
    final_prompt = f"""You are a senior software architect.Below are architecture reviews of different files from the same repository.
    Repository Structure:   {file_list}
    Individual Reviews: {chr("\n").join(reviews)}

    Combine them into ONE final architecture review.

    Return exactly this format:

    Architecture Score: /10

    Strengths

    Weaknesses

    Suggestions
    """

    final_response = llm.invoke([HumanMessage(content=final_prompt)])

    state["architecture_review"] = final_response.content

    return state
