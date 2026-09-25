import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI

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

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0,
    )
    if response.usage == None:
        raise RuntimeError("Usage is None")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    print(response.choices[0].message.content)




if __name__ == "__main__":
    main()
