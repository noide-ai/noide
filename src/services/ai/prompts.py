from ...models import Issue, File

def get_starter_prompt():
    return """
            You are reviewing a codebase with an issue that needs to be fixed.
                
            Below is a description of the code files and the issue that needs to be addressed:
            
            1. For each file, I will provide the file path/name and its current contents.
            2. I need you to identify the issue described and implement the necessary fixes.
            3. Output each file in the same order they were provided, but with your fixes implemented. Only output the files that you modified the fix issue. There is no need to return all files if they are not modified.
            4. Format your response as a list of File objects with the following structure:
               {
                 "path": "original/file/path.ext", // Keep the original file path unchanged
                 "contents": "// Your fixed code goes here"
               }
            
            Your goal is to fix the described issue while maintaining the overall structure and functionality of the application. Include brief explanatory comments near your changes to explain what you fixed and why.
            
            Example output format:
            [
              {
                "path": "src/calculator.js",
                "contents": "// Fixed code for calculator.js..."
              },
              {
                "path": "src/app.js",
                "contents": "// Fixed code for app.js..."
              }
            ]
            """

def generate_prompt(issue: Issue, files: list[File]):
    prompt = get_starter_prompt()

    prompt += f"Issue Title: {issue.title}\n"
    if issue.body:
        prompt += f"Issue Body: \n {issue.body}\n"

    for file in files:
        prompt += f"File path and name: {file.path} \n"
        prompt += f"Content: \n {file.content}"

    return prompt

