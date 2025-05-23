#!/usr/bin/env python3
"""
Setup script for OpenAI Document Analyzer.

This script helps users set up the project environment.
"""

import os
import sys
import subprocess
from pathlib import Path


def create_env_file() -> None:
    """Create .env file from template if it doesn't exist."""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if env_file.exists():
        print("✓ .env file already exists")
        return
    
    if not env_example.exists():
        print("✗ env.example file not found")
        return
    
    print("Creating .env file from template...")
    env_file.write_text(env_example.read_text())
    print("✓ .env file created")
    print("\n⚠️  Please edit .env and add your OpenAI API key")


def install_dependencies() -> None:
    """Install required Python packages."""
    print("\nInstalling dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        sys.exit(1)


def verify_installation() -> None:
    """Verify that all required packages are installed."""
    print("\nVerifying installation...")
    required_packages = ["openai", "pypdf", "dotenv"]
    
    all_good = True
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is not installed")
            all_good = False
    
    if all_good:
        print("\n✅ Setup completed successfully!")
        print("\nTo run the text analysis:")
        print("python scripts/text_analysis.py examples/example_prompt.txt examples/example_response.txt examples/example_text_to_analyze.txt")
    else:
        print("\n❌ Some packages are missing. Please run: pip install -r requirements.txt")


def main() -> None:
    """Run the setup process."""
    print("OpenAI Document Analyzer - Setup")
    print("=" * 40)
    
    # Create virtual environment if needed
    if not os.path.exists("venv") and "--no-venv" not in sys.argv:
        response = input("\nCreate virtual environment? (y/N): ").strip().lower()
        if response == "y":
            print("Creating virtual environment...")
            subprocess.check_call([sys.executable, "-m", "venv", "venv"])
            print("✓ Virtual environment created")
            print("\nActivate it with:")
            if sys.platform == "win32":
                print("  venv\\Scripts\\activate")
            else:
                print("  source venv/bin/activate")
            print("\nThen run this setup script again.")
            sys.exit(0)
    
    # Create .env file
    create_env_file()
    
    # Install dependencies
    install_dependencies()
    
    # Verify installation
    verify_installation()


if __name__ == "__main__":
    main() 
