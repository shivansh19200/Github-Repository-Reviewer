from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


llm = ChatOpenAI(model="gpt-4o",temperature=0)


def code_quality_agent(state):

    files = state["repo"]

    reviews = []

    for file in files:

        path = file["path"]

        chunks = file["content"]

        for chunk in chunks:

            prompt = f"""
            You are a Code Quality Reviewer.
            Review ONLY this piece of code. Assess readability, naming consistency, modularity, and general maintainability based on the actual source file 
            contents provided.

            File:
            {path}

            Code:
            {chunk}

            Focus on:

            - Readability
            - Naming
            - Modularity
            - Maintainability

            Keep the review short.
            """

            response = llm.invoke([HumanMessage(content=prompt)])

            reviews.append(f"""File: {path} 
                           Response: {response.content} \n""")

    final_prompt = f"""
    You are a senior software engineer. These are reviews of different parts of one repository:

    {"\n".join(reviews)}

    Combine everything into one final report.

    Return the following things-
    Overall Score: /10
    Strengths
    Weaknesses
    Suggestions
    """

    final_response = llm.invoke([HumanMessage(content=final_prompt)])

    state["code_quality_review"] = final_response.content

    return state
