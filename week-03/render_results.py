"""由真实 results.csv 生成报告用表格、参数文字与静态图。

固定入口二。直接运行：

    uv run --locked python render_results.py

只读取当前目录的 results.csv，不重新投针、不编造结果。生成：
    results-table.tex   可直接 \\input 的 LaTeX 表格（n、crossings、pi_estimate）
    results-params.tex  可直接 \\input 的短文字（实际 seed、各组 n、针长、线距）
    results.png         不同 n 对应的估计值静态图（含真实 pi 参考线）

图片坐标轴用英文，避免在图像中额外安装中文字体；
中文 LaTeX 文件沿用模板（ctexart + Fandol）的字体设置。
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # 无界面后端，只写文件
import matplotlib.pyplot as plt  # noqa: E402


def read_results(csv_path: str | Path = "results.csv") -> list[dict]:
    """读取真实 CSV；字段保持字符串，数值在使用处再转换。"""
    with open(csv_path, encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"{csv_path} 没有数据行")
    return rows


def write_params(results: list[dict], out_path: str | Path = "results-params.tex") -> None:
    """按 CSV 实际值写出参数短文字。"""
    seeds = sorted({int(r["seed"]) for r in results})
    length = float(results[0]["needle_length"])
    spacing = float(results[0]["line_spacing"])
    sizes = [int(r["n"]) for r in results]

    seed_text = ", ".join(str(s) for s in seeds)
    size_text = ", ".join(f"{n}" for n in sizes)
    content = (
        "本次实验使用 seed $=$ " + seed_text
        + "，针长 $L=" + f"{length:g}" + "$，平行线间距 $d=" + f"{spacing:g}" + "$；"
        + "共 " + str(len(sizes)) + " 组投针，投针数 $N=" + size_text + "$。\n"
    )
    Path(out_path).write_text(content, encoding="utf-8")


def write_table(results: list[dict], out_path: str | Path = "results-table.tex") -> None:
    """写出可直接 input 的 LaTeX 表格。"""
    lines = [
        r"\begin{tabular}{rrr}",
        r"\toprule",
        r"投针数 $n$ & 相交数 $K$ & 估计值 $\widehat{\pi}$ \\",
        r"\midrule",
    ]
    for row in results:
        n = int(row["n"])
        crossings = int(row["crossings"])
        estimate = float(row["pi_estimate"])
        lines.append(f"{n} & {crossings} & {estimate:.6f} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    Path(out_path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_figure(results: list[dict], out_path: str | Path = "results.png") -> None:
    """画出不同 n 对应的估计值，并加真实 pi 参考线。"""
    sizes = [int(r["n"]) for r in results]
    estimates = [float(r["pi_estimate"]) for r in results]

    fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=150)
    ax.axhline(math.pi, color="gray", linestyle="--", linewidth=1.0,
               label=r"true $\pi$")
    ax.plot(sizes, estimates, marker="o", color="#1f77b4", label="estimate")
    ax.set_xscale("log")
    ax.set_xlabel("number of needles n")
    ax.set_ylabel(r"estimated $\pi$")
    ax.set_title("Buffon's needle: estimate vs sample size")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def main() -> int:
    results = read_results("results.csv")
    write_params(results)
    write_table(results)
    write_figure(results)
    print("已生成 results-params.tex、results-table.tex、results.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
