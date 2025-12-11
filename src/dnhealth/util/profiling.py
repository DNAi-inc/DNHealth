# Copyright 2025 DNAi inc.

# Dual-licensed under the DNAi Free License v1.1 and the
# DNAi Commercial License v1.1.
# See the LICENSE files in the project root for details.

"""
Performance profiling utilities for DNHealth library.

Provides timing and memory profiling capabilities.
"""

import time
import tracemalloc
from contextlib import contextmanager
from typing import Dict, Optional, List, Callable, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class PerformanceProfiler:
    """
    Performance profiler for measuring execution time and memory usage.
    """

    def __init__(self):
        """Initialize profiler."""
        self._start_time: Optional[float] = None
        self._end_time: Optional[float] = None
        self._start_memory: Optional[tracemalloc.Snapshot] = None
        self._end_memory: Optional[tracemalloc.Snapshot] = None
        self._memory_tracking = False

    def start(self, track_memory: bool = False) -> None:
        """
        Start profiling.

        Args:
            track_memory: If True, track memory usage (default: False)
        """
        self._start_time = time.perf_counter()
        self._memory_tracking = track_memory
        if track_memory:
            tracemalloc.start()
            self._start_memory = tracemalloc.take_snapshot()

    def stop(self) -> Dict[str, Any]:
        """
        Stop profiling and return results.

        Returns:
            Dictionary with timing and memory statistics, including timestamp
        """
        self._end_time = time.perf_counter()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        results = {
            "elapsed_time": 0.0,
            "memory_used": 0.0,
            "memory_peak": 0.0,
            "timestamp": current_time,
        }
        
        if self._start_time is not None and self._end_time is not None:
            results["elapsed_time"] = self._end_time - self._start_time
        
        if self._memory_tracking:
            if self._start_memory is not None:
                self._end_memory = tracemalloc.take_snapshot()
                stats = self._end_memory.compare_to(self._start_memory, "lineno")
                if stats:
                    # Calculate memory difference
                    current, peak = tracemalloc.get_traced_memory()
                    results["memory_used"] = current / (1024 * 1024)  # MB
                    results["memory_peak"] = peak / (1024 * 1024)  # MB
                tracemalloc.stop()
        
        # Log completion with timestamp
        logger.info(f"Profiling completed at {current_time}: {results['elapsed_time']:.4f}s elapsed")
        
        return results

    def reset(self) -> None:
        """Reset profiler state."""
        self._start_time = None
        self._end_time = None
        self._start_memory = None
        self._end_memory = None
        self._memory_tracking = False


@contextmanager
def profile_operation(operation_name: str = "operation", track_memory: bool = False):
    """
    Context manager for profiling an operation.

    Args:
        operation_name: Name of the operation being profiled
        track_memory: If True, track memory usage

    Yields:
        Profiler instance

    Example:
        with profile_operation("parse_message", track_memory=True) as profiler:
            result = parse_hl7v2(message_text)
        print(f"Time: {profiler.stop()['elapsed_time']}s")
    """
    profiler = PerformanceProfiler()
    profiler.start(track_memory=track_memory)
    try:
        yield profiler
    finally:
        results = profiler.stop()
        if track_memory:
            print(
                f"{operation_name}: {results['elapsed_time']:.4f}s, "
                f"Memory: {results['memory_used']:.2f}MB (peak: {results['memory_peak']:.2f}MB)"
            )
        else:
            print(f"{operation_name}: {results['elapsed_time']:.4f}s")


    # Log completion timestamp at end of operation
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Current Time at End of Operations: {current_time}")

def time_function(func):
    """
    Decorator to time a function execution.

    Args:
        func: Function to time

    Returns:
        Wrapped function that prints execution time with timestamp
    """
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Function {func.__name__} started at {current_time}")
        
        result = func(*args, **kwargs)
        
        end = time.perf_counter()
        elapsed = end - start
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        logger.info(f"Function {func.__name__} completed at {completion_time}: {elapsed:.4f} seconds")
        print(f"{func.__name__} took {elapsed:.4f} seconds (completed at {completion_time})")
        
        return result
    return wrapper


class Benchmark:
    """
    Benchmark utility for running multiple iterations of a function.
    
    Provides statistical analysis of execution times and memory usage.
    """
    
    def __init__(self, name: str = "benchmark"):
        """
        Initialize benchmark.
        
        Args:
            name: Name of the benchmark
        """
        self.name = name
        self.results: List[Dict[str, Any]] = []
    

        # Log completion timestamp at end of operation
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time at End of Operations: {current_time}")
    def run(self, func: Callable, *args, iterations: int = 10, track_memory: bool = False, **kwargs) -> Dict[str, Any]:
        """
        Run benchmark on a function.
        
        Args:
            func: Function to benchmark
            *args: Positional arguments for function
            iterations: Number of iterations to run
            track_memory: If True, track memory usage
            **kwargs: Keyword arguments for function
            
        Returns:
            Dictionary with benchmark statistics including timestamp
        """
        start_time = time.perf_counter()
        benchmark_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Benchmark '{self.name}' started at {benchmark_start_time} with {iterations} iterations")
        
        self.results = []
        
        for i in range(iterations):
            profiler = PerformanceProfiler()
            profiler.start(track_memory=track_memory)
            
            try:
                result = func(*args, **kwargs)
                profiler_results = profiler.stop()
                profiler_results["iteration"] = i + 1
                self.results.append(profiler_results)
            except Exception as e:
                logger.error(f"Benchmark iteration {i+1} failed: {e}")
                profiler.stop()
                raise
        
        end_time = time.perf_counter()
        benchmark_end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total_elapsed = end_time - start_time
        
        # Calculate statistics
        elapsed_times = [r["elapsed_time"] for r in self.results]
        stats = {
            "name": self.name,
            "iterations": iterations,
            "total_elapsed": total_elapsed,
            "avg_elapsed": sum(elapsed_times) / len(elapsed_times) if elapsed_times else 0.0,
            "min_elapsed": min(elapsed_times) if elapsed_times else 0.0,
            "max_elapsed": max(elapsed_times) if elapsed_times else 0.0,
            "start_time": benchmark_start_time,
            "end_time": benchmark_end_time,
            "timestamp": benchmark_end_time,
        }
        
        if track_memory:
            memory_usages = [r["memory_used"] for r in self.results if "memory_used" in r]
            memory_peaks = [r["memory_peak"] for r in self.results if "memory_peak" in r]
            if memory_usages:
                stats["avg_memory"] = sum(memory_usages) / len(memory_usages)
                stats["max_memory"] = max(memory_usages)
            if memory_peaks:
                stats["avg_peak_memory"] = sum(memory_peaks) / len(memory_peaks)
                stats["max_peak_memory"] = max(memory_peaks)
        
        logger.info(
            f"Benchmark '{self.name}' completed at {benchmark_end_time}: "
            f"{stats['avg_elapsed']:.4f}s avg, {stats['min_elapsed']:.4f}s min, "
            f"{stats['max_elapsed']:.4f}s max over {iterations} iterations"
        )
        
        return stats
    
    def format_results(self) -> str:
        """
        Format benchmark results as human-readable text.
        
        Returns:
            Formatted benchmark results with timestamp
        """
        if not self.results:
            return f"Benchmark '{self.name}': No results available"
        
        lines = []
        lines.append(f"Benchmark Results: {self.name}")
        lines.append("=" * 60)
        
        elapsed_times = [r["elapsed_time"] for r in self.results]
        avg_time = sum(elapsed_times) / len(elapsed_times)
        min_time = min(elapsed_times)
        max_time = max(elapsed_times)
        
        lines.append(f"Iterations: {len(self.results)}")
        lines.append(f"Average time: {avg_time:.4f}s")
        lines.append(f"Min time: {min_time:.4f}s")
        lines.append(f"Max time: {max_time:.4f}s")
        
        if self.results and "memory_used" in self.results[0]:
            memory_usages = [r["memory_used"] for r in self.results if "memory_used" in r]
            if memory_usages:
                avg_memory = sum(memory_usages) / len(memory_usages)
                max_memory = max(memory_usages)
                lines.append(f"Average memory: {avg_memory:.2f}MB")
                lines.append(f"Max memory: {max_memory:.2f}MB")
        
        if self.results and "timestamp" in self.results[-1]:
            lines.append(f"Completed at: {self.results[-1]['timestamp']}")
        
        return "\n".join(lines) + "\n"

