#!/usr/bin/env python3
"""
Test script to verify the installation and configuration.
"""

import sys
import os
from pathlib import Path


def check_python_version() -> bool:
    """Check if Python version is 3.8+."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python version {version.major}.{version.minor} is too old. Need 3.8+")
        return False


def check_dependencies() -> bool:
    """Check if all required packages are installed."""
    packages = {
        "openai": "OpenAI API client",
        "pypdf": "PDF processing",
        "dotenv": "Environment management"
    }
    
    all_good = True
    for package, description in packages.items():
        try:
            __import__(package)
            print(f"✓ {package} - {description}")
        except ImportError:
            print(f"✗ {package} - {description} (not installed)")
            all_good = False
    
    return all_good


def check_files() -> bool:
    """Check if all required files exist."""
    required_files = [
        "scripts/text_analysis.py",
        "examples/example_prompt.txt",
        "examples/example_response.txt", 
        "examples/example_text_to_analyze.txt",
        "requirements.txt",
        "env.example"
    ]
    
    all_good = True
    for file in required_files:
        if Path(file).exists():
            print(f"✓ {file}")
        else:
            print(f"✗ {file} (missing)")
            all_good = False
    
    return all_good


def check_env_config() -> bool:
    """Check environment configuration."""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("✗ .env file not found")
        print("  Run: cp env.example .env")
        print("  Then add your OpenAI API key")
        return False
    
    print("✓ .env file exists")
    
    # Check if API key is configured
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key != "your_api_key_here":
        print("✓ OpenAI API key is configured")
        return True
    else:
        print("⚠️  OpenAI API key not configured")
        print("  Edit .env and add your API key")
        return False


def main() -> None:
    """Run all checks."""
    print("OpenAI Document Analyzer - Installation Check")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Required Files", check_files),
        ("Environment Configuration", check_env_config)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\nChecking {name}...")
        results.append(check_func())
    
    print("\n" + "=" * 50)
    
    if all(results):
        print("✅ All checks passed! You're ready to use the text analysis tool.")
        print("\nRun:")
        print("python scripts/text_analysis.py examples/example_prompt.txt examples/example_response.txt examples/example_text_to_analyze.txt")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        if not results[1]:  # Dependencies check
            print("\nInstall dependencies with:")
            print("pip install -r requirements.txt")


if __name__ == "__main__":
    main() 
