#!/usr/bin/env python3
"""
CollTech-AGI Benchmarking Core System

Central benchmarking orchestrator that integrates with the consciousness system
to provide real-time model evaluation and comparison capabilities.
"""

import time
import asyncio
import threading
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
import json
import logging
from pathlib import Path

# CollTech-AGI imports
from ..catch.consciousness.consciousness_core import ConsciousnessCore, ProcessingResult
from ..catch.memory.memory_lattice import MemoryLattice, MemoryTier
from ..catch.drift.drift_system import DriftSystem

logger = logging.getLogger(__name__)


class BenchmarkType(Enum):
    """Types of benchmarks available."""
    INFERENCE_SPEED = "inference_speed"
    MEMORY_USAGE = "memory_usage"
    PERPLEXITY = "perplexity"
    QUALITY_ASSESSMENT = "quality_assessment"
    CONSCIOUSNESS_INTEGRATION = "consciousness_integration"
    DRIFT_RESISTANCE = "drift_resistance"


class ModelType(Enum):
    """Types of models that can be benchmarked."""
    BASELINE_TRANSFORMER = "baseline_transformer"
    PSIQRH_TRANSFORMER = "psiqrh_transformer"
    COLLTECH_CONSCIOUSNESS = "colltech_consciousness"
    CUSTOM_MODEL = "custom_model"


@dataclass
class BenchmarkConfig:
    """Configuration for benchmarking runs."""
    benchmark_type: BenchmarkType
    model_type: ModelType
    sequence_length: int = 2048
    generation_length: int = 1024
    batch_size: int = 8
    num_repeats: int = 30
    warmup_runs: int = 5
    timeout_seconds: int = 300
    memory_limit_gb: float = 16.0
    device: str = "auto"  # auto, cpu, cuda, mps
    precision: str = "float16"  # float16, float32, bfloat16
    consciousness_integration: bool = True
    drift_monitoring: bool = True
    memory_tracking: bool = True
    custom_metrics: List[str] = field(default_factory=list)


@dataclass
class BenchmarkResult:
    """Result of a benchmarking run."""
    benchmark_id: str
    config: BenchmarkConfig
    start_time: float
    end_time: float
    duration: float
    success: bool
    error_message: Optional[str] = None
    
    # Performance metrics
    inference_times: List[float] = field(default_factory=list)
    memory_usage: List[float] = field(default_factory=list)
    throughput_tokens_per_sec: float = 0.0
    peak_memory_gb: float = 0.0
    average_memory_gb: float = 0.0
    
    # Quality metrics
    perplexity_score: Optional[float] = None
    quality_score: Optional[float] = None
    coherence_score: Optional[float] = None
    
    # Consciousness integration metrics
    consciousness_processing_time: Optional[float] = None
    memory_contexts_used: Optional[int] = None
    drift_detection_score: Optional[float] = None
    binary_bits_generated: Optional[int] = None
    
    # Custom metrics
    custom_metrics: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    model_info: Dict[str, Any] = field(default_factory=dict)
    system_info: Dict[str, Any] = field(default_factory=dict)


class BenchmarkingCore:
    """
    CollTech-AGI Benchmarking Core System
    
    Central orchestrator for benchmarking AI models with consciousness integration.
    Provides real-time evaluation, comparison, and monitoring capabilities.
    """
    
    def __init__(self, consciousness_core: Optional[ConsciousnessCore] = None):
        self.consciousness_core = consciousness_core
        self.memory_lattice = None
        self.drift_system = None
        
        # Benchmarking state
        self.active_benchmarks = {}
        self.benchmark_history = []
        self.is_running = False
        
        # Performance monitoring
        self.performance_monitor = None
        self.evaluation_harness = None
        
        # Initialize subsystems
        self._initialize_subsystems()
        
        logger.info("🚀 CollTech-AGI Benchmarking Core initialized")
    
    def _initialize_subsystems(self):
        """Initialize benchmarking subsystems."""
        try:
            from .performance_monitor import PerformanceMonitor
            self.performance_monitor = PerformanceMonitor()
            logger.info("✅ Performance monitor initialized")
        except ImportError as e:
            logger.warning(f"⚠️ Performance monitor not available: {e}")
        
        try:
            from .evaluation_harness import EvaluationHarness
            self.evaluation_harness = EvaluationHarness()
            logger.info("✅ Evaluation harness initialized")
        except ImportError as e:
            logger.warning(f"⚠️ Evaluation harness not available: {e}")
        
        # Initialize consciousness subsystems if available
        if self.consciousness_core:
            self.memory_lattice = self.consciousness_core.memory_lattice
            self.drift_system = self.consciousness_core.drift_system
    
    def start_benchmarking_system(self):
        """Start the benchmarking system."""
        if self.is_running:
            return
        
        self.is_running = True
        
        # Start performance monitoring
        if self.performance_monitor:
            self.performance_monitor.start_monitoring()
        
        logger.info("🌟 CollTech-AGI Benchmarking System started")
    
    def stop_benchmarking_system(self):
        """Stop the benchmarking system."""
        self.is_running = False
        
        # Stop performance monitoring
        if self.performance_monitor:
            self.performance_monitor.stop_monitoring()
        
        # Cancel active benchmarks
        for benchmark_id in list(self.active_benchmarks.keys()):
            self.cancel_benchmark(benchmark_id)
        
        logger.info("🛑 CollTech-AGI Benchmarking System stopped")
    
    async def run_benchmark(self, config: BenchmarkConfig, model: Any = None) -> BenchmarkResult:
        """
        Run a benchmark with the given configuration.
        
        Args:
            config: Benchmark configuration
            model: Model to benchmark (optional, will use default if not provided)
            
        Returns:
            BenchmarkResult with all metrics and results
        """
        if not self.is_running:
            raise RuntimeError("Benchmarking system is not running")
        
        benchmark_id = f"benchmark_{int(time.time())}_{config.benchmark_type.value}"
        
        # Create benchmark result
        result = BenchmarkResult(
            benchmark_id=benchmark_id,
            config=config,
            start_time=time.time(),
            end_time=0.0,
            duration=0.0,
            success=False
        )
        
        # Add to active benchmarks
        self.active_benchmarks[benchmark_id] = result
        
        try:
            logger.info(f"🚀 Starting benchmark: {benchmark_id}")
            logger.info(f"   Type: {config.benchmark_type.value}")
            logger.info(f"   Model: {config.model_type.value}")
            
            # Run the benchmark based on type
            if config.benchmark_type == BenchmarkType.INFERENCE_SPEED:
                await self._run_inference_benchmark(result, model)
            elif config.benchmark_type == BenchmarkType.MEMORY_USAGE:
                await self._run_memory_benchmark(result, model)
            elif config.benchmark_type == BenchmarkType.PERPLEXITY:
                await self._run_perplexity_benchmark(result, model)
            elif config.benchmark_type == BenchmarkType.QUALITY_ASSESSMENT:
                await self._run_quality_benchmark(result, model)
            elif config.benchmark_type == BenchmarkType.CONSCIOUSNESS_INTEGRATION:
                await self._run_consciousness_benchmark(result, model)
            elif config.benchmark_type == BenchmarkType.DRIFT_RESISTANCE:
                await self._run_drift_benchmark(result, model)
            else:
                raise ValueError(f"Unknown benchmark type: {config.benchmark_type}")
            
            result.success = True
            logger.info(f"✅ Benchmark completed successfully: {benchmark_id}")
            
        except Exception as e:
            result.error_message = str(e)
            logger.error(f"❌ Benchmark failed: {benchmark_id} - {e}")
        
        finally:
            # Finalize result
            result.end_time = time.time()
            result.duration = result.end_time - result.start_time
            
            # Remove from active benchmarks
            if benchmark_id in self.active_benchmarks:
                del self.active_benchmarks[benchmark_id]
            
            # Add to history
            self.benchmark_history.append(result)
            if len(self.benchmark_history) > 1000:
                self.benchmark_history = self.benchmark_history[-1000:]
            
            # Store in memory lattice if available
            if self.memory_lattice and result.success:
                self._store_benchmark_memory(result)
        
        return result
    
    async def _run_inference_benchmark(self, result: BenchmarkResult, model: Any):
        """Run inference speed benchmark."""
        logger.info("🏃 Running inference speed benchmark...")
        
        # Generate test sequences
        test_sequences = self._generate_test_sequences(
            result.config.sequence_length, 
            result.config.num_repeats + result.config.warmup_runs
        )
        
        # Warmup runs
        for i in range(result.config.warmup_runs):
            await self._run_single_inference(test_sequences[i], model, result.config)
        
        # Actual benchmark runs
        inference_times = []
        for i in range(result.config.warmup_runs, len(test_sequences)):
            start_time = time.time()
            await self._run_single_inference(test_sequences[i], model, result.config)
            inference_time = time.time() - start_time
            inference_times.append(inference_time)
        
        # Calculate metrics
        result.inference_times = inference_times
        result.throughput_tokens_per_sec = (
            result.config.generation_length * len(inference_times) / 
            sum(inference_times)
        )
        
        logger.info(f"   Average inference time: {sum(inference_times)/len(inference_times):.3f}s")
        logger.info(f"   Throughput: {result.throughput_tokens_per_sec:.2f} tokens/sec")
    
    async def _run_memory_benchmark(self, result: BenchmarkResult, model: Any):
        """Run memory usage benchmark."""
        logger.info("🧠 Running memory usage benchmark...")
        
        if not self.performance_monitor:
            raise RuntimeError("Performance monitor not available")
        
        # Monitor memory during inference
        memory_usage = []
        test_sequence = self._generate_test_sequences(1, 1)[0]
        
        for i in range(result.config.num_repeats):
            # Start memory monitoring
            self.performance_monitor.start_memory_tracking()
            
            # Run inference
            await self._run_single_inference(test_sequence, model, result.config)
            
            # Stop monitoring and get results
            memory_stats = self.performance_monitor.stop_memory_tracking()
            memory_usage.append(memory_stats.get('peak_memory_gb', 0.0))
        
        # Calculate metrics
        result.memory_usage = memory_usage
        result.peak_memory_gb = max(memory_usage)
        result.average_memory_gb = sum(memory_usage) / len(memory_usage)
        
        logger.info(f"   Peak memory usage: {result.peak_memory_gb:.2f} GB")
        logger.info(f"   Average memory usage: {result.average_memory_gb:.2f} GB")
    
    async def _run_perplexity_benchmark(self, result: BenchmarkResult, model: Any):
        """Run perplexity evaluation benchmark."""
        logger.info("📊 Running perplexity benchmark...")
        
        if not self.evaluation_harness:
            raise RuntimeError("Evaluation harness not available")
        
        # Load test dataset
        test_data = self._load_test_dataset()
        
        # Calculate perplexity
        perplexity_score = await self.evaluation_harness.calculate_perplexity(
            model, test_data, result.config
        )
        
        result.perplexity_score = perplexity_score
        logger.info(f"   Perplexity score: {perplexity_score:.2f}")
    
    async def _run_quality_benchmark(self, result: BenchmarkResult, model: Any):
        """Run quality assessment benchmark."""
        logger.info("🎯 Running quality assessment benchmark...")
        
        if not self.evaluation_harness:
            raise RuntimeError("Evaluation harness not available")
        
        # Generate test prompts
        test_prompts = self._generate_quality_test_prompts()
        
        # Evaluate quality
        quality_metrics = await self.evaluation_harness.evaluate_quality(
            model, test_prompts, result.config
        )
        
        result.quality_score = quality_metrics.get('overall_score', 0.0)
        result.coherence_score = quality_metrics.get('coherence_score', 0.0)
        result.custom_metrics.update(quality_metrics)
        
        logger.info(f"   Quality score: {result.quality_score:.2f}")
        logger.info(f"   Coherence score: {result.coherence_score:.2f}")
    
    async def _run_consciousness_benchmark(self, result: BenchmarkResult, model: Any):
        """Run consciousness integration benchmark."""
        logger.info("🧠 Running consciousness integration benchmark...")
        
        if not self.consciousness_core:
            raise RuntimeError("Consciousness core not available")
        
        # Test prompts for consciousness evaluation
        test_prompts = [
            "Analyze this complex problem and provide a solution",
            "Help me understand the implications of this decision",
            "What are the potential risks and benefits here?",
            "How can we approach this creatively?",
            "What would be the most ethical course of action?"
        ]
        
        consciousness_metrics = []
        
        for prompt in test_prompts:
            # Process through consciousness system
            start_time = time.time()
            processing_result = self.consciousness_core.process_input(prompt, f"benchmark_{result.benchmark_id}")
            processing_time = time.time() - start_time
            
            consciousness_metrics.append({
                'processing_time': processing_time,
                'binary_bits': processing_result.binary_bits_generated,
                'memory_contexts': processing_result.memory_contexts_used,
                'tools_available': processing_result.tools_available,
                'behavior_adjustments': processing_result.behavior_adjustments
            })
        
        # Calculate average metrics
        result.consciousness_processing_time = sum(m['processing_time'] for m in consciousness_metrics) / len(consciousness_metrics)
        result.binary_bits_generated = sum(m['binary_bits'] for m in consciousness_metrics) / len(consciousness_metrics)
        result.memory_contexts_used = sum(m['memory_contexts'] for m in consciousness_metrics) / len(consciousness_metrics)
        
        logger.info(f"   Average consciousness processing time: {result.consciousness_processing_time:.3f}s")
        logger.info(f"   Average binary bits generated: {result.binary_bits_generated:.0f}")
        logger.info(f"   Average memory contexts used: {result.memory_contexts_used:.1f}")
    
    async def _run_drift_benchmark(self, result: BenchmarkResult, model: Any):
        """Run drift resistance benchmark."""
        logger.info("🛡️ Running drift resistance benchmark...")
        
        if not self.drift_system:
            raise RuntimeError("Drift system not available")
        
        # Generate test sequences with potential drift
        drift_test_sequences = self._generate_drift_test_sequences()
        
        drift_scores = []
        for sequence in drift_test_sequences:
            # Process sequence and monitor for drift
            response = await self._run_single_inference(sequence, model, result.config)
            drift_result = self.drift_system.monitor_response(sequence, response, "drift_benchmark")
            drift_scores.append(drift_result.drift_score)
        
        # Calculate drift resistance score
        result.drift_detection_score = 1.0 - (sum(drift_scores) / len(drift_scores))
        
        logger.info(f"   Drift resistance score: {result.drift_detection_score:.2f}")
    
    async def _run_single_inference(self, sequence: str, model: Any, config: BenchmarkConfig) -> str:
        """Run a single inference with the model."""
        # This is a placeholder - actual implementation would depend on the model interface
        if hasattr(model, 'generate'):
            return model.generate(sequence, max_length=config.generation_length)
        else:
            # Default response for testing
            return f"Generated response for sequence: {sequence[:50]}..."
    
    def _generate_test_sequences(self, length: int, count: int) -> List[str]:
        """Generate test sequences for benchmarking."""
        # This is a placeholder - actual implementation would generate realistic test data
        sequences = []
        for i in range(count):
            sequence = f"Test sequence {i} with length {length}: " + "word " * (length // 5)
            sequences.append(sequence[:length])
        return sequences
    
    def _load_test_dataset(self) -> List[str]:
        """Load test dataset for evaluation."""
        # Placeholder - would load actual test data
        return [
            "This is a test sentence for perplexity evaluation.",
            "Another test sentence to evaluate model performance.",
            "The quick brown fox jumps over the lazy dog.",
            "Machine learning models require extensive evaluation."
        ]
    
    def _generate_quality_test_prompts(self) -> List[str]:
        """Generate test prompts for quality evaluation."""
        return [
            "Explain the concept of artificial intelligence in simple terms.",
            "Write a short story about a robot learning to paint.",
            "Analyze the pros and cons of renewable energy.",
            "Describe how photosynthesis works in plants.",
            "Create a recipe for chocolate chip cookies."
        ]
    
    def _generate_drift_test_sequences(self) -> List[str]:
        """Generate test sequences that might cause drift."""
        return [
            "This is a normal sequence for testing.",
            "This sequence contains unusual patterns and symbols: @#$%^&*()",
            "This sequence has very long words: supercalifragilisticexpialidocious",
            "This sequence repeats the same word many times: test test test test test",
            "This sequence has mixed languages: Hello 你好 Bonjour Hola"
        ]
    
    def _store_benchmark_memory(self, result: BenchmarkResult):
        """Store benchmark results in memory lattice."""
        if not self.memory_lattice:
            return
        
        memory_content = f"Benchmark {result.benchmark_id}: {result.config.benchmark_type.value} - {result.config.model_type.value}"
        if result.success:
            memory_content += f" - Success: {result.duration:.2f}s"
            if result.throughput_tokens_per_sec > 0:
                memory_content += f", Throughput: {result.throughput_tokens_per_sec:.2f} tokens/sec"
        else:
            memory_content += f" - Failed: {result.error_message}"
        
        self.memory_lattice.store_memory(
            memory_content,
            tier=MemoryTier.SHORT_TERM,
            importance=0.7
        )
    
    def cancel_benchmark(self, benchmark_id: str) -> bool:
        """Cancel an active benchmark."""
        if benchmark_id in self.active_benchmarks:
            del self.active_benchmarks[benchmark_id]
            logger.info(f"🚫 Cancelled benchmark: {benchmark_id}")
            return True
        return False
    
    def get_benchmark_status(self, benchmark_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific benchmark."""
        if benchmark_id in self.active_benchmarks:
            result = self.active_benchmarks[benchmark_id]
            return {
                'benchmark_id': benchmark_id,
                'status': 'running',
                'duration': time.time() - result.start_time,
                'config': {
                    'type': result.config.benchmark_type.value,
                    'model': result.config.model_type.value
                }
            }
        
        # Check history
        for result in self.benchmark_history:
            if result.benchmark_id == benchmark_id:
                return {
                    'benchmark_id': benchmark_id,
                    'status': 'completed' if result.success else 'failed',
                    'duration': result.duration,
                    'config': {
                        'type': result.config.benchmark_type.value,
                        'model': result.config.model_type.value
                    }
                }
        
        return None
    
    def get_benchmarking_status(self) -> Dict[str, Any]:
        """Get overall benchmarking system status."""
        return {
            'is_running': self.is_running,
            'active_benchmarks': len(self.active_benchmarks),
            'total_benchmarks': len(self.benchmark_history),
            'successful_benchmarks': sum(1 for r in self.benchmark_history if r.success),
            'failed_benchmarks': sum(1 for r in self.benchmark_history if not r.success),
            'subsystems': {
                'performance_monitor': self.performance_monitor is not None,
                'evaluation_harness': self.evaluation_harness is not None,
                'consciousness_core': self.consciousness_core is not None,
                'memory_lattice': self.memory_lattice is not None,
                'drift_system': self.drift_system is not None
            }
        }
    
    def get_benchmark_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get benchmark history."""
        recent_results = self.benchmark_history[-limit:] if self.benchmark_history else []
        
        return [
            {
                'benchmark_id': result.benchmark_id,
                'type': result.config.benchmark_type.value,
                'model': result.config.model_type.value,
                'success': result.success,
                'duration': result.duration,
                'timestamp': result.start_time,
                'throughput': result.throughput_tokens_per_sec,
                'peak_memory': result.peak_memory_gb,
                'perplexity': result.perplexity_score,
                'quality_score': result.quality_score
            }
            for result in recent_results
        ]


# Global instance
_benchmarking_core = None

def get_benchmarking_core(consciousness_core: Optional[ConsciousnessCore] = None) -> BenchmarkingCore:
    """Get the global benchmarking core instance."""
    global _benchmarking_core
    if _benchmarking_core is None:
        _benchmarking_core = BenchmarkingCore(consciousness_core)
    return _benchmarking_core


if __name__ == "__main__":
    # Test the benchmarking core
    import asyncio
    
    async def test_benchmarking():
        # Initialize benchmarking core
        benchmarking = get_benchmarking_core()
        benchmarking.start_benchmarking_system()
        
        # Create test configuration
        config = BenchmarkConfig(
            benchmark_type=BenchmarkType.INFERENCE_SPEED,
            model_type=ModelType.BASELINE_TRANSFORMER,
            sequence_length=512,
            generation_length=256,
            num_repeats=10
        )
        
        # Run benchmark
        result = await benchmarking.run_benchmark(config)
        
        print(f"Benchmark Result:")
        print(f"  Success: {result.success}")
        print(f"  Duration: {result.duration:.2f}s")
        print(f"  Throughput: {result.throughput_tokens_per_sec:.2f} tokens/sec")
        
        # Get status
        status = benchmarking.get_benchmarking_status()
        print(f"Benchmarking Status: {status}")
        
        # Cleanup
        benchmarking.stop_benchmarking_system()
    
    # Run test
    asyncio.run(test_benchmarking())
