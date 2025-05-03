from openai import OpenAI

from src.services.ai._utils import generate_prompt
from ...models import Issue, File, FileList
from .test_objects import test_issue, test_file_list

class IssueSolver:
    _openai_api_key: str | None = None

    @classmethod
    def setup(cls, openai_api_key: str):
        cls._openai_api_key = openai_api_key

    def __init__(self):
        self.openai_client = OpenAI(api_key=self._openai_api_key)

    def solve_issues(self, issue: Issue, files: list[File]):
        prompt = generate_prompt(issue, files)

        response = self.openai_client.responses.parse(
            model="gpt-4o-mini",
            input=prompt,
            text_format=FileList
        )

        res = response.output_parsed

        return res


if __name__ == '__main__':
    issue_solver = IssueSolver()

    issue = Issue(title="Issue Title", body="Issue Body")
    file1 = File(path="file1.py", content="Hello World")
    file2 = File(path="fil2.py", content="Hello World 2")

    file_list = [file1, file2]

    # res = issue_solver.generate_response(file_list)
    # print(res)
    test_response = issue_solver.solve_issues(test_issue, test_file_list)
    print(test_response)
