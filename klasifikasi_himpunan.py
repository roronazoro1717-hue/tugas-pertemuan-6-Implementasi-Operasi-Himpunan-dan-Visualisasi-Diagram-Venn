"""
PJBL-2 - Sistem Klasifikasi Data dengan Himpunan
Implementasi: union, intersection, difference, complement,
Diagram Venn otomatis (2-3 himpunan), dan Prinsip Inklusi-Eksklusi (PIE).

Pemakaian:
  python klasifikasi_himpunan.py --demo
  python klasifikasi_himpunan.py --data data/dataset1_keahlian_mahasiswa.csv \
      --op union --sets Desain Programming
  python klasifikasi_himpunan.py --data data/dataset1_keahlian_mahasiswa.csv \
      --op difference --sets Desain Video
  python klasifikasi_himpunan.py --data data/dataset1_keahlian_mahasiswa.csv \
      --op complement --sets Desain
  python klasifikasi_himpunan.py --data data/dataset1_keahlian_mahasiswa.csv \
      --pie --sets Desain Programming Video --venn output/venn.png
"""
import argparse
import csv
from itertools import combinations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


# ---------------------------------------------------------------- DATA
def load_dataset(path):
    """Baca CSV (id,nama,kategori). Return (U, kelompok) dengan
    U = himpunan semesta (id) dan kelompok = {kategori: himpunan id}."""
    universe, groups = set(), {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rid = int(row["id"])
            universe.add(rid)
            for cat in filter(None, (c.strip() for c in row["kategori"].split(";"))):
                groups.setdefault(cat, set()).add(rid)
    return universe, groups


# ------------------------------------------------------ OPERASI HIMPUNAN
def union(*sets):
    out = set()
    for s in sets:
        out = out | s
    return out


def intersection(*sets):
    out = set(sets[0])
    for s in sets[1:]:
        out = out & s
    return out


def difference(a, b):
    return a - b


def complement(a, universe):
    return universe - a


# ------------------------------------------------ PRINSIP INKLUSI-EKSKLUSI
def pie_count(sets):
    """|A1 u ... u An| = sum_{k=1..n} (-1)^(k+1) * sum |irisan k himpunan|.
    Return (total, rincian[(k, [(nama_gabungan, ukuran)], jumlah_suku)])."""
    names = list(sets)
    total, detail = 0, []
    for k in range(1, len(names) + 1):
        terms, subtotal = [], 0
        for combo in combinations(names, k):
            size = len(intersection(*[sets[n] for n in combo]))
            terms.append((" ∩ ".join(combo), size))
            subtotal += size
        sign = 1 if k % 2 == 1 else -1
        total += sign * subtotal
        detail.append((k, sign, terms, subtotal))
    return total, detail


# --------------------------------------------------------- DIAGRAM VENN
def region_sets(sets):
    """Isi tiap daerah eksklusif Diagram Venn (2 atau 3 himpunan)."""
    names = list(sets)
    regions = {}
    for mask in range(1, 2 ** len(names)):
        inside = [names[i] for i in range(len(names)) if mask >> i & 1]
        outside = [n for n in names if n not in inside]
        r = intersection(*[sets[n] for n in inside])
        for n in outside:
            r = r - sets[n]
        regions[tuple(inside)] = r
    return regions


def draw_venn(sets, universe, title, path):
    names = list(sets)
    if len(names) not in (2, 3):
        raise ValueError("Diagram Venn otomatis mendukung 2 atau 3 himpunan.")
    regions = region_sets(sets)
    colors = ["#e45756", "#4c78a8", "#54a24b"]
    if len(names) == 2:
        centers = [(-0.6, 0), (0.6, 0)]
        label_pos = {(names[0],): (-1.15, 0), (names[1],): (1.15, 0),
                     (names[0], names[1]): (0, 0)}
        lim = (-2.6, 2.6, -1.9, 1.9)
    else:
        centers = [(-0.65, 0.4), (0.65, 0.4), (0, -0.7)]
        a, b, c = names
        label_pos = {(a,): (-1.2, 0.75), (b,): (1.2, 0.75), (c,): (0, -1.35),
                     (a, b): (0, 0.85), (a, c): (-0.7, -0.35),
                     (b, c): (0.7, -0.35), (a, b, c): (0, 0.05)}
        lim = (-2.6, 2.6, -2.5, 2.2)
    fig, ax = plt.subplots(figsize=(6.2, 5.0))
    ax.add_patch(plt.Rectangle((lim[0] + .1, lim[2] + .1),
                               lim[1] - lim[0] - .2, lim[3] - lim[2] - .2,
                               fill=False, lw=1.5, ec="#333"))
    for i, (cx, cy) in enumerate(centers):
        ax.add_patch(Circle((cx, cy), 1.05, fc=colors[i], alpha=0.35,
                            ec=colors[i], lw=2))
    for key, pos in label_pos.items():
        ax.text(*pos, str(len(regions[key])), ha="center", va="center",
                fontsize=14, fontweight="bold")
    # nama himpunan + ukuran
    for i, n in enumerate(names):
        cx, cy = centers[i]
        dx = -1 if cx < 0 else (1 if cx > 0 else 0)
        dy = 1 if cy > 0 else -1
        ax.text(cx + dx * 0.9, cy + dy * 1.35, f"{n} ({len(sets[n])})",
                ha="center", fontsize=11, color=colors[i], fontweight="bold")
    outside = universe - union(*sets.values())
    ax.text(lim[0] + .25, lim[2] + .3, f"Di luar semua himpunan: {len(outside)}",
            fontsize=10)
    ax.text(lim[0] + .25, lim[3] - .3, f"|U| = {len(universe)}", fontsize=10)
    ax.set_xlim(lim[0], lim[1]); ax.set_ylim(lim[2], lim[3])
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(title, fontsize=12)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return regions


# ------------------------------------------------------------- LAPORAN
def fmt(s):
    return "{" + ", ".join(map(str, sorted(s))) + "}" if s else "{}"


def run_operation(op, names, universe, groups):
    sets = [groups[n] for n in names]
    if op == "union":
        res, rumus = union(*sets), " ∪ ".join(names)
    elif op == "intersection":
        res, rumus = intersection(*sets), " ∩ ".join(names)
    elif op == "difference":
        if len(names) != 2:
            raise ValueError("difference butuh tepat 2 himpunan")
        res, rumus = difference(*sets), f"{names[0]} − {names[1]}"
    elif op == "complement":
        if len(names) != 1:
            raise ValueError("complement butuh tepat 1 himpunan")
        res, rumus = complement(sets[0], universe), f"({names[0]})ᶜ"
    else:
        raise ValueError("operasi tidak dikenal")
    return rumus, res


def print_pie(sets, universe):
    total, detail = pie_count(sets)
    print("\n=== Prinsip Inklusi-Eksklusi ===")
    for k, sign, terms, sub in detail:
        s = "+" if sign > 0 else "−"
        print(f"  k={k} ({s}): " + "; ".join(f"|{t}|={v}" for t, v in terms)
              + f"  -> jumlah={sub}")
    langsung = len(union(*sets.values()))
    print(f"  Hasil PIE        : {total}")
    print(f"  Hitung langsung  : {langsung}")
    print(f"  Verifikasi       : {'COCOK' if total == langsung else 'TIDAK COCOK'}")
    print(f"  Di luar semua    : {len(universe) - total}")
    return total, langsung


def analyze(path, names, venn_path=None, title=None):
    universe, groups = load_dataset(path)
    sets = {n: groups[n] for n in names}
    print(f"\n##### Dataset: {path}  |U|={len(universe)}")
    for n, s in sets.items():
        print(f"  {n:12s} |{n}|={len(s):2d}  {fmt(s)}")
    if len(names) >= 2:
        for op in ("union", "intersection"):
            r, res = run_operation(op, names, universe, groups)
            print(f"  {op:12s} {r} = {fmt(res)}  (n={len(res)})")
    if len(names) == 2:
        for a, b in (names, names[::-1]):
            r, res = run_operation("difference", [a, b], universe, groups)
            print(f"  difference   {r} = {fmt(res)}  (n={len(res)})")
    r, res = run_operation("complement", [names[0]], universe, groups)
    print(f"  complement   {r} = {fmt(res)}  (n={len(res)})")
    pie = print_pie(sets, universe)
    if venn_path and len(names) in (2, 3):
        draw_venn(sets, universe, title or "Diagram Venn", venn_path)
        print(f"  Diagram Venn disimpan: {venn_path}")
    return universe, groups, pie


def demo():
    analyze("data/dataset1_keahlian_mahasiswa.csv",
            ["Desain", "Programming", "Video"],
            "output/venn_dataset1.png",
            "Dataset 1: Keahlian Mahasiswa (Desain, Programming, Video)")
    # Dataset 2 punya 4 kategori: PIE 4 himpunan + Venn 3 himpunan terpilih
    universe, groups, _ = analyze(
        "data/dataset2_platform_responden.csv",
        ["YouTube", "TikTok", "Instagram", "X"])
    analyze("data/dataset2_platform_responden.csv",
            ["YouTube", "TikTok", "Instagram"],
            "output/venn_dataset2.png",
            "Dataset 2: Platform Responden (YouTube, TikTok, Instagram)")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Klasifikasi Data dengan Himpunan")
    p.add_argument("--demo", action="store_true")
    p.add_argument("--data")
    p.add_argument("--sets", nargs="+")
    p.add_argument("--op", choices=["union", "intersection", "difference", "complement"])
    p.add_argument("--pie", action="store_true")
    p.add_argument("--venn")
    a = p.parse_args()
    if a.demo:
        demo()
    elif a.data and a.sets:
        U, G = load_dataset(a.data)
        if a.op:
            r, res = run_operation(a.op, a.sets, U, G)
            print(f"{r} = {fmt(res)}  (n={len(res)})")
        if a.pie:
            print_pie({n: G[n] for n in a.sets}, U)
        if a.venn:
            draw_venn({n: G[n] for n in a.sets}, U, "Diagram Venn", a.venn)
    else:
        p.print_help()
