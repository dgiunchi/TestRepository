# Collatz Explorer: Visualizing the 3n+1 Conjecture

Discover the fascinating world of the Collatz conjecture through interactive CLI tools and mesmerizing animated visualizations. Analyze sequences, explore patterns, and watch the mathematics unfold.

## What this project includes

- `collatz_explorer.py`: CLI tool to inspect a single sequence or analyze a full range of starting values.
- `collatz_animated_ui.py`: interactive matplotlib animation app with a startup wizard for chart selection and playback speed.

## Features

- Generate full Collatz sequences from any positive starting value.
- Compute stopping time (steps to reach `1`) and peak value.
- Analyze all starts in `1..N` and summarize:
  - longest stopping time
  - highest peak
  - stopping-time distribution buckets
- Animate sequence or range behavior with multiple chart types.

## Requirements

- Python 3.10+
- Dependencies in `requirements.txt` (currently `matplotlib`)

## Quick start (Windows PowerShell)

1. Create a virtual environment and install dependencies:

```powershell
.\setup_env.ps1
```

2. Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Run the CLI explorer:

```powershell
python collatz_explorer.py
```

4. Run the animated UI:

```powershell
python collatz_animated_ui.py
```

## CLI usage

### 1) Show one sequence

```powershell
python collatz_explorer.py --mode sequence --start 27
```

### 2) Analyze a range

```powershell
python collatz_explorer.py --mode range --limit 500
```

### 3) Run both reports

```powershell
python collatz_explorer.py --mode both --start 27 --limit 500
```

Useful options:

- `--max-steps` sets a safety cap for sequence generation.
- `--mode` is one of `sequence`, `range`, or `both`.

## Animated UI usage

Default behavior starts an interactive wizard:

```powershell
python collatz_animated_ui.py
```

You can also skip prompts and run directly:

```powershell
python collatz_animated_ui.py --no-wizard --mode range --limit 300 --interval-ms 80
```

Key options:

- `--mode sequence|range`
- `--start` (sequence mode)
- `--limit` (range mode)
- `--max-steps`
- `--interval-ms` (animation speed in milliseconds)
- `--no-wizard`

## Project structure

- `collatz_explorer.py`
- `collatz_animated_ui.py`
- `requirements.txt`
- `setup_env.ps1`

## Notes

- This project is educational and exploratory; it does not attempt to prove the Collatz conjecture.
- Very large ranges or low animation intervals may be computationally heavy.
