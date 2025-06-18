import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content 
from functions.write_file import write_file
from functions.run_python_file import run_python_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def call_function(function_call_part, verbose=False):
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }


    func_args = {"working_directory": "./calculator"}
    func_args.update(function_call_part.args)
    if function_call_part.name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    result = function_map[function_call_part.name](**func_args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result},
            )
        ],
    )

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

You may need to use multiple function calls to figure out the problem.

When you think you have the complete answer, please provide a detailed summary, a cheeful closing message, and then end the conversation. 
"""

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read the content from, relative to the working directory. This is a required parameter",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified python file, constrained to the working directiory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The name of the python file to execute. This is a required parameter, and the file extension must by .py",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The name of the file to write to. This is a required parameter"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file. This is a required parameter",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

client = genai.Client(api_key=api_key)

if len(sys.argv) <= 1:
    print("Error: expecting text argument")
    exit(1)

verbose_output = False
if (len(sys.argv) >= 3):
    if (sys.argv[2] == "--verbose"):
        verbose_output = True
genai_content = sys.argv[1]

messages = [
    types.Content(role="user", parts=[types.Part(text=genai_content)]),
]

i = 0
MAX_ITER = 20

while i < MAX_ITER:
    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))

    if verbose_output:
        print(f'User prompt: {genai_content}')
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')

    if response.function_calls == None:
        print(response.text)
        break

    else:
        for function in response.function_calls:
            if verbose_output:
                print(f"Calling function: {function.name}({function.args})")
            func_result = call_function(function, verbose_output)
            if func_result.parts[0].function_response.response == None:
                print("Fatal error: no function result")
                sys.exit(1)
            else:
                messages.append(f'I made a call to {function.name}({function.args}) and it returned: {func_result.parts[0].function_response.response}')
                if verbose_output:
                    print(f"-> {func_result.parts[0].function_response.response}")

    for candidate in response.candidates:
        for part in candidate.content.parts:
            if verbose_output:
                print(f'Content: {part.text}')
            if (part.text != None):
                messages.append(part.text)
        if verbose_output:
            print(f'Finish Reason: {candidate.finish_reason}')
            print(f'Finish Message: {candidate.finish_reason}')

    i += 1

