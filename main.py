import argparse
import os
import sys
from unittest import result

from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions, call_function
from prompts import system_prompt


def main():

    parser = argparse.ArgumentParser(description="Ai agent")
    parser.add_argument("user_prompt", type=str, help="Enter your prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY not set")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user","content": args.user_prompt},
    ]
    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            temperature=0,
            tools=available_functions,
        )
        if response.usage == None:
            raise RuntimeError("Usage is None")
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, args.verbose)
                if result_message.get("content") == None:
                    raise Exception("content is empty")
                if args.verbose:
                    print(f"-> {result_message['content']}")
                messages.append(result_message)
        else:
            print(f"{message.content}")
            break
    else:
        print("Maximum iterations (20) reached")
        sys.exit(1)
if __name__ == "__main__":
    main()
