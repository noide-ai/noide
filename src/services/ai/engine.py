from openai import OpenAI

from services.ai.prompts import generate_resolve_issue_prompt, generate_resolve_pull_request_rejection_prompt
from models import Issue, File, FileList, PullRequestRejection


class IssueSolver:
    _openai_api_key: str | None = None
    _ai_model: str | None = None

    @classmethod
    def setup(cls, openai_api_key: str, ai_model: str):
        cls._openai_api_key = openai_api_key
        cls.openai_client = OpenAI(api_key=cls._openai_api_key)
        cls.ai_model = ai_model

    def solve_issues(self, issue: Issue, files: list[File]):
        prompt = generate_resolve_issue_prompt(issue, files)

        response = self.openai_client.responses.parse(
            model=self.ai_model,
            input=prompt,
            text_format=FileList
        )

        return response.output_parsed

    def resolve_pull_request_rejection(self, issue: Issue, original_files: list[File], modified_files: list[File], rejection: PullRequestRejection):
        prompt = generate_resolve_pull_request_rejection_prompt(issue=issue, original_files=original_files, modified_files=modified_files, rejection=rejection)

        response = self.openai_client.responses.parse(
            model=self.ai_model,
            input=prompt,
            text_format=FileList
        )

        return response.output_parsed




