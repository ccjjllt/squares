"""Record-table f(D) analysis + centered-diagonal-block generator.

Part 1 (mode=table)   : n = K^2 + D, f = L - K statistics over the record table.
Part 2 (mode=blocks)  : Friedman DS7 "centered diagonal block" family, relaxed
                        to keep every lattice cell that clears the diamond.

Layout model (lengths in units of the packed unit square)
---------------------------------------------------------
Box side L = K + s.
* "lower" lattice columns/rows : integers 0 .. p-1
* "upper" lattice columns/rows : s + p .. s + K - 1
* a b x b block of unit squares rotated 45 deg, centred at (cx, cy),
  occupying the L1 diamond |x-cx| + |y-cy| <= b/sqrt2
* every lattice cell [i,i+1]x[j,j+1] whose L1 distance to (cx,cy) is
  >= b/sqrt2 - eps is kept (touching allowed).

Published special cases of this family (Friedman, EJC DS7):
  n=26: s = 7/2 + 3/sqrt2   (p=3, b=3)   -> f = 0.621320
  n=65: s = 5 + 5/sqrt2     (p=4, b=5)   -> f = 0.535534
  n=85: s = 11/2 + 3*sqrt2  (p=4, b=6)   -> f = 0.742641
  n=89: s = 5 + 7/sqrt2     (p=4, b=7)   -> f = 0.949747
"""

from __future__ import annotations

import argparse
import bisect
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REC = ROOT / "data/references/leaderboards/perpuzzle_best_20261029.csv"
OUT = ROOT / "outputs/experiments/research_20261111/literature"

CANDIDATES = {
    "1/sqrt2": 1 / math.sqrt(2),
    "(sqrt5-1)/2": (math.sqrt(5) - 1) / 2,
    "2/sqrt5": 2 / math.sqrt(5),
    "1/sqrt3": 1 / math.sqrt(3),
    "sqrt2-1": math.sqrt(2) - 1,
    "sqrt3-1": math.sqrt(3) - 1,
    "2-sqrt3": 2 - math.sqrt(3),
    "3-2sqrt2": 3 - 2 * math.sqrt(2),
    "1/(2sqrt2)": 1 / (2 * math.sqrt(2)),
    "sqrt5-2": math.sqrt(5) - 2,
    "2sqrt2-2": 2 * math.sqrt(2) - 2,
    "4-sqrt13": 4 - math.sqrt(13),
    "sqrt13-3": math.sqrt(13) - 3,
    "5/sqrt2-3": 5 / math.sqrt(2) - 3,
    "(3/2)(sqrt2-1)": 1.5 * (math.sqrt(2) - 1),
    "4-2sqrt2": 4 - 2 * math.sqrt(2),
    "7/2+3/sqrt2-K5": 3.5 + 3 / math.sqrt(2) - 5,
}


# ---------------------------------------------------------------- part 1 ---
def load() -> list[dict]:
    rows = []
    with REC.open() as fh:
        for r in csv.DictReader(fh):
            n = int(r["n"])
            L = float(r["L"])
            if L <= 0:
                continue
            rows.append({"n": n, "L": L})
    rows.sort(key=lambda r: r["n"])
    for r in rows:
        n = r["n"]
        K = math.isqrt(n)
        r["K"] = K
        r["D"] = n - K * K
        r["f"] = r["L"] - K
    return rows


def cluster_f(rows: list[dict], tol: float = 5e-10) -> list[dict]:
    groups: list[dict] = []
    for r in sorted(rows, key=lambda r: r["f"]):
        for g in groups:
            if abs(r["f"] - g["f"]) <= tol:
                g["ns"].append(r)
                break
        else:
            groups.append({"f": r["f"], "ns": [r]})
    return groups


def best_const(f: float) -> tuple[str, float]:
    name, val = min(CANDIDATES.items(), key=lambda kv: abs(kv[1] - f))
    return name, abs(val - f)


def table() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = load()
    by_n = {r["n"]: r for r in rows}
    nontrivial = [r for r in rows if r["n"] >= 2 and (r["f"] < 1 - 1e-6 or r["D"] == 0)]

    clusters = sorted(cluster_f(nontrivial), key=lambda g: -len(g["ns"]))
    cluster_report = []
    for g in clusters:
        if len(g["ns"]) < 2:
            continue
        name, resid = best_const(g["f"])
        cluster_report.append({
            "f": g["f"], "count": len(g["ns"]), "const": name, "const_resid": resid,
            "members": [[r["n"], r["K"], r["D"]] for r in g["ns"]],
            "Ds": sorted({r["D"] for r in g["ns"]}),
            "Ks": sorted({r["K"] for r in g["ns"]}),
        })

    by_d: dict[int, list[dict]] = defaultdict(list)
    for r in nontrivial:
        by_d[r["D"]].append(r)
    per_d = []
    for D in sorted(by_d):
        b = min(by_d[D], key=lambda r: r["f"])
        name, resid = best_const(b["f"])
        per_d.append({"D": D, "f_min": b["f"], "n": b["n"], "K": b["K"], "L": b["L"],
                      "const": name, "const_resid": resid, "count_D": len(by_d[D]),
                      "f_median": sorted(r["f"] for r in by_d[D])[len(by_d[D]) // 2]})

    xs = [(d["D"], d["f_min"]) for d in per_d if d["D"] >= 1]
    m = len(xs)
    sx = sum(math.log(D) for D, _ in xs)
    sy = sum(math.log(f) for _, f in xs)
    sxx = sum(math.log(D) ** 2 for D, _ in xs)
    sxy = sum(math.log(D) * math.log(f) for D, f in xs)
    p = (m * sxy - sx * sy) / (m * sxx - sx * sx)
    c = math.exp((sy - p * sx) / m)
    cs = [f * math.sqrt(D) for D, f in xs]
    cs24 = [f * math.sqrt(D) for D, f in xs if D <= 24]

    def resid(formula):
        out = [{"D": d["D"], "f_min": d["f_min"], "pred": formula(d["D"]),
                "resid": d["f_min"] - formula(d["D"])} for d in per_d]
        err = [abs(o["resid"]) for o in out]
        return {"max_abs": max(err), "rms": math.sqrt(sum(e * e for e in err) / len(err)),
                "table": out}

    fits = {
        "power": {"c": c, "p": p, "resid": resid(lambda D: c * D ** p if D >= 1 else 0.0)},
        "c_over_sqrtD_D24": {"c": sum(cs24) / len(cs24),
                             "resid": resid(lambda D: (sum(cs24) / len(cs24)) / math.sqrt(D) if D >= 1 else 0.0)},
        "c_over_sqrtD_all": {"c_mean": sum(cs) / len(cs), "c_min": min(cs), "c_max": max(cs)},
    }

    fixed_d = []
    for D in sorted(by_d):
        fs: dict[float, list] = {}
        for r in by_d[D]:
            fs.setdefault(round(r["f"], 9), []).append((r["n"], r["K"]))
        multi = {k: v for k, v in fs.items() if len(v) >= 2}
        if multi:
            fixed_d.append({"D": D, "same_f_groups": multi})

    kd = []
    for D in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16, 21]:
        ent = {"D": D}
        for K in range(1, 32):
            n = K * K + D
            if n in by_n:
                ent[str(K)] = round(by_n[n]["f"], 9)
        kd.append(ent)

    report = {"n_rows": len(rows), "clusters_repeated": cluster_report, "per_D": per_d,
              "fits": {k: {kk: vv for kk, vv in v.items() if kk != "resid"} for k, v in fits.items()},
              "fit_residuals": {k: {"max_abs": v["resid"]["max_abs"], "rms": v["resid"]["rms"]}
                                for k, v in fits.items() if "resid" in v},
              "fixed_D_multiple_K": fixed_d, "f_by_K_at_D": kd,
              "top_gap_records": sorted([r for r in rows if r["n"] >= 2],
                                        key=lambda r: -r["f"])[:40]}
    (OUT / "record_family.json").write_text(json.dumps(report, indent=1))

    lines = ["# Record-table f(D) analysis", "", "f = L - K, K = floor(sqrt n), D = n - K^2.", ""]
    lines += ["## min f per D (best known record, non-trivial packings)", "",
              "| D | f_min | n | K | L | radical form | resid | #records D | f_median |",
              "|---|---|---|---|---|---|---|---|---|"]
    for d in per_d:
        lines.append("| {} | {:.12f} | {} | {} | {:.12f} | {} | {:.2e} | {} | {:.6f} |".format(
            d["D"], d["f_min"], d["n"], d["K"], d["L"], d["const"], d["const_resid"],
            d["count_D"], d["f_median"]))
    lines += ["", "## Repeated exact f values (>=2 puzzles)", "",
              "| f | count | nearest form | resid | D set | K set |", "|---|---|---|---|---|---|"]
    for c_ in cluster_report[:40]:
        lines.append("| {:.12f} | {} | {} | {:.2e} | {} | {} |".format(
            c_["f"], c_["count"], c_["const"], c_["const_resid"],
            ",".join(map(str, c_["Ds"])), ",".join(map(str, c_["Ks"]))))
    lines += ["", "## fits", "", "```json",
              json.dumps(report["fits"] | report["fit_residuals"], indent=1), "```", "",
              "## f by K at fixed D", ""]
    for ent in kd:
        lines.append(str(ent))
    (OUT / "record_family.md").write_text("\n".join(lines) + "\n")
    print("wrote", OUT / "record_family.json")
    print("fits:", json.dumps(report["fit_residuals"]))
    for c_ in cluster_report[:10]:
        print("f={:.12f} n={} const={} resid={:.1e} D={}".format(
            c_["f"], c_["count"], c_["const"], c_["const_resid"], c_["Ds"][:8]))


# ---------------------------------------------------------------- part 2 ---
def columns(K: int, p: int, s: float) -> list[float]:
    return [float(i) for i in range(p)] + [s + i for i in range(p, K)]


CLEAR = 1e-6  # required strict clearance between an upright cell and the diamond


def count_cells(K: int, p: int, s: float, b: float, cy: float) -> int:
    L = K + s
    cx = L / 2.0
    r = b / math.sqrt(2.0)
    cols = columns(K, p, s)

    def d(v):
        return max(0.0, v - cx, cx - v - 1.0)

    def dy(v):
        return max(0.0, v - cy, cy - v - 1.0)

    dys = sorted(dy(v) for v in cols)
    n = 0
    for v in cols:
        need = r + CLEAR - d(v)
        n += len(dys) - bisect.bisect_left(dys, need)
    return n


def best_for(K: int, n: int, bmax: int = 26, s_hi: float = 1.0,
             ds: float = 0.004, tys: int = 17) -> dict | None:
    best = None
    for p in range(1, K):
        for b in range(2, min(bmax, K) + 1):
            if b * b > n:
                break
            need = n - b * b
            if need > K * K:
                continue
            for ti in range(tys):
                cy_off = -0.9 + 1.8 * ti / (tys - 1)
                s = 0.0
                while s < s_hi:
                    s += ds
                    L = K + s
                    cy = L / 2.0 + cy_off
                    r = b / math.sqrt(2.0)
                    if cy - r < -1e-12 or cy + r > L + 1e-12:
                        continue
                    if count_cells(K, p, s, b, cy) >= need:
                        if best is None or s < best["s"] - 1e-15:
                            best = {"K": K, "n": n, "p": p, "b": b, "s": s,
                                    "cy_off": cy_off, "L": L}
                        break
    return best


def build(K: int, p: int, b: float, s: float, cy_off: float, n: int):
    L = K + s
    cx = L / 2.0
    cy = L / 2.0 + cy_off
    r = b / math.sqrt(2.0)
    cols = columns(K, p, s)
    sq = []
    for i in cols:
        for j in cols:
            dx = max(0.0, i - cx, cx - i - 1.0)
            dy = max(0.0, j - cy, cy - j - 1.0)
            if dx + dy >= r + CLEAR:
                sq.append((i + 0.5, j + 0.5, 0.0))
    c45 = math.sin(math.pi / 4)
    for u in range(int(round(b))):
        for v in range(int(round(b))):
            lx = u + 0.5 - b / 2.0
            ly = v + 0.5 - b / 2.0
            sq.append((cx + c45 * (lx - ly), cy + c45 * (lx + ly), 45.0))
    if len(sq) < n:
        raise RuntimeError(f"not enough squares {len(sq)} < {n}")
    sq = sq[:n]
    ex = [x - (abs(math.cos(math.radians(a))) + abs(math.sin(math.radians(a)))) / 2 for x, y, a in sq]
    ey = [y - (abs(math.cos(math.radians(a))) + abs(math.sin(math.radians(a)))) / 2 for x, y, a in sq]
    ox, oy = min(ex), min(ey)
    return [(x - ox, y - oy, a) for x, y, a in sq]


def bbox_side(sq) -> float:
    hi = -1e9
    lox = loy = 1e9
    for x, y, a in sq:
        e = (abs(math.cos(math.radians(a))) + abs(math.sin(math.radians(a)))) / 2
        hi = max(hi, x + e, y + e)
        lox = min(lox, x - e)
        loy = min(loy, y - e)
    return max(hi - min(lox, loy), hi)


def blocks(targets: list[int], s_hi: float, ds: float) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rec = {int(r["n"]): float(r["L"]) for r in csv.DictReader(REC.open())}
    report = {"targets": [], "params": {"s_hi": s_hi, "ds": ds}}
    for n in targets:
        K = math.isqrt(n)
        bb = best_for(K, n, s_hi=s_hi, ds=ds)
        if bb is None:
            print(f"n={n}: no feasible parameter")
            report["targets"].append({"n": n, "K": K, "found": False})
            continue
        sq = build(bb["K"], bb["p"], bb["b"], bb["s"], bb["cy_off"], n)
        bb["L_bbox"] = bbox_side(sq)
        bb["record_L"] = rec[n]
        bb["beats_record"] = bb["L_bbox"] < rec[n]
        bb["squares"] = sq
        report["targets"].append(bb)
        print(f"n={n:4d} K={K:2d} p={bb['p']:2d} b={bb['b']:2d} s={bb['s']:.4f} "
              f"L={bb['L_bbox']:.6f} f={bb['L_bbox']-K:.6f} rec={rec[n]:.6f} "
              f"{'BEATS' if bb['beats_record'] else ''}")
    (OUT / "centered_diagonal_block.json").write_text(json.dumps(report, indent=1))


def emit(targets: list[int], s_hi: float, ds: float) -> None:
    """Certify CDB candidates against the official metric and the current best.

    NOTE the CSV/leaderboard convention trap: the submission CSV stores
    ``angle`` in RADIANS (the official metric reduces it mod 2*pi), while the
    evand atlas stores degrees.
    """
    import csv as _csv
    import sys as _sys

    _sys.path.insert(0, str(ROOT / "src"))
    from squares._vendor import official_metric as om

    rec = {int(r["n"]): float(r["L"]) for r in _csv.DictReader(REC.open())}
    cur: dict[int, float] = {}
    boxes: dict[int, list[float]] = {}
    sub = ROOT / "outputs/merged/v124_plus_daily44_public2/submission.csv"
    for r in _csv.DictReader(sub.open()):
        n = int(r["n"])
        x, y, a = float(r["x"]), float(r["y"]), float(r["angle"])  # angle in RADIANS
        e = (abs(math.cos(a)) + abs(math.sin(a))) / 2
        b = boxes.setdefault(n, [1e9, 1e9, -1e9, -1e9])
        b[0] = min(b[0], x - e)
        b[1] = min(b[1], y - e)
        b[2] = max(b[2], x + e)
        b[3] = max(b[3], y + e)
    for n, b in boxes.items():
        cur[n] = max(b[2] - b[0], b[3] - b[1])

    certified = []
    for n in targets:
        K = math.isqrt(n)
        bb = best_for(K, n, s_hi=s_hi, ds=ds, tys=9)
        if bb is None:
            print(f"n={n}: no CDB parameter")
            continue
        # nudge s off the tangency threshold so contacts become real gaps
        s = bb["s"] + 1e-6
        sq = build(bb["K"], bb["p"], bb["b"], s, bb["cy_off"], n)
        rows = [{"id": str(n), "n": str(n), "square_id": str(i),
                 "x": repr(float(x)), "y": repr(float(y)),
                 "angle": repr(math.radians(a))} for i, (x, y, a) in enumerate(sq)]
        _, score, L, reason = om.evaluate_single_puzzle(n, rows)
        tag = "INVALID" if L is None else (
            "beats_record" if float(L) < rec[n] else
            "beats_current" if float(L) < cur[n] else "worse")
        print(f"n={n:4d} K={K:2d} p={bb['p']:2d} b={bb['b']:2d} s={s:.6f} "
              f"L={L} cur={cur[n]:.6f} rec={rec[n]:.6f} -> {tag}"
              + ("" if L else f" ({reason[:60]})"))
        if L is not None and float(L) < cur[n]:
            certified.append({"n": n, "L": float(L), "squares": sq,
                              "params": {"p": bb["p"], "b": bb["b"], "s": s,
                                         "cy_off": bb["cy_off"]}})

    # improved_groups.csv: complete n groups that beat the current submission
    out_csv = OUT / "improved_groups.csv"
    with out_csv.open("w", newline="") as fh:
        w = _csv.writer(fh)
        w.writerow(["id", "n", "square_id", "x", "y", "angle"])
        sid = 0
        for g in certified:
            for i, (x, y, a) in enumerate(g["squares"]):
                w.writerow([sid, g["n"], i, repr(float(x)), repr(float(y)),
                            repr(math.radians(a))])
                sid += 1
    (OUT / "cdb_certified.json").write_text(json.dumps(
        [{k: v for k, v in g.items() if k != "squares"} for g in certified], indent=1))
    print(f"wrote {out_csv} with {len(certified)} certified improved group(s)")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="table", choices=("table", "blocks", "emit", "both"))
    ap.add_argument("--targets", default="971,911,910,791,972,793,908,969,862,687,328")
    ap.add_argument("--s-hi", type=float, default=1.0)
    ap.add_argument("--ds", type=float, default=0.004)
    a = ap.parse_args()
    if a.mode in ("table", "both"):
        table()
    if a.mode in ("blocks", "both"):
        blocks([int(t) for t in a.targets.split(",")], a.s_hi, a.ds)
    if a.mode == "emit":
        emit([int(t) for t in a.targets.split(",")], a.s_hi, a.ds)


if __name__ == "__main__":
    main()
