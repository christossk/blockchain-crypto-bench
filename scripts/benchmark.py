import time
import psutil
import os
import argparse
import statistics

def benchmark(func, label="Benchmark", iterations=1000, warmup=10):
    """
    Benchmark the given function.

    Parameters:
        func (callable): The function to test.
        label (str): Descriptive label for output.
        iterations (int): Number of times to run the function.
        warmup (int): Number of warm-up runs (not timed).
    """
    print(f"\n🔬 Running {label} for {iterations} iterations...\n")

    # Warm-up
    for _ in range(warmup):
        func()

    latencies = []
    process = psutil.Process(os.getpid())
    start_mem = process.memory_info().rss

    for _ in range(iterations):
        t0 = time.perf_counter()
        func()
        t1 = time.perf_counter()
        latencies.append((t1 - t0) * 1e6)  # microseconds

    end_mem = process.memory_info().rss
    peak_memory_kb = (end_mem - start_mem) / 1024.0

    avg_latency_us = statistics.mean(latencies)
    median_latency_us = statistics.median(latencies)
    throughput = 1e6 / avg_latency_us  # ops/sec assuming microsecond latency

    print(f"[{label}]")
    print(f"Iterations        : {iterations}")
    print(f"Avg Latency       : {avg_latency_us:.2f} µs")
    print(f"Median Latency    : {median_latency_us:.2f} µs")
    print(f"Peak Memory Delta : {peak_memory_kb:.2f} KB")
    print(f"Throughput        : {throughput:,.2f} ops/sec\n")

    return {
        "label": label,
        "iterations": iterations,
        "avg_latency_us": avg_latency_us,
        "median_latency_us": median_latency_us,
        "peak_memory_kb": peak_memory_kb,
        "throughput_ops_per_sec": throughput
    }

# CLI usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=1000, help="Number of iterations to run")
    args = parser.parse_args()

    def test_function():
        sum(i for i in range(100))

    benchmark(test_function, "Sample Function", iterations=args.iterations)
