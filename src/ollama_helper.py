# src/ollama_helper.py
"""
Ollama integration helper for data science projects
"""
import requests
import json
import os
from typing import Optional, Dict, Any


class OllamaHelper:
    def __init__(self, base_url: str = "http://ollama:11434"):
        """
        Initialize Ollama helper

        Args:
            base_url: Ollama server URL
        """
        self.base_url = base_url
        self.session = requests.Session()

    def is_available(self) -> bool:
        """Check if Ollama server is available"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def list_models(self) -> list:
        """List available models"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                return [model['name'] for model in response.json().get('models', [])]
            return []
        except requests.exceptions.RequestException:
            return []

    def pull_model(self, model: str) -> bool:
        """Pull a model from Ollama"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/pull",
                json={"name": model},
                stream=True
            )
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def ask(self, prompt: str, model: str = "llama2", **kwargs) -> Optional[str]:
        """
        Ask Ollama a question

        Args:
            prompt: The question or prompt
            model: Model to use (default: llama2)
            **kwargs: Additional parameters for the model

        Returns:
            Response text or None if error
        """
        try:
            data = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                **kwargs
            }

            response = self.session.post(
                f"{self.base_url}/api/generate",
                json=data,
                timeout=60
            )

            if response.status_code == 200:
                return response.json().get('response', '')
            return None

        except requests.exceptions.RequestException as e:
            print(f"Error asking Ollama: {e}")
            return None

    def analyze_data(self, data_summary: str, question: str = None) -> str:
        """
        Get AI assistance for data analysis

        Args:
            data_summary: Summary of your dataset
            question: Specific question about the analysis

        Returns:
            AI response with analysis suggestions
        """
        if question:
            prompt = f"""
            I have a dataset with the following characteristics:
            {data_summary}

            Question: {question}

            Please provide specific recommendations for data analysis, including:
            1. Relevant statistical tests
            2. Visualization suggestions
            3. Potential insights to look for
            4. Python code examples if applicable

            Keep the response focused and practical.
            """
        else:
            prompt = f"""
            I have a dataset with the following characteristics:
            {data_summary}

            Please suggest:
            1. Appropriate exploratory data analysis steps
            2. Statistical tests to consider
            3. Visualization techniques
            4. Potential research questions
            5. Next steps for analysis

            Provide practical, actionable advice.
            """

        return self.ask(prompt, model="llama2")

    def code_review(self, code: str, context: str = "") -> str:
        """
        Get code review and suggestions

        Args:
            code: Python code to review
            context: Context about what the code does

        Returns:
            AI feedback on the code
        """
        prompt = f"""
        Please review this Python data science code:

        Context: {context}

        Code:
        ```python
        {code}
        ```

        Please provide:
        1. Code quality feedback
        2. Performance suggestions
        3. Best practices recommendations
        4. Potential bugs or issues
        5. Alternative approaches

        Focus on practical improvements.
        """

        return self.ask(prompt, model="llama2")


# Convenience functions for Jupyter notebooks
def setup_ollama(model: str = "llama2") -> OllamaHelper:
    """Setup Ollama helper and ensure model is available"""
    ollama = OllamaHelper()

    if not ollama.is_available():
        print("❌ Ollama server not available. Please start Ollama first.")
        return ollama

    models = ollama.list_models()
    if model not in models:
        print(f"📥 Pulling {model} model...")
        if ollama.pull_model(model):
            print(f"✅ {model} model ready!")
        else:
            print(f"❌ Failed to pull {model} model")
    else:
        print(f"✅ {model} model already available!")

    return ollama


def ask_ai(prompt: str, model: str = "llama2") -> str:
    """Quick function to ask AI a question"""
    ollama = OllamaHelper()
    response = ollama.ask(prompt, model)
    return response if response else "Sorry, I couldn't get a response from the AI."


# Example usage in notebooks:
"""
# In your Jupyter notebook:
from src.ollama_helper import setup_ollama, ask_ai

# Setup
ai = setup_ollama("llama2")

# Ask for analysis help
data_info = f"Dataset shape: {df.shape}, Columns: {list(df.columns)}"
suggestion = ai.analyze_data(data_info, "What statistical tests should I run?")
print(suggestion)

# Quick questions
response = ask_ai("What's the best way to handle missing values in time series data?")
print(response)
"""