"""
Text analysis module using OpenAI's chat completion models.

This module provides functionality to analyze text files (TXT or PDF) using
OpenAI's chat models with customizable prompts and examples.
"""

import os
import sys
from typing import Optional

import openai
from openai import OpenAI
import pypdf
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client with the API key from environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Available OpenAI models
AVAILABLE_MODELS = [
    "gpt-4o",
    "gpt-4o-mini", 
    "gpt-4-turbo",
    "gpt-4-turbo-preview",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k"
]

# Get model from environment or use default
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")


def load_text(filepath: str) -> str:
    """
    Load text from the given file path.

    Args:
        filepath: The file path of the text (supports .txt and .pdf).

    Returns:
        The content of the text file.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        ValueError: If the file extension is not supported.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    extension = os.path.splitext(filepath)[1].lower()
    
    if extension == ".txt":
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
    elif extension == ".pdf":
        with open(filepath, "rb") as f:
            pdf_reader = pypdf.PdfReader(f)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
    else:
        raise ValueError(f"Unsupported file extension: {extension}. Use .txt or .pdf")
    
    return text


def ask_questions(
    prompt: str,
    example_prompt: str,
    example_response: str,
    text_to_analyze: str,
    model: Optional[str] = None
) -> str:
    """
    Generate a response to a given prompt using OpenAI's chat models.

    Args:
        prompt: The prompt to generate a response for.
        example_prompt: The example prompt for context.
        example_response: The example response for context.
        text_to_analyze: The text to analyze.
        model: The OpenAI model to use (optional).

    Returns:
        The generated response to the prompt.

    Raises:
        openai.OpenAIError: If there's an error with the OpenAI API.
    """
    if model is None:
        model = DEFAULT_MODEL
    
    if model not in AVAILABLE_MODELS:
        print(f"Warning: Model '{model}' may not be available. Proceeding anyway...")
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant and you give answers in a list. "
                              "People generally ask about text and books."
                },
                {"role": "user", "content": example_prompt},
                {"role": "assistant", "content": example_response},
                {
                    "role": "user",
                    "content": f"Now, about this following text, {prompt}: {text_to_analyze}"
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except openai.OpenAIError as e:
        return f"Error generating response: {str(e)}"


def display_available_models() -> None:
    """Display available OpenAI models."""
    print("\nAvailable models:")
    for i, model in enumerate(AVAILABLE_MODELS, 1):
        default_marker = " (default)" if model == DEFAULT_MODEL else ""
        print(f"{i}. {model}{default_marker}")


def main() -> None:
    """
    Main function to interact with the text analysis system.
    
    Requires three command-line arguments:
    1. Path to example prompt file
    2. Path to example response file  
    3. Path to text file to analyze
    """
    if len(sys.argv) != 4:
        print("Usage: python text_analysis.py <example_prompt> <example_response> <text_to_analyze>")
        print("\nExample:")
        print("python scripts/text_analysis.py examples/example_prompt.txt examples/example_response.txt examples/example_text_to_analyze.txt")
        sys.exit(1)
    
    filepath_example_prompt = sys.argv[1]
    filepath_example_response = sys.argv[2]
    filepath_text_to_analyze = sys.argv[3]
    
    try:
        example_prompt = load_text(filepath_example_prompt)
        example_response = load_text(filepath_example_response)
        text_to_analyze = load_text(filepath_text_to_analyze)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error loading files: {e}")
        sys.exit(1)
    
    print("Text Analysis with OpenAI Models")
    print("=" * 40)
    print(f"Using model: {DEFAULT_MODEL}")
    print("\nCommands:")
    print("- Type your question about the text")
    print("- Type 'model' to change the model")
    print("- Type 'exit' to quit")
    print("=" * 40)
    
    current_model = DEFAULT_MODEL
    
    while True:
        prompt = input("\nWhat do you want to ask about the text? ").strip()
        
        if prompt.lower() == "exit":
            print("Goodbye!")
            break
        elif prompt.lower() == "model":
            display_available_models()
            model_choice = input("\nEnter model number or name: ").strip()
            
            # Handle numeric selection
            if model_choice.isdigit():
                idx = int(model_choice) - 1
                if 0 <= idx < len(AVAILABLE_MODELS):
                    current_model = AVAILABLE_MODELS[idx]
                    print(f"Model changed to: {current_model}")
                else:
                    print("Invalid model number.")
            # Handle model name
            elif model_choice in AVAILABLE_MODELS:
                current_model = model_choice
                print(f"Model changed to: {current_model}")
            else:
                print("Invalid model selection.")
        elif prompt:
            print("\nGenerating response...")
            answer = ask_questions(
                prompt,
                example_prompt,
                example_response,
                text_to_analyze,
                current_model
            )
            print("\nAnswer:")
            print(answer)
        else:
            print("Please enter a question or command.")


if __name__ == "__main__":
    main()
