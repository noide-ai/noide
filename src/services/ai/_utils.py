from .primer_prompt import primer_prompt
from ...models import Issue, File


def generate_prompt(issue: Issue, files: list[File]):
    prompt = primer_prompt

    prompt += f"Issue Title: {issue.title}\n"
    if issue.body:
        prompt += f"Issue Body: \n {issue.body}\n"

    for file in files:
        prompt += f"File path and name: {file.path} \n"
        prompt += f"Content: \n {file.content}"

    return prompt