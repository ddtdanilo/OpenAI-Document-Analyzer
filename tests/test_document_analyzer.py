"""Unit tests for the document analyzer functionality."""
import pytest
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from openai import OpenAI
from scripts.document_analyzer import DocumentAnalyzer


@pytest.fixture
def document_analyzer(mock_env_vars):
    """Create a DocumentAnalyzer instance for testing."""
    return DocumentAnalyzer(api_key="test-api-key")


class TestDocumentAnalyzer:
    """Test class for DocumentAnalyzer."""
    
    def test_document_analyzer_initialization(self, document_analyzer):
        """Test DocumentAnalyzer initialization."""
        assert document_analyzer.client is not None
        assert isinstance(document_analyzer.client, OpenAI)
        assert document_analyzer.default_model in DocumentAnalyzer.AVAILABLE_MODELS
    
    @pytest.mark.asyncio
    async def test_analyze_text(self, document_analyzer):
        """Test text analysis functionality."""
        test_text = "This is a test document for analysis."
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Test analysis result"))]
        
        with patch.object(document_analyzer.client.chat.completions, 'create', return_value=mock_response):
            result = await document_analyzer.analyze_text(test_text)
            assert result == "Test analysis result"
    
    def test_load_text_txt_file(self, document_analyzer, test_data_dir):
        """Test loading text from .txt file."""
        # Create test data directory if it doesn't exist
        test_data_dir.mkdir(exist_ok=True)
        
        # Create a test text file
        test_txt_path = test_data_dir / "test.txt"
        test_content = "This is test content"
        test_txt_path.write_text(test_content)
        
        try:
            result = document_analyzer.load_text(test_txt_path)
            assert result == test_content
        finally:
            # Cleanup
            if test_txt_path.exists():
                test_txt_path.unlink()
    
    def test_load_text_file_not_found(self, document_analyzer):
        """Test error handling for non-existent file."""
        with pytest.raises(FileNotFoundError):
            document_analyzer.load_text("nonexistent.txt")
    
    def test_load_text_unsupported_extension(self, document_analyzer, test_data_dir):
        """Test error handling for unsupported file extension."""
        test_data_dir.mkdir(exist_ok=True)
        test_file = test_data_dir / "test.doc"
        test_file.write_text("content")
        
        try:
            with pytest.raises(ValueError, match="Unsupported file extension"):
                document_analyzer.load_text(test_file)
        finally:
            if test_file.exists():
                test_file.unlink()
    
    @patch('scripts.document_analyzer.pypdf')
    def test_extract_text_from_pdf(self, mock_pypdf, document_analyzer, test_data_dir):
        """Test PDF text extraction."""
        # Create test data directory if it doesn't exist
        test_data_dir.mkdir(exist_ok=True)
        
        # Create a mock PDF file
        test_pdf_path = test_data_dir / "test.pdf"
        test_pdf_path.write_bytes(b"fake pdf content")
        
        # Mock pypdf
        mock_page = Mock()
        mock_page.extract_text.return_value = "Extracted PDF text"
        mock_reader = Mock()
        mock_reader.pages = [mock_page]
        mock_pypdf.PdfReader.return_value = mock_reader
        
        try:
            result = document_analyzer.extract_text_from_pdf(test_pdf_path)
            assert result == "Extracted PDF text"
        finally:
            # Cleanup
            if test_pdf_path.exists():
                test_pdf_path.unlink()
    
    @pytest.mark.asyncio
    async def test_analyze_document(self, document_analyzer, test_data_dir):
        """Test complete document analysis workflow."""
        # Create test data directory if it doesn't exist
        test_data_dir.mkdir(exist_ok=True)
        
        # Create a test text file
        test_txt_path = test_data_dir / "test.txt"
        test_content = "This is test document content"
        test_txt_path.write_text(test_content)
        
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Test analysis result"))]
        
        try:
            with patch.object(document_analyzer.client.chat.completions, 'create', return_value=mock_response):
                result = await document_analyzer.analyze_document(test_txt_path)
                assert result == "Test analysis result"
        finally:
            # Cleanup
            if test_txt_path.exists():
                test_txt_path.unlink()
    
    def test_ask_questions(self, document_analyzer):
        """Test the ask_questions method."""
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Test question response"))]
        
        with patch.object(document_analyzer.client.chat.completions, 'create', return_value=mock_response):
            result = document_analyzer.ask_questions(
                prompt="What is the main theme?",
                example_prompt="Example question",
                example_response="Example answer",
                text_to_analyze="Test text to analyze"
            )
            assert result == "Test question response" 
