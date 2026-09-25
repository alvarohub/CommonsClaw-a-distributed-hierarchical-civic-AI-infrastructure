# SSAI — Model Benchmarks

Machine: emotionpi (Raspberry Pi 5, 16 GB, active fan, CPU-only).
Prompt: "Explain what a differentiable manifold is in two short sentences." — num_predict=100, 3 timed runs after 1 warm-up.

| Date       | Model                   | avg tok/s | best tok/s | warm TTFT | wall (100 tok) | max tokens       | temp |
| ---------- | ----------------------- | --------- | ---------- | --------- | -------------- | ---------------- | ---- |
| 2026-09-25 | phi3.5:latest (3.8B Q4) | 5.19      | 5.19       | ~0.8 s    | ~19 s          | 30 (quick probe) | 54°C |
| 2026-09-25 | llama3.2:1b (1.3B Q4)   | 8.42      | 8.42       | ~0.5 s    | ~12 s          | 30 (quick probe) | 54°C |

_Note: the two rows above were quick 30-token probes ("count to ten"); the
script's standard benchmark (100 tokens, manifold prompt) gives the rigorous
numbers going forward. Add Hailo AI HAT+ rows here when available._
