#!/usr/bin/env python3
"""
CollTech-AGI Benchmarking System Example

This example demonstrates how to use the CollTech-AGI benchmarking system
to evaluate and compare AI models with consciousness integration.
"""

import asyncio
import time
import torch
from pathlib import Path

# CollTech-AGI imports
from colltech_agi_framework import CollTechAGIAdvanced, FrameworkConfig
from src.benchmarking import (
    BenchmarkingCore, BenchmarkConfig, BenchmarkType, ModelType,
    PsiQRHModel, PsiQRHConfig, EvaluationHarness, PerformanceMonitor
)
from src.catch.tools.benchmarking_tools import BenchmarkingToolMaker


async def main():
    """Main example function demonstrating the benchmarking system."""
    print("🚀 CollTech-AGI Benchmarking System Example")
    print("=" * 60)
    
    # Initialize CollTech-AGI with advanced features
    config = FrameworkConfig(
        auto_personality_enabled=True,
        catalyst_integration_enabled=True,
        realtime_apis_enabled=True,
        memory_lattice_enabled=True,
        drift_detection_enabled=True,
        tool_making_enabled=True
    )
    
    agi = CollTechAGIAdvanced(config)
    agi.start()
    
    print("✅ CollTech-AGI Advanced Framework initialized")
    
    # Initialize benchmarking system
    print("\n🔧 Initializing Benchmarking System...")
    
    # Get consciousness core for benchmarking integration
    consciousness_core = agi.consciousness_core if hasattr(agi, 'consciousness_core') else None
    
    # Initialize benchmarking core
    benchmarking = BenchmarkingCore(consciousness_core)
    benchmarking.start_benchmarking_system()
    
    # Initialize evaluation harness
    evaluation_harness = EvaluationHarness(consciousness_core)
    
    # Initialize performance monitor
    performance_monitor = PerformanceMonitor()
    
    # Initialize benchmarking tool maker
    tool_maker = BenchmarkingToolMaker(consciousness_core)
    
    print("✅ Benchmarking system initialized")
    
    # Example 1: Create and evaluate ΨQRH model
    print("\n🧠 Example 1: ΨQRH Model Evaluation")
    print("-" * 40)
    
    # Create ΨQRH model configuration
    psiqrh_config = PsiQRHConfig(
        vocab_size=1000,
        d_model=256,
        n_heads=8,
        n_layers=6,
        max_seq_len=512,
        consciousness_aware=True,
        memory_integration=True,
        drift_resistant=True
    )
    
    # Create ΨQRH model
    psiqrh_model = PsiQRHModel(psiqrh_config)
    print(f"✅ ΨQRH Model created with {sum(p.numel() for p in psiqrh_model.parameters()):,} parameters")
    
    # Run quality assessment benchmark
    quality_config = BenchmarkConfig(
        benchmark_type=BenchmarkType.QUALITY_ASSESSMENT,
        model_type=ModelType.PSIQRH_TRANSFORMER,
        sequence_length=256,
        generation_length=128,
        num_repeats=5,
        consciousness_integration=True,
        drift_monitoring=True
    )
    
    print("🎯 Running quality assessment benchmark...")
    quality_result = await benchmarking.run_benchmark(quality_config, psiqrh_model)
    
    print(f"   Success: {quality_result.success}")
    print(f"   Duration: {quality_result.duration:.2f}s")
    print(f"   Quality Score: {quality_result.quality_score:.2f}" if quality_result.quality_score else "   Quality Score: N/A")
    print(f"   Coherence Score: {quality_result.coherence_score:.2f}" if quality_result.coherence_score else "   Coherence Score: N/A")
    
    # Example 2: Performance monitoring
    print("\n📊 Example 2: Performance Monitoring")
    print("-" * 40)
    
    # Start performance monitoring
    performance_monitor.start_monitoring(sample_interval=0.5)
    performance_monitor.start_memory_tracking()
    
    print("📈 Monitoring performance for 3 seconds...")
    
    # Simulate some work
    for i in range(3):
        # Record some metrics
        performance_monitor.record_inference_time(0.1 + i * 0.01, sequence_length=100 + i * 10)
        performance_monitor.record_throughput(1000 - i * 50, batch_size=1 + i)
        
        # Simulate model inference
        test_input = torch.randint(0, 1000, (1, 50))
        with torch.no_grad():
            _ = psiqrh_model(test_input)
        
        time.sleep(1.0)
    
    # Stop monitoring and get results
    memory_stats = performance_monitor.stop_memory_tracking()
    performance_monitor.stop_monitoring()
    
    print(f"📊 Performance Results:")
    print(f"   Peak Memory: {memory_stats.get('peak_memory_gb', 0):.2f} GB")
    print(f"   Average Memory: {memory_stats.get('average_memory_gb', 0):.2f} GB")
    print(f"   Memory Increase: {memory_stats.get('memory_increase_gb', 0):.2f} GB")
    
    # Get performance summary
    summary = performance_monitor.get_performance_summary()
    if 'inference_time' in summary:
        print(f"   Average Inference Time: {summary['inference_time']['avg']:.3f}s")
    if 'throughput' in summary:
        print(f"   Average Throughput: {summary['throughput']['avg']:.1f} tokens/sec")
    
    # Example 3: Consciousness integration evaluation
    print("\n🧠 Example 3: Consciousness Integration Evaluation")
    print("-" * 40)
    
    if consciousness_core:
        # Test consciousness integration
        consciousness_config = BenchmarkConfig(
            benchmark_type=BenchmarkType.CONSCIOUSNESS_INTEGRATION,
            model_type=ModelType.COLLTECH_CONSCIOUSNESS,
            consciousness_integration=True
        )
        
        print("🌟 Running consciousness integration benchmark...")
        consciousness_result = await benchmarking.run_benchmark(consciousness_config)
        
        print(f"   Success: {consciousness_result.success}")
        print(f"   Duration: {consciousness_result.duration:.2f}s")
        print(f"   Consciousness Processing Time: {consciousness_result.consciousness_processing_time:.3f}s" if consciousness_result.consciousness_processing_time else "   Consciousness Processing Time: N/A")
        print(f"   Binary Bits Generated: {consciousness_result.binary_bits_generated:.0f}" if consciousness_result.binary_bits_generated else "   Binary Bits Generated: N/A")
        print(f"   Memory Contexts Used: {consciousness_result.memory_contexts_used:.1f}" if consciousness_result.memory_contexts_used else "   Memory Contexts Used: N/A")
    else:
        print("⚠️ Consciousness core not available for integration testing")
    
    # Example 4: Benchmarking tools
    print("\n🔧 Example 4: Benchmarking Tools")
    print("-" * 40)
    
    # Create benchmarking tools
    print("🔨 Creating benchmarking tools...")
    
    model_eval_tool = tool_maker.create_model_evaluation_tool("psiqrh")
    perf_monitor_tool = tool_maker.create_performance_monitoring_tool()
    consciousness_tool = tool_maker.create_consciousness_integration_tool()
    
    # List available tools
    tools = tool_maker.list_tools()
    print(f"📋 Available Tools ({len(tools)}):")
    for tool in tools:
        print(f"   - {tool['name']} ({tool['category']})")
    
    # Execute a tool
    print("\n🚀 Executing performance monitoring tool...")
    tool_result = tool_maker.execute_tool(
        perf_monitor_tool.id,
        duration=2,
        sample_interval=0.5
    )
    
    print(f"   Monitoring Duration: {tool_result.get('monitoring_duration', 'N/A')}s")
    print(f"   Sample Interval: {tool_result.get('sample_interval', 'N/A')}s")
    
    # Example 5: Model comparison
    print("\n⚖️ Example 5: Model Comparison")
    print("-" * 40)
    
    # Create baseline model for comparison
    class BaselineModel:
        def __init__(self):
            self.name = "BaselineModel"
        
        def generate(self, input_ids, max_length=100, temperature=0.8):
            return torch.randint(0, 1000, (input_ids.size(0), max_length))
    
    baseline_model = BaselineModel()
    
    # Run comparison benchmarks
    print("🔄 Running comparison benchmarks...")
    
    # ΨQRH model benchmark
    psiqrh_benchmark = BenchmarkConfig(
        benchmark_type=BenchmarkType.INFERENCE_SPEED,
        model_type=ModelType.PSIQRH_TRANSFORMER,
        sequence_length=256,
        generation_length=128,
        num_repeats=5
    )
    
    psiqrh_result = await benchmarking.run_benchmark(psiqrh_benchmark, psiqrh_model)
    
    # Baseline model benchmark
    baseline_benchmark = BenchmarkConfig(
        benchmark_type=BenchmarkType.INFERENCE_SPEED,
        model_type=ModelType.BASELINE_TRANSFORMER,
        sequence_length=256,
        generation_length=128,
        num_repeats=5
    )
    
    baseline_result = await benchmarking.run_benchmark(baseline_benchmark, baseline_model)
    
    # Compare results
    print(f"📊 Comparison Results:")
    print(f"   ΨQRH Model:")
    print(f"     Success: {psiqrh_result.success}")
    print(f"     Duration: {psiqrh_result.duration:.2f}s")
    print(f"     Throughput: {psiqrh_result.throughput_tokens_per_sec:.1f} tokens/sec")
    print(f"     Peak Memory: {psiqrh_result.peak_memory_gb:.2f} GB")
    
    print(f"   Baseline Model:")
    print(f"     Success: {baseline_result.success}")
    print(f"     Duration: {baseline_result.duration:.2f}s")
    print(f"     Throughput: {baseline_result.throughput_tokens_per_sec:.1f} tokens/sec")
    print(f"     Peak Memory: {baseline_result.peak_memory_gb:.2f} GB")
    
    # Calculate performance improvement
    if psiqrh_result.success and baseline_result.success:
        throughput_improvement = ((psiqrh_result.throughput_tokens_per_sec - baseline_result.throughput_tokens_per_sec) / baseline_result.throughput_tokens_per_sec) * 100
        memory_efficiency = ((baseline_result.peak_memory_gb - psiqrh_result.peak_memory_gb) / baseline_result.peak_memory_gb) * 100
        
        print(f"\n📈 Performance Analysis:")
        print(f"   Throughput Improvement: {throughput_improvement:+.1f}%")
        print(f"   Memory Efficiency: {memory_efficiency:+.1f}%")
    
    # Example 6: Benchmark history and analysis
    print("\n📚 Example 6: Benchmark History")
    print("-" * 40)
    
    # Get benchmark history
    history = benchmarking.get_benchmark_history(limit=10)
    print(f"📋 Recent Benchmarks ({len(history)}):")
    
    for benchmark in history:
        print(f"   - {benchmark['type']} ({benchmark['model']}): {benchmark['duration']:.2f}s")
        if benchmark['throughput'] > 0:
            print(f"     Throughput: {benchmark['throughput']:.1f} tokens/sec")
        if benchmark['quality_score']:
            print(f"     Quality Score: {benchmark['quality_score']:.2f}")
    
    # Get system status
    status = benchmarking.get_benchmarking_status()
    print(f"\n📊 System Status:")
    print(f"   Total Benchmarks: {status['total_benchmarks']}")
    print(f"   Successful: {status['successful_benchmarks']}")
    print(f"   Failed: {status['failed_benchmarks']}")
    print(f"   Subsystems Available: {sum(status['subsystems'].values())}/{len(status['subsystems'])}")
    
    # Cleanup
    print("\n🧹 Cleaning up...")
    benchmarking.stop_benchmarking_system()
    agi.shutdown()
    
    print("\n✅ Benchmarking system example completed!")
    print("\n🎯 Key Features Demonstrated:")
    print("   ✅ ΨQRH Transformer model creation and evaluation")
    print("   ✅ Performance monitoring and memory tracking")
    print("   ✅ Consciousness integration evaluation")
    print("   ✅ Benchmarking tools creation and execution")
    print("   ✅ Model comparison and analysis")
    print("   ✅ Benchmark history and system status")


if __name__ == "__main__":
    # Run the example
    asyncio.run(main())
