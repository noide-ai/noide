from datetime import datetime

from openai import OpenAI

from src.config import OPENAI_API_KEY
from src.models import File, Issue


class IssueSolver():
    def __init__(self):
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)

    def generate_prompt(self, issue: Issue, files: list[File]):
        prompt = ("Below is a description of a list of coding files. As well as an issue. \n "
                  "IGNORE THE ISSUE FOR NOW \n"
                  "For each file, I will provide the file name and path and its contents. \n"
                  "Can you output each file and contents in the same order, but rewrite each content with some random function. \n"
                  "Output this as a JSON, where each key is the file/path name and the value is the contents \n")

        prompt += f"Issue Title: {issue.title}\n"
        prompt += f"Issue Body: \n {issue.body}\n"

        prompt += issue.body

        for file in files:
            prompt += f"File path and name: {file.path} \n"
            prompt += f"Content: \n {file.content}"

        return prompt

    def generate_response(self, files: list[File]):
        prompt = self.generate_prompt(files)

        response = self.openai_client.responses.create(
            model="gpt-4o-mini",
            input=prompt,
        )

        return response.output_text

    def solve_issue(self, issue: Issue, files: list[File]):
        res = []
        for file in files:
            file.content = f"Hello World + {datetime.now()}"
            res.append(file)

        return res

if __name__ == '__main__':
    issue_solver = IssueSolver()

    issue = Issue(title="Issue Title", body="Issue Body")
    file1 = File(path="file1.py", content="Hello World")
    file2 = File(path="fil2.py", content="Hello World 2")

    file_list = [file1, file2]

    # res = issue_solver.generate_response(file_list)
    # print(res)
    prompt = issue_solver.generate_prompt(issue, file_list)
    print(prompt)
