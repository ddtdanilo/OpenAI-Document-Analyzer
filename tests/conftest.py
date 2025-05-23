"""Pytest configuration file with common fixtures."""
import os
import warnings
import pytest
from pathlib import Path

# Configure pytest-asyncio
pytest_plugins = ("pytest_asyncio",)


def pytest_configure(config):
    """Configure pytest settings."""
    # Set asyncio mode to auto
    config.option.asyncio_mode = "auto"
    # Suppress specific warnings
    warnings.filterwarnings("ignore", category=pytest.PytestDeprecationWarning)


@pytest.fixture
def test_data_dir() -> Path:
    """Return the path to the test data directory."""
    return Path(__file__).parent / "test_data"


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Mock environment variables for testing."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-3.5-turbo") 
