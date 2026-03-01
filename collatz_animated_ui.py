#!/usr/bin/env python3
"""
Animated Collatz explorer with a startup input wizard.

The script asks for your choices first, then opens an animated matplotlib UI
with multiple chart types to visualize Collatz behavior.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from typing import Callable


import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if SRC.exists() and str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from collatz.core import collatz_sequence



@dataclass
class SequenceConfig:
    start: int
    max_steps: int
    interval_ms: int
    charts: list[str]


@dataclass
class RangeConfig:
    limit: int
    max_steps: int
    interval_ms: int
    charts: list[str]


def ask_int(prompt: str, default: int, min_value: int = 1) -> int:
    while True:
        raw = input(f"{prompt} [{default}]: ").strip()
        if raw == "":
            return default
        try:
            value = int(raw)
            if value < min_value:
                print(f"Please enter an integer >= {min_value}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid integer.")


def ask_choice(prompt: str, options: list[str], default: str) -> str:
    options_str = ", ".join(options)
    while True:
        raw = input(f"{prompt} ({options_str}) [{default}]: ").strip().lower()
        if raw == "":
            return default
        if raw in options:
            return raw
        print("Please choose one of the listed options.")


def ask_yes_no(prompt: str, default_yes: bool = True) -> bool:
    default_str = "Y/n" if default_yes else "y/N"
    while True:
        raw = input(f"{prompt} [{default_str}]: ").strip().lower()
        if raw == "":
            return default_yes
        if raw in {"y", "yes"}:
            return True
        if raw in {"n", "no"}:
            return False
        print("Please answer with y or n.")


def pick_charts(available: dict[str, str]) -> list[str]:
    print("\nSelect charts to include:")
    selected: list[str] = []
    for chart_id, description in available.items():
        use_it = ask_yes_no(f"- {chart_id}: {description}?", default_yes=True)
        if use_it:
            selected.append(chart_id)
    if not selected:
        first_key = next(iter(available))
        print(f"No chart selected. Using '{first_key}'.")
        selected.append(first_key)
    return selected


def make_axes(plt_module, chart_ids: list[str]):
    n = len(chart_ids)
    cols = 1 if n == 1 else 2
    rows = math.ceil(n / cols)
    fig, axes = plt_module.subplots(rows, cols, figsize=(7 * cols, 4 * rows))
    if not isinstance(axes, (list, tuple)):
        try:
            flat_axes = list(axes.flat)
        except AttributeError:
            flat_axes = [axes]
    else:
        flat_axes = list(axes)
    for idx in range(n, len(flat_axes)):
        flat_axes[idx].set_visible(False)
    ax_map = {chart_ids[i]: flat_axes[i] for i in range(n)}
    return fig, ax_map


def run_sequence_ui(config: SequenceConfig) -> None:
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    seq = collatz_sequence(config.start, max_steps=config.max_steps)
    steps = list(range(len(seq)))
    peak = max(seq)

    chart_defs = {
        "line": "Sequence values over time",
        "bar_parity": "Even vs odd counts (cumulative)",
        "scatter_log": "Scatter of step vs log10(value)",
        "hist_values": "Histogram of visited values",
    }
    fig, ax_map = make_axes(plt, config.charts)
    fig.suptitle(f"Collatz Sequence Explorer (start={config.start})")

    artists: dict[str, object] = {}

    if "line" in ax_map:
        ax = ax_map["line"]
        ax.set_title(chart_defs["line"])
        ax.set_xlabel("Step")
        ax.set_ylabel("Value")
        ax.set_xlim(0, max(1, len(seq) - 1))
        ax.set_ylim(0, max(2, int(peak * 1.05)))
        (line_artist,) = ax.plot([], [], lw=2, color="tab:blue")
        artists["line"] = line_artist

    if "bar_parity" in ax_map:
        ax = ax_map["bar_parity"]
        ax.set_title(chart_defs["bar_parity"])
        ax.set_ylabel("Count")
        bars = ax.bar(["Even", "Odd"], [0, 0], color=["tab:green", "tab:orange"])
        ax.set_ylim(0, len(seq))
        artists["bar_parity"] = bars

    if "scatter_log" in ax_map:
        ax = ax_map["scatter_log"]
        ax.set_title(chart_defs["scatter_log"])
        ax.set_xlabel("Step")
        ax.set_ylabel("log10(Value)")
        ax.set_xlim(0, max(1, len(seq) - 1))
        ax.set_ylim(0, math.log10(max(2, peak)) + 0.2)
        scatter = ax.scatter([], [], s=22, color="tab:red", alpha=0.75)
        artists["scatter_log"] = scatter

    if "hist_values" in ax_map:
        ax = ax_map["hist_values"]
        ax.set_title(chart_defs["hist_values"])
        ax.set_xlabel("Value")
        ax.set_ylabel("Frequency")
        artists["hist_values"] = ax

    def update(frame: int):
        current = seq[: frame + 1]
        current_steps = steps[: frame + 1]

        if "line" in artists:
            line_artist = artists["line"]
            line_artist.set_data(current_steps, current)

        if "bar_parity" in artists:
            bars = artists["bar_parity"]
            even_count = sum(1 for x in current if x % 2 == 0)
            odd_count = len(current) - even_count
            bars[0].set_height(even_count)
            bars[1].set_height(odd_count)

        if "scatter_log" in artists:
            scatter = artists["scatter_log"]
            points = [[s, math.log10(max(1, v))] for s, v in zip(current_steps, current)]
            scatter.set_offsets(points)

        if "hist_values" in artists:
            ax = artists["hist_values"]
            ax.cla()
            ax.set_title(chart_defs["hist_values"])
            ax.set_xlabel("Value")
            ax.set_ylabel("Frequency")
            bins = min(30, max(5, int(math.sqrt(len(current)))))
            ax.hist(current, bins=bins, color="tab:purple", alpha=0.8)

        return []

    anim = FuncAnimation(
        fig,
        update,
        frames=len(seq),
        interval=config.interval_ms,
        repeat=False,
        blit=False,
    )
    # Keep a strong reference to prevent garbage collection before rendering.
    fig._collatz_anim = anim
    plt.tight_layout()
    plt.show()


def run_range_ui(config: RangeConfig) -> None:
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    starts: list[int] = []
    stop_times: list[int] = []
    peaks: list[int] = []
    for s in range(1, config.limit + 1):
        seq = collatz_sequence(s, max_steps=config.max_steps)
        if seq[-1] != 1:
            continue
        starts.append(s)
        stop_times.append(len(seq) - 1)
        peaks.append(max(seq))

    chart_defs = {
        "line_stop": "Stopping time by start value",
        "line_peak": "Peak value by start value",
        "scatter_stop_peak": "Stopping time vs peak (scatter)",
        "hist_stop": "Histogram of stopping times",
        "bar_top_stop": "Top 10 starts by stopping time",
    }
    fig, ax_map = make_axes(plt, config.charts)
    fig.suptitle(f"Collatz Range Explorer (1..{config.limit})")

    artists: dict[str, object] = {}
    max_stop = max(stop_times) if stop_times else 1
    max_peak = max(peaks) if peaks else 1

    if "line_stop" in ax_map:
        ax = ax_map["line_stop"]
        ax.set_title(chart_defs["line_stop"])
        ax.set_xlabel("Start")
        ax.set_ylabel("Stopping Time")
        ax.set_xlim(1, max(2, config.limit))
        ax.set_ylim(0, int(max_stop * 1.1) + 1)
        (line_stop,) = ax.plot([], [], color="tab:blue", lw=2)
        artists["line_stop"] = line_stop

    if "line_peak" in ax_map:
        ax = ax_map["line_peak"]
        ax.set_title(chart_defs["line_peak"])
        ax.set_xlabel("Start")
        ax.set_ylabel("Peak")
        ax.set_xlim(1, max(2, config.limit))
        ax.set_ylim(0, int(max_peak * 1.05) + 1)
        (line_peak,) = ax.plot([], [], color="tab:green", lw=2)
        artists["line_peak"] = line_peak

    if "scatter_stop_peak" in ax_map:
        ax = ax_map["scatter_stop_peak"]
        ax.set_title(chart_defs["scatter_stop_peak"])
        ax.set_xlabel("Stopping Time")
        ax.set_ylabel("Peak")
        ax.set_xlim(0, int(max_stop * 1.1) + 1)
        ax.set_ylim(0, int(max_peak * 1.05) + 1)
        scatter = ax.scatter([], [], color="tab:red", alpha=0.7, s=22)
        artists["scatter_stop_peak"] = scatter

    if "hist_stop" in ax_map:
        ax = ax_map["hist_stop"]
        ax.set_title(chart_defs["hist_stop"])
        ax.set_xlabel("Stopping Time")
        ax.set_ylabel("Frequency")
        artists["hist_stop"] = ax

    if "bar_top_stop" in ax_map:
        ax = ax_map["bar_top_stop"]
        ax.set_title(chart_defs["bar_top_stop"])
        ax.set_xlabel("Stopping Time")
        ax.set_ylabel("Start Value")
        artists["bar_top_stop"] = ax

    def update(frame: int):
        i = frame + 1
        x = starts[:i]
        y_stop = stop_times[:i]
        y_peak = peaks[:i]

        if "line_stop" in artists:
            artists["line_stop"].set_data(x, y_stop)

        if "line_peak" in artists:
            artists["line_peak"].set_data(x, y_peak)

        if "scatter_stop_peak" in artists:
            points = [[a, b] for a, b in zip(y_stop, y_peak)]
            artists["scatter_stop_peak"].set_offsets(points)

        if "hist_stop" in artists:
            ax = artists["hist_stop"]
            ax.cla()
            ax.set_title(chart_defs["hist_stop"])
            ax.set_xlabel("Stopping Time")
            ax.set_ylabel("Frequency")
            bins = min(20, max(5, int(math.sqrt(len(y_stop)))))
            ax.hist(y_stop, bins=bins, color="tab:orange", alpha=0.8)

        if "bar_top_stop" in artists:
            ax = artists["bar_top_stop"]
            ax.cla()
            ax.set_title(chart_defs["bar_top_stop"])
            ax.set_xlabel("Stopping Time")
            ax.set_ylabel("Start Value")
            top = sorted(zip(x, y_stop), key=lambda t: t[1], reverse=True)[:10]
            top_starts = [t[0] for t in top][::-1]
            top_times = [t[1] for t in top][::-1]
            ax.barh([str(s) for s in top_starts], top_times, color="tab:cyan")

        return []

    frames = max(1, len(starts))
    anim = FuncAnimation(
        fig,
        update,
        frames=frames,
        interval=config.interval_ms,
        repeat=False,
        blit=False,
    )
    # Keep a strong reference to prevent garbage collection before rendering.
    fig._collatz_anim = anim
    plt.tight_layout()
    plt.show()


def interactive_wizard(args: argparse.Namespace):
    print("Collatz Animated Explorer")
    print("========================")
    mode = ask_choice("Mode", ["sequence", "range"], args.mode)
    max_steps = ask_int("Max steps per sequence", args.max_steps, min_value=1)
    interval_ms = ask_int("Animation speed in ms per frame", args.interval_ms, min_value=10)

    if mode == "sequence":
        start = ask_int("Starting value", args.start, min_value=1)
        charts = pick_charts(
            {
                "line": "Line chart of sequence values",
                "bar_parity": "Bar chart of even/odd counts",
                "scatter_log": "Scatter chart with log-scale values",
                "hist_values": "Histogram of seen values",
            }
        )
        return mode, SequenceConfig(start=start, max_steps=max_steps, interval_ms=interval_ms, charts=charts)

    limit = ask_int("Analyze range 1..N, choose N", args.limit, min_value=2)
    charts = pick_charts(
        {
            "line_stop": "Line chart of stopping times",
            "line_peak": "Line chart of peak values",
            "scatter_stop_peak": "Scatter of stopping time vs peak",
            "hist_stop": "Histogram of stopping times",
            "bar_top_stop": "Bar chart of top 10 longest stopping times",
        }
    )
    return mode, RangeConfig(limit=limit, max_steps=max_steps, interval_ms=interval_ms, charts=charts)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Animated matplotlib UI for exploring Collatz behavior."
    )
    parser.add_argument("--mode", choices=["sequence", "range"], default="sequence")
    parser.add_argument("--start", type=int, default=27, help="Default start for sequence mode.")
    parser.add_argument("--limit", type=int, default=200, help="Default upper bound for range mode.")
    parser.add_argument("--max-steps", type=int, default=10000, help="Safety cap for each sequence.")
    parser.add_argument("--interval-ms", type=int, default=120, help="Animation speed in ms per frame.")
    parser.add_argument(
        "--no-wizard",
        action="store_true",
        help="Skip startup prompts and run with CLI arguments/defaults.",
    )
    return parser.parse_args()


def build_direct_config(args: argparse.Namespace):
    if args.mode == "sequence":
        return args.mode, SequenceConfig(
            start=max(1, args.start),
            max_steps=max(1, args.max_steps),
            interval_ms=max(10, args.interval_ms),
            charts=["line", "bar_parity", "scatter_log", "hist_values"],
        )
    return args.mode, RangeConfig(
        limit=max(2, args.limit),
        max_steps=max(1, args.max_steps),
        interval_ms=max(10, args.interval_ms),
        charts=["line_stop", "line_peak", "scatter_stop_peak", "hist_stop", "bar_top_stop"],
    )


def main() -> None:
    args = parse_args()
    mode: str
    config: SequenceConfig | RangeConfig
    if args.no_wizard:
        mode, config = build_direct_config(args)
    else:
        mode, config = interactive_wizard(args)

    runner: Callable[[SequenceConfig | RangeConfig], None]
    if mode == "sequence":
        runner = run_sequence_ui
    else:
        runner = run_range_ui
    runner(config)


if __name__ == "__main__":
    main()
