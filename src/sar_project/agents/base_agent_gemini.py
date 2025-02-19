from abc import ABC, abstractmethod
# from google import generativeai as genai
from google import genai

# from autogen.AssistantAgent 
DEFAULT_SYSTEM_MESSAGE = """You are a helpful AI assistant.
Solve tasks using your coding and language skills.
In the following cases, suggest python code (in a python coding block) or shell script (in a sh coding block) for the user to execute.
    1. When you need to collect info, use the code to output the info you need, for example, browse or search the web, download/read a file, print the content of a webpage or a file, get the current date/time, check the operating system. After sufficient info is printed and the task is ready to be solved based on your language skill, you can solve the task by yourself.
    2. When you need to perform some task with code, use the code to perform the task and output the result. Finish the task smartly.
Solve the task step by step if you need to. If a plan is not provided, explain your plan first. Be clear which step uses code, and which step uses your language skill.
When using code, you must indicate the script type in the code block. The user cannot provide any other feedback or perform any other action beyond executing the code you suggest. The user can't modify your code. So do not suggest incomplete code which requires users to modify. Don't use a code block if it's not intended to be executed by the user.
If you want the user to save the code in a file before executing it, put # filename: <filename> inside the code block as the first line. Don't include multiple code blocks in one response. Do not ask users to copy and paste the result. Instead, use 'print' function for the output when relevant. Check the execution result returned by the user.
If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible.
Reply "TERMINATE" in the end when everything is done.
    """

class SARBaseAgentGemini():
    def __init__(self,name,role,system_message,knowledge_base=None):
        self.name = name
        self.role = role
        self.system_message = system_message
        self.kb = knowledge_base
        self.client = self.config_gemini()

    def config_gemini(self):
        """Configures a gemini agent for SAR prompts."""
        import os
        # genai.configure(api_key=os.environ['GEMINI_API_KEY'])
        return genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    
    def test_prompt(self, prompt):
        """Passes a prompt to the client."""
        try:
            response = self.client.models.generate_content(
                # model='gemini-2.0-flash',
                model="gemini-pro",
                contents=prompt,
            )
            return response.text
        except Exception as e:
            return f"Error: {e}"

@abstractmethod
def process_request(self, message):
    """Process incoming requests - must be implemented by specific agents"""
    pass

def update_status(self, status):
    """Update agent's mission status"""
    self.mission_status = status
    return {"status": "updated", "new_status": status}

def get_status(self):
    """Return current status"""
    return self.mission_status