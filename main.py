import os, argparse, json, sys
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_functions import available_functions, call_function

def main():

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("No API key found!")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key = api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]   

    for _ in range(20):
        chat = client.chat.completions.create(
            model = "openrouter/free",
            messages = messages,
            temperature = 0,
            tools = available_functions,
        )
        if chat.usage is None:
            raise RuntimeError("No tokens used!")
        else:
            if args.verbose:
                print(f"User prompt: {args.user_prompt}")
                print(f"Prompt tokens: {chat.usage.prompt_tokens}")
                print(f"Response tokens: {chat.usage.completion_tokens}")

        message = chat.choices[0].message
        messages.append(message)
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, args.verbose)
                messages.append(result_message)
                if not result_message["content"]:
                    raise Exception("No content found")
                if args.verbose:
                    print(f"-> {result_message['content']}")
        else:
            print(message.content)
            return

    print("Agent has reached it's iteration limit")
    sys.exit(1)


if __name__ == "__main__":
    main()
