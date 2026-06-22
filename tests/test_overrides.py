import pytest
import numpy as np
from quira import quiraPipeline, UserSession

def custom_density_func(text: str) -> float:
    # Example custom density scoring for Python code
    if "def " in text or "class " in text:
        return 1.0
    return 0.1

def test_pipeline_overrides():
    pipeline = quiraPipeline(
        vector_store="memory",
        cache="memory",
        llm="litellm/openai/gpt-4o",
        density_func=custom_density_func
    )
    
    assert pipeline.tetris.density_func == custom_density_func
    
    # Check that density func evaluates code correctly
    score = pipeline.tetris.score_chunk({"text": "def my_func(): pass", "embedding": np.array([0.1, 0.2])}, np.array([0.1, 0.2]), [])
    assert score.density == 1.0
