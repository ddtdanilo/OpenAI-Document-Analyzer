"""Unit tests for the document analyzer functionality."""
import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from openai import OpenAI
from scripts.document_analyzer import DocumentAnalyzer


@pytest.fixture
def document_analyzer(mock_env_vars):
    """Create a DocumentAnalyzer instance for testing."""
    return DocumentAnalyzer()


def test_document_analyzer_initialization(document_analyzer):
    """Test DocumentAnalyzer initialization."""
    assert document_analyzer.client is not None
    assert isinstance(document_analyzer.client, OpenAI)


@pytest.mark.asyncio
async def test_analyze_text(document_analyzer):
    """Test text analysis functionality."""
    test_text = "This is a test document for analysis."
    mock_response = Mock()
    mock_response.choices = [Mock(message=Mock(content="Test analysis result"))]
    
    with patch.object(document_analyzer.client.chat.completions, 'create', return_value=mock_response):
        result = await document_analyzer.analyze_text(test_text)
        assert result == "Test analysis result"


def test_extract_text_from_pdf(document_analyzer, test_data_dir):
    """Test PDF text extraction."""
    # Create a test PDF file
    test_pdf_path = test_data_dir / "test.pdf"
    with open(test_pdf_path, "w") as f:
        f.write("Test PDF content")
    
    try:
        text = document_analyzer.extract_text_from_pdf(test_pdf_path)
        assert isinstance(text, str)
    finally:
        # Cleanup
        if test_pdf_path.exists():
            test_pdf_path.unlink()


@pytest.mark.asyncio
async def test_analyze_document(document_analyzer, test_data_dir):
    """Test complete document analysis workflow."""
    # Create a test PDF file
    test_pdf_path = test_data_dir / "test.pdf"
    with open(test_pdf_path, "w") as f:
        f.write("Test PDF content")
    
    mock_response = Mock()
    mock_response.choices = [Mock(message=Mock(content="Test analysis result"))]
    
    try:
        with patch.object(document_analyzer.client.chat.completions, 'create', return_value=mock_response):
            result = await document_analyzer.analyze_document(test_pdf_path)
            assert result == "Test analysis result"
    finally:
        # Cleanup
        if test_pdf_path.exists():
            test_pdf_path.unlink() 
