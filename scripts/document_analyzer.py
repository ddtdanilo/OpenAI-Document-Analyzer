"""
Document analyzer module using OpenAI's chat completion models.

This module provides a class-based interface for analyzing documents.
"""

import os
from pathlib import Path
from typing import Optional, Union

import pypdf
from openai import OpenAI
from dotenv import load_dotenv


class DocumentAnalyzer:
    """A class for analyzing documents using OpenAI's chat models."""
    
    AVAILABLE_MODELS = [
        "gpt-4o",
        "gpt-4o-mini", 
        "gpt-4-turbo",
        "gpt-4-turbo-preview",
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-16k"
    ]
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the DocumentAnalyzer.
        
        Args:
            api_key: OpenAI API key. If None, loads from environment.
            model: Default model to use. If None, uses environment or default.
        """
        # Load environment variables
        load_dotenv()
        
        # Set up API key
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            raise ValueError("OpenAI API key not provided")
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=api_key)
        
        # Set default model
        self.default_model = model or os.getenv("OPENAI_MODEL", "gpt-4o")
    
    def extract_text_from_pdf(self, filepath: Union[str, Path]) -> str:
        """
        Extract text from a PDF file.
        
        Args:
            filepath: Path to the PDF file.
            
        Returns:
            Extracted text content.
            
        Raises:
            FileNotFoundError: If the file doesn't exist.
            ValueError: If the file is not a valid PDF.
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        try:
            with open(filepath, "rb") as f:
                pdf_reader = pypdf.PdfReader(f)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
            return text
        except Exception as e:
            raise ValueError(f"Error reading PDF file: {e}")
    
    def load_text(self, filepath: Union[str, Path]) -> str:
        """
        Load text from a file (supports .txt and .pdf).
        
        Args:
            filepath: Path to the text file.
            
        Returns:
            File content as string.
            
        Raises:
            FileNotFoundError: If the file doesn't exist.
            ValueError: If the file extension is not supported.
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        extension = filepath.suffix.lower()
        
        if extension == ".txt":
            return filepath.read_text(encoding="utf-8")
        elif extension == ".pdf":
            return self.extract_text_from_pdf(filepath)
        else:
            raise ValueError(f"Unsupported file extension: {extension}. Use .txt or .pdf")
    
    async def analyze_text(
        self,
        text: str,
        prompt: str = "Analyze this text",
        model: Optional[str] = None
    ) -> str:
        """
        Analyze text using OpenAI's chat models.
        
        Args:
            text: Text to analyze.
            prompt: Analysis prompt.
            model: Model to use (optional).
            
        Returns:
            Analysis result.
        """
        if model is None:
            model = self.default_model
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that analyzes text and documents."
                    },
                    {
                        "role": "user",
                        "content": f"{prompt}: {text}"
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error analyzing text: {e}")
    
    async def analyze_document(
        self,
        filepath: Union[str, Path],
        prompt: str = "Analyze this document",
        model: Optional[str] = None
    ) -> str:
        """
        Analyze a document file.
        
        Args:
            filepath: Path to the document.
            prompt: Analysis prompt.
            model: Model to use (optional).
            
        Returns:
            Analysis result.
        """
        text = self.load_text(filepath)
        return await self.analyze_text(text, prompt, model)
    
    def ask_questions(
        self,
        prompt: str,
        example_prompt: str,
        example_response: str,
        text_to_analyze: str,
        model: Optional[str] = None
    ) -> str:
        """
        Generate a response using example-based prompting.
        
        Args:
            prompt: The question/prompt.
            example_prompt: Example prompt for context.
            example_response: Example response for context.
            text_to_analyze: Text to analyze.
            model: Model to use (optional).
            
        Returns:
            Generated response.
        """
        if model is None:
            model = self.default_model
        
        try:
            response = self.client.chat.completions.create(
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
        except Exception as e:
            return f"Error generating response: {str(e)}" 
