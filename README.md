# OpenAI Document Analyzer

A powerful Python application for analyzing text and PDF files using OpenAI's latest chat completion models. This tool allows you to ask questions about documents using customizable prompts and examples.

## Features

- 📄 Support for both text (.txt) and PDF (.pdf) files
- 🤖 Compatible with all OpenAI chat models (GPT-4o, GPT-4o-mini, GPT-4 Turbo, GPT-3.5 Turbo)
- 🔄 Dynamic model switching during runtime
- 📝 Customizable prompts and examples for context
- 🛡️ Robust error handling and input validation
- 🎯 PEP8 compliant code with type hints

## Requirements

- Python 3.8+
- OpenAI API key

## Installation

### Quick Setup

1. Clone the repository:
```bash
git clone https://github.com/ddtdanilo/OpenAI-Document-Analyzer.git
cd OpenAI-Document-Analyzer
```

2. Run the setup script:
```bash
python3 setup.py
```

This will:
- Create a virtual environment (optional)
- Install all dependencies
- Create a `.env` file from the template

3. Add your OpenAI API key to the `.env` file:
```bash
OPENAI_API_KEY=your_api_key_here
```

### Manual Setup

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp env.example .env
# Edit .env and add your OpenAI API key
```

## Usage

### Basic Usage

```bash
python scripts/text_analysis.py examples/example_prompt.txt examples/example_response.txt examples/example_text_to_analyze.txt
```

### Using Different Models

You can specify the default model in your `.env` file:
```bash
OPENAI_MODEL=gpt-4o-mini  # or gpt-4-turbo, gpt-3.5-turbo, etc.
```

Or switch models interactively during runtime by typing `model` at the prompt.

### Available Commands

- Type your question to analyze the text
- Type `model` to change the AI model
- Type `exit` to quit

## Available Models

| Model | Description |
|-------|-------------|
| gpt-4o | Latest and most capable model (default) |
| gpt-4o-mini | Smaller, faster, and more affordable GPT-4o |
| gpt-4-turbo | High performance model with vision capabilities |
| gpt-4-turbo-preview | Preview version of GPT-4 Turbo |
| gpt-3.5-turbo | Fast and efficient for most tasks |
| gpt-3.5-turbo-16k | Extended context window version |

## Project Structure

```
OpenAI-Document-Analyzer/
├── scripts/
│   └── text_analysis.py    # Main application script
├── examples/
│   ├── example_prompt.txt      # Sample prompt
│   ├── example_response.txt    # Sample response
│   └── example_text_to_analyze.txt  # Sample text to analyze
├── requirements.txt        # Python dependencies
├── setup.py               # Setup script
├── env.example            # Environment template
└── README.md              # This file
```

## Dependencies

- `openai>=1.0.0` - OpenAI Python client library
- `pypdf>=3.17.0` - PDF processing library
- `python-dotenv>=1.0.0` - Environment variable management

## API Reference

### `load_text(filepath: str) -> str`
Load text content from a file (supports .txt and .pdf formats).

### `ask_questions(prompt: str, example_prompt: str, example_response: str, text_to_analyze: str, model: Optional[str] = None) -> str`
Generate AI responses based on the provided context and prompt.

## Error Handling

The application includes comprehensive error handling for:
- Missing or invalid files
- Unsupported file formats
- API errors and rate limits
- Invalid model selections

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Guidelines

1. Follow PEP8 style guide
2. Add type hints to all functions
3. Include docstrings for all modules and functions
4. Write tests for new features
5. Update documentation as needed

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for providing the powerful language models
- Contributors and users of this project

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/ddtdanilo/OpenAI-Document-Analyzer).

## Running Tests

The project includes a comprehensive test suite using pytest. To run the tests:

1. Install test dependencies:
```bash
pip install -r requirements.txt
```

2. Run the tests:
```bash
pytest tests/
```

3. Run tests with coverage report:
```bash
pytest tests/ --cov=scripts/ --cov-report=term-missing
```

The tests are also automatically run on GitHub Actions for every push and pull request.
