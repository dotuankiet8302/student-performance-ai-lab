# Student Performance + AI Lab

A local-only educational student search website. Uses Python standard library and SQLite; 5,000 **synthetic** student records.

## Windows / VS Code

1. Install Python 3.10+ and open this folder in VS Code.
2. Terminal 1: `python server.py` and visit `http://127.0.0.1:18765`.
3. Terminal 2: `python benchmark.py` to run 500 HTTP requests at five concurrent-worker levels.
4. Install analysis packages: `pip install pandas numpy scikit-learn matplotlib`.
5. Run `python analyze.py` to create `analyzed_results.csv` and `measured_chart.png`.
6. Optional: install k6 and run `k6 run k6_search.js` while server is running. The Python benchmark and k6 are **different workload models**; do not compare them as equivalent.

## Controlled anomaly

Stop the server. In PowerShell: `$env:LAB_DELAY_MS="120"; python server.py`. Run benchmark again and compare against a saved baseline. This injects known delay, **not a naturally occurring bottleneck**.

## Interpretation caveats

- This is a loopback/local demo, not a deployed production web system.
- Worker count is concurrent clients, **not measured requests per second**.
- `analyze.py` fits and scores on the same dataset for exploratory visualization only. For an honest evaluation, fit on training data and score separate held-out runs, and provide independently labeled anomalies.
- AI flags alone do not establish precision, recall, F1, root cause, or AI superiority.
- For credible experiments, repeat trials, warm up the server, isolate system load, collect CPU/memory and compare against a stable baseline.
