#!/usr/bin/env python3
"""
CollTech-AGI Performance Monitor

Real-time performance monitoring system for benchmarking and evaluation.
Tracks memory usage, CPU utilization, GPU metrics, and system performance.
"""

import time
import threading
import psutil
import torch
import asyncio
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Types of performance metrics."""
    MEMORY_USAGE = "memory_usage"
    CPU_USAGE = "cpu_usage"
    GPU_USAGE = "gpu_usage"
    GPU_MEMORY = "gpu_memory"
    INFERENCE_TIME = "inference_time"
    THROUGHPUT = "throughput"
    LATENCY = "latency"
    CUSTOM = "custom"


@dataclass
class PerformanceMetrics:
    """Performance metrics data structure."""
    timestamp: float
    metric_type: MetricType
    value: float
    unit: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MemoryStats:
    """Memory usage statistics."""
    total_memory_gb: float
    used_memory_gb: float
    available_memory_gb: float
    memory_percentage: float
    peak_memory_gb: float
    process_memory_gb: float
    gpu_memory_gb: Optional[float] = None
    gpu_memory_percentage: Optional[float] = None


@dataclass
class SystemStats:
    """System performance statistics."""
    cpu_percentage: float
    memory_stats: MemoryStats
    gpu_utilization: Optional[float] = None
    gpu_temperature: Optional[float] = None
    disk_usage_percentage: float = 0.0
    network_io_bytes: int = 0


class MemoryTracker:
    """Memory usage tracking system."""
    
    def __init__(self):
        self.is_tracking = False
        self.tracking_thread = None
        self.memory_samples = []
        self.peak_memory = 0.0
        self.start_memory = 0.0
        
    def start_tracking(self):
        """Start memory tracking."""
        if self.is_tracking:
            return
        
        self.is_tracking = True
        self.memory_samples = []
        self.peak_memory = 0.0
        self.start_memory = self._get_current_memory()
        
        self.tracking_thread = threading.Thread(target=self._tracking_loop)
        self.tracking_thread.daemon = True
        self.tracking_thread.start()
        
        logger.info("📊 Memory tracking started")
    
    def stop_tracking(self) -> Dict[str, float]:
        """Stop memory tracking and return statistics."""
        if not self.is_tracking:
            return {}
        
        self.is_tracking = False
        if self.tracking_thread:
            self.tracking_thread.join(timeout=5.0)
        
        if not self.memory_samples:
            return {}
        
        # Calculate statistics
        current_memory = self._get_current_memory()
        peak_memory = max(self.memory_samples) if self.memory_samples else current_memory
        average_memory = sum(self.memory_samples) / len(self.memory_samples)
        memory_increase = current_memory - self.start_memory
        
        stats = {
            'start_memory_gb': self.start_memory,
            'current_memory_gb': current_memory,
            'peak_memory_gb': peak_memory,
            'average_memory_gb': average_memory,
            'memory_increase_gb': memory_increase,
            'sample_count': len(self.memory_samples)
        }
        
        logger.info(f"📊 Memory tracking stopped - Peak: {peak_memory:.2f} GB")
        return stats
    
    def _tracking_loop(self):
        """Memory tracking loop."""
        while self.is_tracking:
            try:
                current_memory = self._get_current_memory()
                self.memory_samples.append(current_memory)
                self.peak_memory = max(self.peak_memory, current_memory)
                time.sleep(0.1)  # Sample every 100ms
            except Exception as e:
                logger.warning(f"Memory tracking error: {e}")
                time.sleep(1.0)
    
    def _get_current_memory(self) -> float:
        """Get current memory usage in GB."""
        try:
            process = psutil.Process()
            memory_bytes = process.memory_info().rss
            return memory_bytes / (1024 ** 3)  # Convert to GB
        except Exception:
            return 0.0


class GPUMonitor:
    """GPU monitoring system."""
    
    def __init__(self):
        self.gpu_available = torch.cuda.is_available()
        self.gpu_count = torch.cuda.device_count() if self.gpu_available else 0
    
    def get_gpu_stats(self) -> Dict[str, Any]:
        """Get GPU statistics."""
        if not self.gpu_available:
            return {'gpu_available': False}
        
        stats = {'gpu_available': True, 'gpu_count': self.gpu_count}
        
        try:
            for i in range(self.gpu_count):
                # Memory stats
                memory_allocated = torch.cuda.memory_allocated(i) / (1024 ** 3)
                memory_reserved = torch.cuda.memory_reserved(i) / (1024 ** 3)
                memory_total = torch.cuda.get_device_properties(i).total_memory / (1024 ** 3)
                
                stats[f'gpu_{i}'] = {
                    'memory_allocated_gb': memory_allocated,
                    'memory_reserved_gb': memory_reserved,
                    'memory_total_gb': memory_total,
                    'memory_percentage': (memory_allocated / memory_total) * 100,
                    'name': torch.cuda.get_device_name(i)
                }
        except Exception as e:
            logger.warning(f"GPU monitoring error: {e}")
        
        return stats


class PerformanceMonitor:
    """
    Comprehensive performance monitoring system.
    
    Tracks system performance, memory usage, GPU metrics, and custom metrics
    for benchmarking and evaluation purposes.
    """
    
    def __init__(self):
        self.is_monitoring = False
        self.monitoring_thread = None
        self.metrics_history = []
        self.custom_metrics = {}
        
        # Subsystems
        self.memory_tracker = MemoryTracker()
        self.gpu_monitor = GPUMonitor()
        
        # Monitoring configuration
        self.sample_interval = 1.0  # seconds
        self.max_history_size = 10000
        
        logger.info("✅ Performance Monitor initialized")
    
    def start_monitoring(self, sample_interval: float = 1.0):
        """Start performance monitoring."""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self.sample_interval = sample_interval
        self.metrics_history = []
        
        # Start monitoring thread
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        
        logger.info(f"📊 Performance monitoring started (interval: {sample_interval}s)")
    
    def stop_monitoring(self):
        """Stop performance monitoring."""
        if not self.is_monitoring:
            return
        
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=10.0)
        
        logger.info("📊 Performance monitoring stopped")
    
    def start_memory_tracking(self):
        """Start detailed memory tracking."""
        self.memory_tracker.start_tracking()
    
    def stop_memory_tracking(self) -> Dict[str, float]:
        """Stop memory tracking and return statistics."""
        return self.memory_tracker.stop_tracking()
    
    def record_metric(self, metric_type: MetricType, value: float, 
                     unit: str = "", metadata: Dict[str, Any] = None):
        """Record a custom metric."""
        metric = PerformanceMetrics(
            timestamp=time.time(),
            metric_type=metric_type,
            value=value,
            unit=unit,
            metadata=metadata or {}
        )
        
        self.metrics_history.append(metric)
        
        # Maintain history size
        if len(self.metrics_history) > self.max_history_size:
            self.metrics_history = self.metrics_history[-self.max_history_size:]
    
    def record_inference_time(self, inference_time: float, sequence_length: int = 0):
        """Record inference time metric."""
        self.record_metric(
            MetricType.INFERENCE_TIME,
            inference_time,
            "seconds",
            {"sequence_length": sequence_length}
        )
    
    def record_throughput(self, tokens_per_second: float, batch_size: int = 1):
        """Record throughput metric."""
        self.record_metric(
            MetricType.THROUGHPUT,
            tokens_per_second,
            "tokens/second",
            {"batch_size": batch_size}
        )
    
    def get_system_stats(self) -> SystemStats:
        """Get current system statistics."""
        try:
            # CPU usage
            cpu_percentage = psutil.cpu_percent(interval=0.1)
            
            # Memory stats
            memory = psutil.virtual_memory()
            memory_stats = MemoryStats(
                total_memory_gb=memory.total / (1024 ** 3),
                used_memory_gb=memory.used / (1024 ** 3),
                available_memory_gb=memory.available / (1024 ** 3),
                memory_percentage=memory.percent,
                peak_memory_gb=self.memory_tracker.peak_memory,
                process_memory_gb=self.memory_tracker._get_current_memory()
            )
            
            # GPU stats
            gpu_stats = self.gpu_monitor.get_gpu_stats()
            if gpu_stats.get('gpu_available'):
                gpu_0_stats = gpu_stats.get('gpu_0', {})
                memory_stats.gpu_memory_gb = gpu_0_stats.get('memory_allocated_gb', 0.0)
                memory_stats.gpu_memory_percentage = gpu_0_stats.get('memory_percentage', 0.0)
            
            # Disk usage
            disk_usage = psutil.disk_usage('/')
            disk_usage_percentage = (disk_usage.used / disk_usage.total) * 100
            
            return SystemStats(
                cpu_percentage=cpu_percentage,
                memory_stats=memory_stats,
                disk_usage_percentage=disk_usage_percentage
            )
            
        except Exception as e:
            logger.warning(f"Error getting system stats: {e}")
            return SystemStats(
                cpu_percentage=0.0,
                memory_stats=MemoryStats(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
            )
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary."""
        if not self.metrics_history:
            return {"message": "No metrics recorded"}
        
        # Group metrics by type
        metrics_by_type = {}
        for metric in self.metrics_history:
            metric_type = metric.metric_type.value
            if metric_type not in metrics_by_type:
                metrics_by_type[metric_type] = []
            metrics_by_type[metric_type].append(metric.value)
        
        # Calculate statistics for each metric type
        summary = {}
        for metric_type, values in metrics_by_type.items():
            if values:
                summary[metric_type] = {
                    'count': len(values),
                    'min': min(values),
                    'max': max(values),
                    'avg': sum(values) / len(values),
                    'latest': values[-1]
                }
        
        # Add system stats
        system_stats = self.get_system_stats()
        summary['system'] = {
            'cpu_percentage': system_stats.cpu_percentage,
            'memory_usage_gb': system_stats.memory_stats.used_memory_gb,
            'memory_percentage': system_stats.memory_stats.memory_percentage,
            'gpu_memory_gb': system_stats.memory_stats.gpu_memory_gb,
            'gpu_memory_percentage': system_stats.memory_stats.gpu_memory_percentage
        }
        
        return summary
    
    def _monitoring_loop(self):
        """Main monitoring loop."""
        while self.is_monitoring:
            try:
                # Get system stats
                system_stats = self.get_system_stats()
                
                # Record system metrics
                self.record_metric(
                    MetricType.CPU_USAGE,
                    system_stats.cpu_percentage,
                    "percentage"
                )
                
                self.record_metric(
                    MetricType.MEMORY_USAGE,
                    system_stats.memory_stats.used_memory_gb,
                    "GB"
                )
                
                if system_stats.memory_stats.gpu_memory_gb is not None:
                    self.record_metric(
                        MetricType.GPU_MEMORY,
                        system_stats.memory_stats.gpu_memory_gb,
                        "GB"
                    )
                
                # Sleep for sample interval
                time.sleep(self.sample_interval)
                
            except Exception as e:
                logger.warning(f"Monitoring loop error: {e}")
                time.sleep(self.sample_interval)
    
    def save_metrics(self, filepath: str):
        """Save metrics to file."""
        metrics_data = []
        for metric in self.metrics_history:
            metrics_data.append({
                'timestamp': metric.timestamp,
                'metric_type': metric.metric_type.value,
                'value': metric.value,
                'unit': metric.unit,
                'metadata': metric.metadata
            })
        
        with open(filepath, 'w') as f:
            json.dump(metrics_data, f, indent=2)
        
        logger.info(f"✅ Metrics saved to {filepath}")
    
    def load_metrics(self, filepath: str):
        """Load metrics from file."""
        with open(filepath, 'r') as f:
            metrics_data = json.load(f)
        
        self.metrics_history = []
        for data in metrics_data:
            metric = PerformanceMetrics(
                timestamp=data['timestamp'],
                metric_type=MetricType(data['metric_type']),
                value=data['value'],
                unit=data['unit'],
                metadata=data.get('metadata', {})
            )
            self.metrics_history.append(metric)
        
        logger.info(f"✅ Metrics loaded from {filepath}")
    
    def clear_metrics(self):
        """Clear all recorded metrics."""
        self.metrics_history = []
        logger.info("🗑️ Metrics cleared")


if __name__ == "__main__":
    # Test the performance monitor
    import time
    
    def test_performance_monitor():
        print("🧪 Testing Performance Monitor")
        print("=" * 50)
        
        # Create performance monitor
        monitor = PerformanceMonitor()
        
        # Start monitoring
        monitor.start_monitoring(sample_interval=0.5)
        
        # Start memory tracking
        monitor.start_memory_tracking()
        
        print("📊 Monitoring for 5 seconds...")
        
        # Simulate some work
        for i in range(5):
            # Record some custom metrics
            monitor.record_inference_time(0.1 + i * 0.01, sequence_length=100 + i * 10)
            monitor.record_throughput(1000 - i * 50, batch_size=1 + i)
            
            time.sleep(1.0)
        
        # Stop memory tracking
        memory_stats = monitor.stop_memory_tracking()
        print(f"📊 Memory tracking results:")
        for key, value in memory_stats.items():
            print(f"   {key}: {value:.2f}")
        
        # Get performance summary
        summary = monitor.get_performance_summary()
        print(f"\n📊 Performance Summary:")
        for metric_type, stats in summary.items():
            if isinstance(stats, dict) and 'count' in stats:
                print(f"   {metric_type}:")
                print(f"     Count: {stats['count']}")
                print(f"     Average: {stats['avg']:.2f}")
                print(f"     Min: {stats['min']:.2f}")
                print(f"     Max: {stats['max']:.2f}")
        
        # Stop monitoring
        monitor.stop_monitoring()
        
        print("\n✅ Performance monitor test completed!")
    
    # Run test
    test_performance_monitor()
