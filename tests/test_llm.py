#!/usr/bin/env python3
"""
Simple test script to verify LLM model works
"""

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

def test_models():
    """Test different available models"""
    models = ["gpt-4.1-mini", "gpt-4.1-nano", "gemini-2.5-flash"]
    
    for model in models:
        try:
            print(f"Testing model: {model}")
            llm = ChatOpenAI(model=model, temperature=0, max_tokens=100)
            
            response = llm.invoke([HumanMessage(content="Hello, can you respond with 'Model working'?")])
            print(f"✓ {model}: {response.content}")
            return model  # Return the first working model
            
        except Exception as e:
            print(f"✗ {model}: {e}")
    
    return None

if __name__ == "__main__":
    working_model = test_models()
    if working_model:
        print(f"\nWorking model found: {working_model}")
    else:
        print("\nNo working models found")

