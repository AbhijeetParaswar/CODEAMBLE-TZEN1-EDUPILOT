"""
Temporary patch for ragas 0.2.14 compatibility with newer langchain-community.
The import path for ChatVertexAI has changed.
"""
import sys

# Create dummy module path to satisfy ragas imports
from langchain_google_vertexai import ChatVertexAI

# Monkey patch the old import path
if 'langchain_community.chat_models' not in sys.modules:
    import types
    sys.modules['langchain_community.chat_models'] = types.ModuleType('langchain_community.chat_models')
    sys.modules['langchain_community.chat_models.vertexai'] = types.ModuleType('langchain_community.chat_models.vertexai')
    sys.modules['langchain_community.chat_models.vertexai'].ChatVertexAI = ChatVertexAI
