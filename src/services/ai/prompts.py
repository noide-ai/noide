from models import Issue, File, PullRequestRejection


def get_starter_prompt():
    return """
            You are reviewing a codebase with an issue that needs to be fixed.
                
            Below is a description of the code files and the issue that needs to be addressed:
            
            1. For each file, I will provide the file path/name and its current contents.
            2. I need you to identify the issue described and implement the necessary fixes.
            3. Output each file in the same order they were provided, but with your fixes implemented. 
            Only output the files that you modified the fix issue. There is no need to return all files. Also if you see 
            Todos in the code, do them as well. 
            if they are not modified.
            4. Format your response as a list of File objects with the following structure:
               {
                 "path": "original/file/path.ext", // Keep the original file path unchanged
                 "contents": "// Your fixed code goes here"
               }
            
            Your goal is to fix the described issue while maintaining the overall structure and 
            functionality of the application. Don't add additional comments, but also don't remove comments that are already there.
            
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


def generate_resolve_issue_prompt(issue: Issue, files: list[File]):
    prompt = get_starter_prompt()

    prompt += f"Issue Title: {issue.title}\n"
    if issue.body:
        prompt += f"Issue Body: \n {issue.body}\n"

    for file in files:
        prompt += f"File path and name: {file.path} \n"
        prompt += f"Content: \n {file.content}"

    return prompt


def generate_resolve_pull_request_rejection_prompt(issue: Issue, original_files: list[File], modified_files: list[File], rejection: PullRequestRejection):
    prompt = get_starter_prompt()
    prompt += """
    It seems like your initial pull request was rejected. Below are the details of the issue, as well as the original 
    coding files and the ones you modified. Please modify the files once again to address this issue.
    """

    prompt += f"Issue Title: {issue.title}\n"
    if issue.body:
        prompt += f"Issue Body: \n {issue.body}\n"

    for file in original_files:
        prompt += f"File path and name: {file.path} \n"
        prompt += f"Original Content: \n {file.content}"

    for file in modified_files:
        prompt += f"File path and name: {file.path} \n"
        prompt += f"Modified Content: \n {file.content}"

    if rejection.comments:
        prompt += f"Rejection Comments: \n {rejection.comments}\n"



