from datetime import datetime

from openai import OpenAI

from src.config import OPENAI_API_KEY
from src.models import File, Issue


class IssueSolver():
    def __init__(self):
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)

    def generate_response(self, prompt):
        response = self.openai_client.responses.create(
            model="gpt-4o-mini",
            input=prompt,
        )
        return response

    def solve_issue(self, issue: Issue, files: list[File]):
        res = []
        for file in files:
            file.content = f"Hello World + {datetime.now()}"
            res.append(file)

        return res

if __name__ == '__main__':
    issue_solver = IssueSolver()
    prompt = "What is 2 + 2?"
    res = issue_solver.generate_response(prompt)
    print(res)