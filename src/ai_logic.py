from openai import OpenAI

class IssueSolver():
    def __init__(self):
        self.openai_client = OpenAI()

    def generate_response(self, prompt):
        response = self.openai_client.responses.create(
            model="gpt-4o-mini",
            input=prompt,
        )
        return response


if __name__ == '__main__':
    issue_solver = IssueSolver()
    prompt = "What is 2 + 2?"
    res = issue_solver.generate_response(prompt)
    print(res)