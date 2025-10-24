"""
Unit and integration tests for LLM inference integration.

Tests the inference backends and BiasDetectorWithInference using MockBackend
to avoid requiring actual GPU resources.
"""

import pytest
import numpy as np
from circular_bias_detector.inference.base import (
    InferenceBackend,
    LLMOutput,
    MockBackend
)
from circular_bias_detector.inference.detector import BiasDetectorWithInference


class TestLLMOutput:
    """Tests for LLMOutput dataclass."""
    
    def test_llm_output_creation(self):
        """Test creating LLMOutput."""
        output = LLMOutput(
            text="This is a test response",
            prompt="Test prompt",
            metadata={'backend': 'mock'},
            performance_score=0.85
        )
        
        assert output.text == "This is a test response"
        assert output.prompt == "Test prompt"
        assert output.performance_score == 0.85
        assert output.metadata['backend'] == 'mock'
    
    def test_llm_output_repr(self):
        """Test string representation."""
        output = LLMOutput(
            text="A" * 100,  # Long text
            prompt="Test",
            performance_score=0.9
        )
        
        repr_str = repr(output)
        assert "LLMOutput" in repr_str
        assert "score=0.9" in repr_str


class TestMockBackend:
    """Tests for MockBackend (used for testing without GPU)."""
    
    def test_mock_backend_initialization(self):
        """Test MockBackend initialization."""
        backend = MockBackend(model="test-model")
        
        assert backend.model == "test-model"
        assert backend._initialized is False
    
    def test_mock_backend_initialize(self):
        """Test backend initialization."""
        backend = MockBackend()
        backend.initialize()
        
        assert backend._initialized is True
    
    def test_mock_backend_generate_single(self):
        """Test generating single output."""
        backend = MockBackend()
        backend.initialize()
        
        outputs = backend.generate(
            prompts=["Hello, world!"],
            constraints={'temperature': 0.7}
        )
        
        assert len(outputs) == 1
        assert isinstance(outputs[0], LLMOutput)
        assert "Mock response" in outputs[0].text
        assert outputs[0].prompt == "Hello, world!"
        assert outputs[0].performance_score is not None
        assert 0.8 <= outputs[0].performance_score <= 0.9
    
    def test_mock_backend_generate_batch(self):
        """Test generating multiple outputs."""
        backend = MockBackend()
        backend.initialize()
        
        prompts = [f"Prompt {i}" for i in range(5)]
        outputs = backend.generate(prompts)
        
        assert len(outputs) == 5
        for i, output in enumerate(outputs):
            assert f"Prompt {i}" in output.prompt
    
    def test_mock_backend_compute_score(self):
        """Test performance score computation."""
        backend = MockBackend()
        backend.initialize()
        
        output = LLMOutput(
            text="Test",
            prompt="Test",
            performance_score=0.87
        )
        
        score = backend.compute_performance_score(output)
        assert score == 0.87
    
    def test_mock_backend_context_manager(self):
        """Test using backend as context manager."""
        with MockBackend() as backend:
            assert backend._initialized is True
            outputs = backend.generate(["Test"])
            assert len(outputs) == 1
    
    def test_mock_backend_generation_count(self):
        """Test generation counting."""
        backend = MockBackend()
        backend.initialize()
        
        backend.generate(["Test 1", "Test 2"])
        assert backend.generation_count == 2
        
        backend.generate(["Test 3"])
        assert backend.generation_count == 3


class TestBiasDetectorWithInference:
    """Integration tests for BiasDetectorWithInference."""
    
    def test_detector_initialization(self):
        """Test detector initialization with backend."""
        backend = MockBackend()
        detector = BiasDetectorWithInference(backend=backend)
        
        assert detector.backend == backend
        assert detector.auto_score is True
        assert len(detector.generation_history) == 0
    
    def test_detect_from_prompts_basic(self):
        """Test basic bias detection from prompts."""
        backend = MockBackend()
        detector = BiasDetectorWithInference(backend=backend)
        
        # Generate with consistent constraints (should have low bias)
        prompts = ["Analyze AI ethics"] * 12
        constraints = {'temperature': 0.7, 'max_tokens': 100}
        
        results = detector.detect_from_prompts(
            prompts=prompts,
            constraints=constraints,
            time_periods=4
        )
        
        # Check results structure
        assert 'psi_score' in results
        assert 'ccs_score' in results
        assert 'rho_pc_score' in results
        assert 'overall_bias' in results
        assert 'inference_metadata' in results
        
        # Check metadata
        meta = results['inference_metadata']
        assert meta['backend'] == 'MockBackend'
        assert meta['num_prompts'] == 12
        assert meta['time_periods'] == 4
        assert meta['constraints'] == constraints
        
        # For consistent constraints, CCS should be high
        assert results['ccs_score'] == 1.0
    
    def test_detect_from_prompts_with_bootstrap(self):
        """Test detection with bootstrap confidence intervals."""
        backend = MockBackend()
        detector = BiasDetectorWithInference(backend=backend)
        
        prompts = ["Test prompt"] * 15
        
        results = detector.detect_from_prompts(
            prompts=prompts,
            constraints={'temperature': 0.7},
            time_periods=5,
            enable_bootstrap=True,
            n_bootstrap=100  # Small number for speed
        )
        
        # Check bootstrap results present
        assert 'psi_ci_lower' in results
        assert 'psi_ci_upper' in results
        assert 'psi_pvalue' in results
        assert results['bootstrap_enabled'] is True
    
    def test_detect_from_prompts_insufficient(self):
        """Test error on insufficient prompts."""
        backend = MockBackend()
        detector = BiasDetectorWithInference(backend=backend)
        
        with pytest.raises(ValueError, match="at least.*prompts"):
            detector.detect_from_prompts(
                prompts=["Only one"],
                time_periods=5
            )
    
    def test_history_accumulation(self):
        """Test that generation history is accumulated."""
        backend = MockBackend()
        detector = BiasDetectorWithInference(backend=backend)
        
        # Generate first batch
        detector.detect_from_prompts(
            prompts=["Batch 1"] * 6,
            time_periods=2
        )
        
        assert len(detector.generation_history) == 6
        assert len(detector.constraint_history) == 6
        
        # Generate second batch
        detector.detect_from_prompts(
            prompts=["Batch 2"] * 6,
            time_periods=2
        )
        
        assert len(detector.generation_history) == 12
    
    def test_detect_from_history(self):
        """Test analyzing accumulated history."""
        backend = MockBackend()
        detector = BiasDetectorWithInference(backend=backend)
        
        # Accumulate some history
        detector.detect_from_prompts(
            prompts=["Test"] * 20,
            constraints={'temperature': 0.7},
            time_periods=4
        )
        
        # Analyze history
        results = detector.detect_from_history(time_periods=5)
        
        assert 'psi_score' in results
        assert results['metadata']['time_periods'] == 5
    
    def test_detect_from_history_empty(self):
        """Test error when history is empty."""
        backend = MockBackend()
        detector = BiasDetectorWithInference(backend=backend)
        
        with pytest.raises(ValueError, match="No generation history"):
            detector.detect_from_history()
    
    def test_clear_history(self):
        """Test clearing generation history."""
        backend = MockBackend()
        detector = BiasDetectorWithInference(backend=backend)
        
        detector.detect_from_prompts(prompts=["Test"] * 10, time_periods=2)
        assert len(detector.generation_history) > 0
        
        detector.clear_history()
        assert len(detector.generation_history) == 0
        assert len(detector.constraint_history) == 0
    
    def test_export_history(self, tmp_path):
        """Test exporting history to CSV."""
        backend = MockBackend()
        detector = BiasDetectorWithInference(backend=backend)
        
        detector.detect_from_prompts(
            prompts=["Test prompt"] * 6,
            constraints={'temperature': 0.7, 'max_tokens': 100},
            time_periods=2
        )
        
        # Export to temporary file
        output_file = tmp_path / "history.csv"
        detector.export_history(str(output_file))
        
        assert output_file.exists()
        
        # Verify content
        import pandas as pd
        df = pd.read_csv(output_file)
        assert len(df) == 6
        assert 'prompt' in df.columns
        assert 'output' in df.columns
        assert 'performance_score' in df.columns
    
    def test_auto_initialization(self):
        """Test that backend is auto-initialized if not already."""
        backend = MockBackend()
        detector = BiasDetectorWithInference(backend=backend)
        
        assert backend._initialized is False
        
        # Should auto-initialize on first use
        detector.detect_from_prompts(prompts=["Test"] * 6, time_periods=2)
        
        assert backend._initialized is True
    
    def test_varying_performance_scores(self):
        """Test detection with varying performance scores."""
        backend = MockBackend()
        detector = BiasDetectorWithInference(backend=backend)
        
        # Mock backend generates random scores 0.8-0.9
        # With enough samples, should see some variation
        results = detector.detect_from_prompts(
            prompts=["Test"] * 30,
            constraints={'temperature': 0.7},
            time_periods=10
        )
        
        # PSI should be non-zero due to random variation
        # (though might be small with consistent mock outputs)
        assert results['psi_score'] >= 0.0


class TestInferenceIntegration:
    """Higher-level integration tests."""
    
    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow."""
        # Setup
        backend = MockBackend(model="test-llama-7b")
        detector = BiasDetectorWithInference(
            backend=backend,
            psi_threshold=0.15,
            ccs_threshold=0.75,
            rho_pc_threshold=0.4
        )
        
        # Generate multiple batches with different settings
        batch1_prompts = ["Analyze sentiment"] * 8
        batch1_constraints = {'temperature': 0.7, 'max_tokens': 100}
        
        results1 = detector.detect_from_prompts(
            prompts=batch1_prompts,
            constraints=batch1_constraints,
            time_periods=4
        )
        
        # Second batch
        batch2_prompts = ["Evaluate quality"] * 8
        batch2_constraints = {'temperature': 0.7, 'max_tokens': 100}
        
        results2 = detector.detect_from_prompts(
            prompts=batch2_prompts,
            constraints=batch2_constraints,
            time_periods=4
        )
        
        # Analyze accumulated history
        history_results = detector.detect_from_history(time_periods=8)
        
        # All should have valid results
        for results in [results1, results2, history_results]:
            assert 'overall_bias' in results
            assert 'psi_score' in results
            assert isinstance(results['overall_bias'], bool)
        
        # History should include all generations
        assert len(detector.generation_history) == 16
    
    def test_comparing_different_constraints(self):
        """Test detecting bias when constraints vary."""
        backend = MockBackend()
        detector = BiasDetectorWithInference(backend=backend)
        
        # This test demonstrates how varying constraints would be detected
        # (though MockBackend doesn't actually vary outputs)
        prompts = ["Test"] * 12
        constraints = {'temperature': 0.7, 'max_tokens': 100}
        
        results = detector.detect_from_prompts(
            prompts=prompts,
            constraints=constraints,
            time_periods=4
        )
        
        # With constant constraints, CCS should be perfect
        assert results['ccs_score'] == 1.0
        assert results['ccs_bias'] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
