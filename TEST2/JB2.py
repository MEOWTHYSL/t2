import os
import openai
from ghapi.all import GhApi

def generate_text(prompt):
    openai.api_key = os.environ['OPENAI_API_KEY']

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.8,
    )

    return response.choices[0].text.strip()

def main():
    # Read the GitHub token and issue event payload from environment variables
    token = os.environ['GITHUB_TOKEN']
    issue_event = os.environ['ISSUE_PAYLOAD']

    api = GhApi(token=token)
    issue = api.parse_event(issue_event)

    if issue.action == 'opened':
        prompt = f"Please provide a response to the following issue: {issue.issue.title}"
        response_text = generate_text(prompt)

        api.issues.create_comment(issue.repository.full_name, issue.issue.number, response_text)

if __name__ == "__main__":
    main()
