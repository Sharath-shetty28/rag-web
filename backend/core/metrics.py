import numpy as np

def compute_latency_stats(times_ms):
    times = np.array(times_ms)
    return {
        "p50_ms": float(np.percentile(times, 50)),
        "p95_ms": float(np.percentile(times, 95)),
        "min_ms": float(times.min()),
        "max_ms": float(times.max())
    }
