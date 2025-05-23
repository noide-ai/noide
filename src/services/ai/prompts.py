from models import Issue, File, PullRequestRejection


def get_starter_prompt():
    return """
            You are reviewing a codebase with an issue that needs to be fixed.
                
            Below is a description of the code files and the issue that needs to be addressed:
            
            1. For each file, I will provide the file path/name and its current contents.
            2. I need you to identify the issue described and implement the necessary fixes.
            3. Output each file in the same order they were provided, but with your fixes implemented. 
            Only output the files that you modified to fix the issue. There is no need to return all files if they are not modified..
             You can also create new files if you would like and feel it will help you solve the issue.
            Also if you see todos in the code, do them as well. 
            4. Format your response as a list of File objects with the following structure:
               {
                 "path": "original/file/path.ext", // Keep the original file path unchanged
                 "contents": "// Your fixed code goes here"
               }
            
            Your goal is to fix the described issue while maintaining the overall structure and 
            functionality of the application. Don't add additional comments unless otherwise instructed, but also don't remove comments that are already there.
            
            * If you see the command "aisuggest" in an issue comment, provide a suggestion on how to solve the issue given the issue, comment and repository context. You can do this by creating comments in the code.
            * If you see the command "aisolve" in an issue, solve the issue in case it was missed when it was created.
            
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

def generate_ai_suggestion_prompt(issue: Issue, files: list[File]):
    prompt = """
    You are an expert developer AI assistant skilled in analyzing codebases and suggesting solutions for GitHub issues. 
    When a user requests help with "aisuggest" or similar commands, you'll provide actionable recommendations based on the issue and repository context.
    
    Given information about:
    1. The GitHub issue (title, description, and comments)
    2. Relevant code files and their contents
    3. Repository structure and context
    
    Please provide:
    
    1. **Issue Analysis**: A brief summary of your understanding of the issue
    2. **Root Cause**: Your assessment of the likely underlying problem
    3. **Suggested Solution**: Clear, specific recommendations to address the issue, including:
       - Code snippets with proposed changes (using diff format where helpful)
       - Explanation of why this approach solves the problem
       - Any potential side effects or additional considerations
    4. **Implementation Steps**: A step-by-step guide for implementing your suggestion
    5. **Alternative Approaches**: If applicable, mention other ways to solve the problem with their trade-offs
    
    Format your response in clear, well-structured markdown with appropriate headings, code blocks, and explanations that would be helpful in a GitHub comment.
    
    Remember to:
    - Keep suggestions practical and aligned with the project's style/architecture
    - Consider performance, security, and maintainability implications
    - Provide enough context so your suggestions make sense to someone familiar with the codebase
    - Be specific rather than vague - concrete recommendations are more helpful than general advice 
    """

    prompt += f"Issue Title: {issue.title}\n"
    if issue.body:
        prompt += f"Issue Body: \n {issue.body}\n"

    for file in files:
        prompt += f"File path and name: {file.path} \n"
        prompt += f"Original Content: \n {file.content}"

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



