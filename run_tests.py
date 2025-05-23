#!/usr/bin/env python3
"""
Script to run tests for OpenAI Document Analyzer.
"""

import subprocess
import sys
from pathlib import Path


def run_tests() -> None:
    """Run the test suite with coverage."""
    print("OpenAI Document Analyzer - Running Tests")
    print("=" * 40)
    
    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Not running in a virtual environment.")
        print("   It's recommended to activate your virtual environment first:")
        print("   source venv/bin/activate")
        print("")
    
    # Check if pytest is installed
    try:
        import pytest
    except ImportError:
        print("❌ pytest not found. Please install dependencies:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Run tests with coverage
    print("\n🧪 Running tests with coverage report...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", 
            "--cov=scripts/", 
            "--cov-report=term-missing",
            "-v"
        ], check=True)
        
        print("\n✅ All tests passed!")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code {e.returncode}")
        sys.exit(1)


def main() -> None:
    """Main function."""
    if not Path("tests").exists():
        print("❌ Tests directory not found. Make sure you're in the project root.")
        sys.exit(1)
    
    run_tests()


if __name__ == "__main__":
    main() 
