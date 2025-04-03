# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0


def header():
    """
    Logs the welcome message and usage guide for the tool use demo.
    """
    print("\033[0m")
    separator("=")
    print("Welcome to the triple store LLM demo!")
    separator("=")
    print(
        "This assistant provides flood analysis for user-specified locations."
    )
    print(
        "You can ask for location information by providing the location name or code and type."
    )
    print("")
    print("Example queries:")
    print("- What school zones are impacted if the levee with the code 'LEV_A_229' floods?")
    print("- What is the total population impacted if channel with the code 'CEMVK_RR_03_ONE_25' floods?")
    print("")
    print("To exit the program, simply type 'x' and press Enter.")
    print("")


def footer():
    """
    Logs the footer information for the tool use demo.
    """
    print("\033[0m")
    separator("=")
    print("Thank you for checking out the triple store demo. We hope you")
    print("learned something new, or got some inspiration for your own apps today!")
    print("")
    separator("=")


def call_to_bedrock(conversation):
    """
    Logs information about the call to Amazon Bedrock.

    :param conversation: The conversation history.
    """    
    if "toolResult" in conversation[-1]["content"][0]:
        print("\033[0;90mReturning the tool response(s) to the model...\033[0m")
    else:
        print("\033[0;90mSending the query to the model...\033[0m")
    print(conversation)

def tool_use(tool_name, input_data):
    """
    Logs information about the tool use.

    :param tool_name: The name of the tool being used.
    :param input_data: The input data for the tool.
    """
    print(f"\033[0;90mExecuting tool: {tool_name} with input: {input_data}...\033[0m")


def model_response(message):
    """
    Logs the model's response.

    :param message: The model's response message.
    """
    print("\033[0;90mThe model's response:\033[0m")
    print(message)


def separator(char="-"):
    """
    Logs a separator line.

    :param char: The character to use for the separator line.
    """
    print(char * 80)
