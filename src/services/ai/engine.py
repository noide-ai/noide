from openai import OpenAI

from src.services.ai.prompts import generate_prompt
from ...models import Issue, File, FileList


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
