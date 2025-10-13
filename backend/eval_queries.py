from routes.ask_routes import ask
from backend.core.metrics import compute_latency_stats

# Example small test set
test_questions = [
    "What services does the website offer?",
    "What time does the library open?",
    "Who is the owner of the website?"  # intentionally unanswerable
]

timings = []

for q in test_questions:
    print(f"Question: {q}")
    res = ask(q, top_k=3)
    timings.append(res["timings"]["total_ms"])
    print(res)
    print("-" * 40)

# Compute p50/p95 latency
stats = compute_latency_stats(timings)
print("Latency stats:", stats)
