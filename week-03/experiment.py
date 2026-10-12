"""蒲丰投针实验：用真实随机模拟估计圆周率。

固定入口一。可被 import；import 时不启动实验、不写文件。
直接运行会按起始配置跑三组实验并写出 results.csv：

    uv run --locked python experiment.py
"""

from __future__ import annotations

import argparse
import csv
import math
import random

DEFAULT_SEED = 42
DEFAULT_SIZES = (1000, 10000, 100000)
DEFAULT_LENGTH = 0.5
DEFAULT_SPACING = 1.0

# CSV 表头；顺序与 simulate() 返回字段一致。
FIELDS = (
    "seed",
    "n",
    "crossings",
    "pi_estimate",
    "needle_length",
    "line_spacing",
)


def _check_geometry(length: float, spacing: float) -> None:
    """校验针长与线距：0 < length <= spacing。不合法就报错，不静默改参数。"""
    if not (spacing > 0):
        raise ValueError("line spacing must be positive")
    if not (length > 0):
        raise ValueError("needle length must be positive")
    if length > spacing:
        raise ValueError("needle length must not exceed line spacing")


def crosses_line(distance, angle, length=DEFAULT_LENGTH, spacing=DEFAULT_SPACING) -> bool:
    """判断一次投针是否与平行线相交（接触也算相交）。

    相交判据：distance <= (length / 2) * sin(angle)。
    合法输入范围：0 <= distance <= spacing/2，0 <= angle <= pi/2。
    越界的几何参数抛 ValueError，不做静默修正。
    """
    _check_geometry(length, spacing)
    if not (0 <= distance <= spacing / 2):
        raise ValueError("distance must be within [0, spacing/2]")
    if not (0 <= angle <= math.pi / 2):
        raise ValueError("angle must be within [0, pi/2]")

    return distance <= (length / 2) * math.sin(angle)


def estimate_pi(n, crossings, length=DEFAULT_LENGTH, spacing=DEFAULT_SPACING) -> float:
    """由投针数与相交数估计圆周率：2 * length * n / (spacing * crossings)。

    n 为正整数；crossings 为整数且 0 <= crossings <= n。
    crossings = 0 时该式无法成立，抛 ValueError，不返回虚构的估计值。
    """
    _check_geometry(length, spacing)
    if not (isinstance(n, int) and not isinstance(n, bool) and n > 0):
        raise ValueError("n must be a positive integer")
    if not (isinstance(crossings, int) and not isinstance(crossings, bool)):
        raise ValueError("crossings must be an integer")
    if not (0 <= crossings <= n):
        raise ValueError("crossings must satisfy 0 <= crossings <= n")
    if crossings == 0:
        raise ValueError("cannot estimate pi from zero crossings")

    return 2 * length * n / (spacing * crossings)


def simulate(n, seed=DEFAULT_SEED, length=DEFAULT_LENGTH, spacing=DEFAULT_SPACING) -> dict:
    """投 n 次针，返回本次实验的真实记录。

    每次调用只在循环外用 seed 初始化一次随机数生成器；循环内持续取样，
    不在每次投针时重设 seed。
    """
    _check_geometry(length, spacing)
    if not (isinstance(n, int) and not isinstance(n, bool) and n > 0):
        raise ValueError("n must be a positive integer")

    rng = random.Random(seed)  # 循环外初始化一次
    crossings = 0
    for _ in range(n):
        distance = rng.uniform(0.0, spacing / 2)
        angle = rng.uniform(0.0, math.pi / 2)
        if crosses_line(distance, angle, length=length, spacing=spacing):
            crossings += 1

    if crossings == 0:
        raise ValueError("no crossings in this run; pi cannot be estimated")

    pi_estimate = estimate_pi(n, crossings, length=length, spacing=spacing)

    return {
        "seed": seed,
        "n": n,
        "crossings": crossings,
        "pi_estimate": pi_estimate,
        "needle_length": length,
        "line_spacing": spacing,
    }


def run_experiments(sizes, seed=DEFAULT_SEED, length=DEFAULT_LENGTH,
                    spacing=DEFAULT_SPACING, out_path="results.csv"):
    """按给定投针数逐组运行，每组独立初始化一次随机数生成器，写出 CSV。"""
    rows = []
    for n in sizes:
        result = simulate(n, seed=seed, length=length, spacing=spacing)
        rows.append(result)
        print(
            f"n={n:>7}  seed={seed}  crossings={result['crossings']:>7}  "
            f"pi_estimate={result['pi_estimate']:.6f}"
        )

    with open(out_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"已写出 {out_path}（{len(rows)} 行）")
    return rows


def _parse_args(argv=None):
    parser = argparse.ArgumentParser(description="蒲丰投针估计圆周率")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED,
                        help="随机数种子（默认 %(default)s）")
    parser.add_argument("--n", type=int, action="append", dest="sizes",
                        help="投针数，可重复指定；默认 1000 10000 100000")
    parser.add_argument("--length", type=float, default=DEFAULT_LENGTH,
                        help="针长（默认 %(default)s）")
    parser.add_argument("--spacing", type=float, default=DEFAULT_SPACING,
                        help="平行线间距（默认 %(default)s）")
    parser.add_argument("--out", default="results.csv",
                        help="CSV 输出路径（默认 %(default)s）")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = _parse_args(argv)
    sizes = tuple(args.sizes) if args.sizes else DEFAULT_SIZES
    run_experiments(sizes, seed=args.seed, length=args.length,
                    spacing=args.spacing, out_path=args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
