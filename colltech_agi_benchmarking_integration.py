#!/usr/bin/env python3
"""
CollTech-AGI Benchmarking System Integration

Complete integration of the benchmarking harness into the CollTech AI OS.
This script demonstrates the full capabilities of the integrated system.
"""

import asyncio
import time
import torch
import logging
from pathlib import Path

# CollTech-AGI Framework imports
from colltech_agi_framework import CollTechAGIAdvanced, FrameworkConfig

# Benchmarking system imports
from src.benchmarking import (
    BenchmarkingCore, BenchmarkConfig, BenchmarkType, ModelType,
    PsiQRHModel, PsiQRHConfig, EvaluationHarness, PerformanceMonitor
)
from src.catch.tools.benchmarking_tools import BenchmarkingToolMaker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CollTechAGIBenchmarkingIntegration:
    """
    Complete integration of benchmarking system into CollTech-AGI.
    
    This class provides a unified interface for using the benchmarking
    system within the CollTech-AGI consciousness architecture.
    """
    
    def __init__(self, config: FrameworkConfig = None):
        """Initialize the integrated system."""
        self.config = config or FrameworkConfig(
            auto_personality_enabled=True,
            catalyst_integration_enabled=True,
            realtime_apis_enabled=True,
            memory_lattice_enabled=True,
            drift_detection_enabled=True,
            tool_making_enabled=True
        )
        
        # Initialize CollTech-AGI
        self.agi = CollTechAGIAdvanced(self.config)
        
        # Initialize benchmarking components
        self.benchmarking_core = None
        self.evaluation_harness = None
        self.performance_monitor = None
        self.tool_maker = None
        
        # System state
        self.is_initialized = False
        self.is_running = False
        
        logger.info("🚀 CollTech-AGI Benchmarking Integration initialized")
    
    async def initialize(self):
        """Initialize all systems."""
        if self.is_initialized:
            return
        
        logger.info("🔧 Initializing CollTech-AGI Benchmarking Integration...")
        
        # Start CollTech-AGI
        self.agi.start()
        logger.info("✅ CollTech-AGI Advanced Framework started")
        
        # Initialize benchmarking core with consciousness integration
        consciousness_core = getattr(self.agi, 'consciousness_core', None)
        self.benchmarking_core = BenchmarkingCore(consciousness_core)
        self.benchmarking_core.start_benchmarking_system()
        logger.info("✅ Benchmarking Core started")
        
        # Initialize evaluation harness
        self.evaluation_harness = EvaluationHarness(consciousness_core)
        logger.info("✅ Evaluation Harness initialized")
        
        # Initialize performance monitor
        self.performance_monitor = PerformanceMonitor()
        logger.info("✅ Performance Monitor initialized")
        
        # Initialize tool maker
        self.tool_maker = BenchmarkingToolMaker(consciousness_core)
        logger.info("✅ Benchmarking Tool Maker initialized")
        
        self.is_initialized = True
        self.is_running = True
        
        logger.info("🌟 CollTech-AGI Benchmarking Integration fully initialized")
    
    async def create_psiqrh_model(self, config: PsiQRHConfig = None) -> PsiQRHModel:
        """Create a ΨQRH model with consciousness integration."""
        if not self.is_initialized:
            await self.initialize()
        
        if config is None:
            config = PsiQRHConfig(
                vocab_size=1000,
                d_model=256,
                n_heads=8,
                n_layers=6,
                max_seq_len=512,
                consciousness_aware=True,
                memory_integration=True,
                drift_resistant=True
            )
        
        model = PsiQRHModel(config)
        logger.info(f"✅ ΨQRH Model created with {sum(p.numel() for p in model.parameters()):,} parameters")
        
        return model
    
    async def run_comprehensive_evaluation(self, model: PsiQRHModel) -> dict:
        """Run comprehensive evaluation of a model."""
        if not self.is_running:
            raise RuntimeError("System not running")
        
        logger.info("🎯 Starting comprehensive model evaluation...")
        
        results = {}
        
        # 1. Quality Assessment
        logger.info("📊 Running quality assessment...")
        quality_config = BenchmarkConfig(
            benchmark_type=BenchmarkType.QUALITY_ASSESSMENT,
            model_type=ModelType.PSIQRH_TRANSFORMER,
            sequence_length=256,
            generation_length=128,
            num_repeats=5,
            consciousness_integration=True,
            drift_monitoring=True
        )
        
        quality_result = await self.benchmarking_core.run_benchmark(quality_config, model)
        results['quality_assessment'] = {
            'success': quality_result.success,
            'duration': quality_result.duration,
            'quality_score': quality_result.quality_score,
            'coherence_score': quality_result.coherence_score,
            'consciousness_processing_time': quality_result.consciousness_processing_time,
            'binary_bits_generated': quality_result.binary_bits_generated
        }
        
        # 2. Inference Speed Benchmark
        logger.info("⚡ Running inference speed benchmark...")
        speed_config = BenchmarkConfig(
            benchmark_type=BenchmarkType.INFERENCE_SPEED,
            model_type=ModelType.PSIQRH_TRANSFORMER,
            sequence_length=256,
            generation_length=128,
            num_repeats=10,
            warmup_runs=3
        )
        
        speed_result = await self.benchmarking_core.run_benchmark(speed_config, model)
        results['inference_speed'] = {
            'success': speed_result.success,
            'duration': speed_result.duration,
            'throughput_tokens_per_sec': speed_result.throughput_tokens_per_sec,
            'average_inference_time': sum(speed_result.inference_times) / len(speed_result.inference_times) if speed_result.inference_times else 0
        }
        
        # 3. Memory Usage Benchmark
        logger.info("🧠 Running memory usage benchmark...")
        memory_config = BenchmarkConfig(
            benchmark_type=BenchmarkType.MEMORY_USAGE,
            model_type=ModelType.PSIQRH_TRANSFORMER,
            sequence_length=256,
            batch_size=4,
            num_repeats=5
        )
        
        memory_result = await self.benchmarking_core.run_benchmark(memory_config, model)
        results['memory_usage'] = {
            'success': memory_result.success,
            'duration': memory_result.duration,
            'peak_memory_gb': memory_result.peak_memory_gb,
            'average_memory_gb': memory_result.average_memory_gb
        }
        
        # 4. Consciousness Integration Test
        if hasattr(self.agi, 'consciousness_core') and self.agi.consciousness_core:
            logger.info("🌟 Running consciousness integration test...")
            consciousness_config = BenchmarkConfig(
                benchmark_type=BenchmarkType.CONSCIOUSNESS_INTEGRATION,
                model_type=ModelType.COLLTECH_CONSCIOUSNESS,
                consciousness_integration=True
            )
            
            consciousness_result = await self.benchmarking_core.run_benchmark(consciousness_config)
            results['consciousness_integration'] = {
                'success': consciousness_result.success,
                'duration': consciousness_result.duration,
                'consciousness_processing_time': consciousness_result.consciousness_processing_time,
                'binary_bits_generated': consciousness_result.binary_bits_generated,
                'memory_contexts_used': consciousness_result.memory_contexts_used
            }
        
        logger.info("✅ Comprehensive evaluation completed")
        return results
    
    async def run_performance_monitoring_demo(self, duration: int = 10):
        """Demonstrate performance monitoring capabilities."""
        if not self.is_running:
            raise RuntimeError("System not running")
        
        logger.info(f"📈 Starting performance monitoring demo for {duration} seconds...")
        
        # Start monitoring
        self.performance_monitor.start_monitoring(sample_interval=0.5)
        self.performance_monitor.start_memory_tracking()
        
        # Simulate work
        start_time = time.time()
        while time.time() - start_time < duration:
            # Record some metrics
            self.performance_monitor.record_inference_time(0.1, sequence_length=100)
            self.performance_monitor.record_throughput(1000, batch_size=1)
            
            # Simulate some processing
            await asyncio.sleep(1.0)
        
        # Stop monitoring and get results
        memory_stats = self.performance_monitor.stop_memory_tracking()
        self.performance_monitor.stop_monitoring()
        
        # Get performance summary
        summary = self.performance_monitor.get_performance_summary()
        
        logger.info("📊 Performance monitoring results:")
        logger.info(f"   Peak Memory: {memory_stats.get('peak_memory_gb', 0):.2f} GB")
        logger.info(f"   Average Memory: {memory_stats.get('average_memory_gb', 0):.2f} GB")
        logger.info(f"   Memory Increase: {memory_stats.get('memory_increase_gb', 0):.2f} GB")
        
        if 'inference_time' in summary:
            logger.info(f"   Average Inference Time: {summary['inference_time']['avg']:.3f}s")
        if 'throughput' in summary:
            logger.info(f"   Average Throughput: {summary['throughput']['avg']:.1f} tokens/sec")
        
        return {
            'memory_stats': memory_stats,
            'performance_summary': summary
        }
    
    async def demonstrate_benchmarking_tools(self):
        """Demonstrate benchmarking tools capabilities."""
        if not self.is_running:
            raise RuntimeError("System not running")
        
        logger.info("🔧 Demonstrating benchmarking tools...")
        
        # Create various tools
        model_eval_tool = self.tool_maker.create_model_evaluation_tool("psiqrh")
        perf_monitor_tool = self.tool_maker.create_performance_monitoring_tool()
        consciousness_tool = self.tool_maker.create_consciousness_integration_tool()
        comparative_tool = self.tool_maker.create_comparative_analysis_tool()
        realtime_tool = self.tool_maker.create_real_time_monitoring_tool()
        
        # List available tools
        tools = self.tool_maker.list_tools()
        logger.info(f"📋 Available Tools ({len(tools)}):")
        for tool in tools:
            logger.info(f"   - {tool['name']} ({tool['category']})")
        
        # Execute performance monitoring tool
        logger.info("🚀 Executing performance monitoring tool...")
        tool_result = self.tool_maker.execute_tool(
            perf_monitor_tool.id,
            duration=3,
            sample_interval=0.5
        )
        
        logger.info(f"   Monitoring Duration: {tool_result.get('monitoring_duration', 'N/A')}s")
        logger.info(f"   Sample Interval: {tool_result.get('sample_interval', 'N/A')}s")
        
        # Test real-time monitoring
        logger.info("⏱️ Testing real-time monitoring...")
        monitor_result = self.tool_maker.execute_tool(
            realtime_tool.id,
            action="start",
            monitoring_config={"sample_interval": 0.5}
        )
        
        if "session_id" in monitor_result:
            logger.info(f"   Real-time monitoring started: {monitor_result['session_id']}")
            
            # Let it run for a bit
            await asyncio.sleep(2)
            
            # Stop monitoring
            stop_result = self.tool_maker.execute_tool(
                realtime_tool.id,
                action="stop",
                session_id=monitor_result["session_id"]
            )
            logger.info(f"   Real-time monitoring stopped: {stop_result.get('duration', 'N/A')}s")
        
        # Get system status
        status = self.tool_maker.get_system_status()
        logger.info(f"📊 Tool System Status:")
        logger.info(f"   Total Tools: {status['total_tools']}")
        logger.info(f"   Active Sessions: {status['active_sessions']}")
        logger.info(f"   Subsystems Available: {sum(status['subsystems'].values())}/{len(status['subsystems'])}")
        
        return {
            'tools_created': len(tools),
            'tool_execution_result': tool_result,
            'system_status': status
        }
    
    async def run_model_comparison(self, model1: PsiQRHModel, model2: PsiQRHModel = None):
        """Run comparison between models."""
        if not self.is_running:
            raise RuntimeError("System not running")
        
        logger.info("⚖️ Running model comparison...")
        
        # Create baseline model if not provided
        if model2 is None:
            class BaselineModel:
                def __init__(self):
                    self.name = "BaselineModel"
                
                def generate(self, input_ids, max_length=100, temperature=0.8):
                    return torch.randint(0, 1000, (input_ids.size(0), max_length))
            
            model2 = BaselineModel()
        
        # Run benchmarks for both models
        config = BenchmarkConfig(
            benchmark_type=BenchmarkType.INFERENCE_SPEED,
            model_type=ModelType.PSIQRH_TRANSFORMER,
            sequence_length=256,
            generation_length=128,
            num_repeats=5
        )
        
        # Benchmark model 1 (ΨQRH)
        logger.info("🧠 Benchmarking ΨQRH model...")
        result1 = await self.benchmarking_core.run_benchmark(config, model1)
        
        # Benchmark model 2 (Baseline)
        logger.info("📊 Benchmarking baseline model...")
        config.model_type = ModelType.BASELINE_TRANSFORMER
        result2 = await self.benchmarking_core.run_benchmark(config, model2)
        
        # Compare results
        comparison = {
            'psiqrh_model': {
                'success': result1.success,
                'duration': result1.duration,
                'throughput': result1.throughput_tokens_per_sec,
                'peak_memory': result1.peak_memory_gb
            },
            'baseline_model': {
                'success': result2.success,
                'duration': result2.duration,
                'throughput': result2.throughput_tokens_per_sec,
                'peak_memory': result2.peak_memory_gb
            }
        }
        
        # Calculate improvements
        if result1.success and result2.success:
            throughput_improvement = ((result1.throughput_tokens_per_sec - result2.throughput_tokens_per_sec) / 
                                    result2.throughput_tokens_per_sec) * 100
            memory_efficiency = ((result2.peak_memory_gb - result1.peak_memory_gb) / 
                               result2.peak_memory_gb) * 100
            
            comparison['improvements'] = {
                'throughput_improvement_percent': throughput_improvement,
                'memory_efficiency_percent': memory_efficiency
            }
        
        logger.info("📊 Comparison Results:")
        logger.info(f"   ΨQRH Model:")
        logger.info(f"     Success: {result1.success}")
        logger.info(f"     Throughput: {result1.throughput_tokens_per_sec:.1f} tokens/sec")
        logger.info(f"     Peak Memory: {result1.peak_memory_gb:.2f} GB")
        
        logger.info(f"   Baseline Model:")
        logger.info(f"     Success: {result2.success}")
        logger.info(f"     Throughput: {result2.throughput_tokens_per_sec:.1f} tokens/sec")
        logger.info(f"     Peak Memory: {result2.peak_memory_gb:.2f} GB")
        
        if 'improvements' in comparison:
            logger.info(f"   Performance Analysis:")
            logger.info(f"     Throughput Improvement: {comparison['improvements']['throughput_improvement_percent']:+.1f}%")
            logger.info(f"     Memory Efficiency: {comparison['improvements']['memory_efficiency_percent']:+.1f}%")
        
        return comparison
    
    def get_system_status(self) -> dict:
        """Get comprehensive system status."""
        status = {
            'initialized': self.is_initialized,
            'running': self.is_running,
            'agi_status': self.agi.get_advanced_status() if self.agi else None,
            'benchmarking_status': self.benchmarking_core.get_benchmarking_status() if self.benchmarking_core else None,
            'tool_system_status': self.tool_maker.get_system_status() if self.tool_maker else None
        }
        
        return status
    
    async def shutdown(self):
        """Shutdown all systems."""
        if not self.is_running:
            return
        
        logger.info("🛑 Shutting down CollTech-AGI Benchmarking Integration...")
        
        # Stop benchmarking system
        if self.benchmarking_core:
            self.benchmarking_core.stop_benchmarking_system()
        
        # Stop performance monitoring
        if self.performance_monitor:
            self.performance_monitor.stop_monitoring()
        
        # Shutdown CollTech-AGI
        if self.agi:
            self.agi.shutdown()
        
        self.is_running = False
        logger.info("✅ CollTech-AGI Benchmarking Integration shutdown complete")


async def main():
    """Main demonstration function."""
    print("🚀 CollTech-AGI Benchmarking System Integration Demo")
    print("=" * 70)
    
    # Initialize the integrated system
    integration = CollTechAGIBenchmarkingIntegration()
    
    try:
        # Initialize all systems
        await integration.initialize()
        
        # Create ΨQRH model
        print("\n🧠 Creating ΨQRH Model...")
        psiqrh_model = await integration.create_psiqrh_model()
        
        # Run comprehensive evaluation
        print("\n🎯 Running Comprehensive Evaluation...")
        evaluation_results = await integration.run_comprehensive_evaluation(psiqrh_model)
        
        print("\n📊 Evaluation Results Summary:")
        for benchmark_type, results in evaluation_results.items():
            print(f"   {benchmark_type.replace('_', ' ').title()}:")
            if results['success']:
                print(f"     Duration: {results['duration']:.2f}s")
                if 'quality_score' in results:
                    print(f"     Quality Score: {results['quality_score']:.2f}")
                if 'throughput_tokens_per_sec' in results:
                    print(f"     Throughput: {results['throughput_tokens_per_sec']:.1f} tokens/sec")
                if 'peak_memory_gb' in results:
                    print(f"     Peak Memory: {results['peak_memory_gb']:.2f} GB")
            else:
                print(f"     Status: Failed")
        
        # Demonstrate performance monitoring
        print("\n📈 Performance Monitoring Demo...")
        monitoring_results = await integration.run_performance_monitoring_demo(duration=5)
        
        # Demonstrate benchmarking tools
        print("\n🔧 Benchmarking Tools Demo...")
        tools_results = await integration.demonstrate_benchmarking_tools()
        
        # Run model comparison
        print("\n⚖️ Model Comparison Demo...")
        comparison_results = await integration.run_model_comparison(psiqrh_model)
        
        # Get final system status
        print("\n📊 Final System Status...")
        final_status = integration.get_system_status()
        
        print(f"   System Initialized: {final_status['initialized']}")
        print(f"   System Running: {final_status['running']}")
        
        if final_status['benchmarking_status']:
            bm_status = final_status['benchmarking_status']
            print(f"   Total Benchmarks: {bm_status['total_benchmarks']}")
            print(f"   Successful Benchmarks: {bm_status['successful_benchmarks']}")
            print(f"   Failed Benchmarks: {bm_status['failed_benchmarks']}")
        
        if final_status['tool_system_status']:
            tool_status = final_status['tool_system_status']
            print(f"   Total Tools: {tool_status['total_tools']}")
            print(f"   Active Sessions: {tool_status['active_sessions']}")
        
        print("\n✅ CollTech-AGI Benchmarking Integration Demo completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Demo failed: {e}")
        raise
    
    finally:
        # Cleanup
        await integration.shutdown()


if __name__ == "__main__":
    # Run the demonstration
    asyncio.run(main())
