#!/usr/bin/env python3
"""
Prototype 007A: RNA to GNA Linkage-Optimized Converter

Digital Polymerase / XNA World Project

GNA (glycerol nucleic acid) is a wild beast because its backbone is much smaller
than RNA, and it uses a glycerol-like scaffold rather than a ribose/threose ring.

The uploaded GNA template uses atoms such as:
    C1G, C2G, C3G, O2G, O3G

Observed GNA-like linkage logic from the template:
    P(i)    -> O3G(i)
    O2G(i) -> P(i+1)

This converter:
1. uses source RNA phosphate positions as a global guide,
2. selects GNA template residues by base class,
3. places a GNA-like glycerol scaffold,
4. locally optimizes the GNA scaffold to satisfy internal and polymer-linkage distances,
5. attaches the source RNA base to C1G.

Outputs are computational candidates only.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Tuple, Optional, List
import numpy as np
from scipy.optimize import least_squares


ResidueKey = Tuple[str, int, str]

GNA_ATOMS = ["C1G", "C2G", "C3G", "O2G", "O3G"]
BACKBONE_ORDER = ["P", "OP1", "OP2", "O3G", "C3G", "C2G", "O2G", "C1G"]


@dataclass
class Atom:
    record: str
    atom_name: str
    res_name: str
    chain: str
    res_num: int
    insertion_code: str
    coords: np.ndarray
    occupancy: float
    temp_factor: float
    element: str


@dataclass
class ConversionRecord:
    source_key: ResidueKey
    source_base: str
    target_res_name: str
    template_key: ResidueKey
    template_res_name: str
    align_rmsd: float
    base_shift: float
    opt_cost: float
    gly: Optional[float]
    p_o3g: Optional[float]
    o2g_next_p: Optional[float]
    note: str


@dataclass
class DistanceSummary:
    label: str
    measured: int
    missing: int
    failed: int
    mean: float
    minimum: float
    maximum: float
    lo: float
    hi: float


def infer_element(atom_name: str, pdb_element: str = "") -> str:
    elem = (pdb_element or "").strip()
    if elem and re.match(r"^[A-Za-z]{1,2}$", elem):
        return elem[0].upper() + elem[1:].lower()
    cleaned = re.sub(r"[^A-Za-z]", "", atom_name)
    if not cleaned:
        return ""
    return cleaned[0].upper()


def norm_phosphate_atom(name: str) -> str:
    return {"O1P": "OP1", "O2P": "OP2"}.get(name.strip(), name.strip())


def parse_pdb(path: Path, *, normalize_phosphate: bool = False) -> Dict[ResidueKey, Dict[str, Atom]]:
    residues = defaultdict(dict)
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.startswith(("ATOM", "HETATM")):
            continue
        try:
            raw = line[12:16].strip()
            name = norm_phosphate_atom(raw) if normalize_phosphate else raw
            resn = line[17:20].strip()
            chain = line[21].strip() or "A"
            rn = int(line[22:26].strip())
            ic = line[26].strip()
            xyz = np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])], dtype=float)
            occ = float(line[54:60].strip()) if len(line) >= 60 and line[54:60].strip() else 1.0
            temp = float(line[60:66].strip()) if len(line) >= 66 and line[60:66].strip() else 0.0
            elem = line[76:78].strip() if len(line) >= 78 else ""
            residues[(chain, rn, ic)][name] = Atom(
                record="HETATM",
                atom_name=name,
                res_name=resn,
                chain=chain,
                res_num=rn,
                insertion_code=ic,
                coords=xyz,
                occupancy=occ,
                temp_factor=temp,
                element=infer_element(name, elem),
            )
        except Exception:
            continue
    return dict(residues)


def keys(residues):
    return sorted(residues.keys(), key=lambda k: (k[0], k[1], k[2]))


def resname(residue):
    return next(iter(residue.values())).res_name


def base_of(residue_name: str) -> str:
    r = residue_name.upper().strip()
    if r in {"A", "U", "G", "C"}:
        return r
    if r in {"ZAD", "GNA", "A"} or r.endswith("A"):
        return "A"
    if r in {"ZGU", "G"} or r.endswith("G"):
        return "G"
    if r in {"ZCY", "C"} or r.endswith("C") or "CY" in r:
        return "C"
    if r in {"ZBU", "ZTH", "U", "T"} or r.endswith("U") or r.endswith("T") or "TH" in r:
        return "U"
    if r.startswith("A"):
        return "A"
    if r.startswith("G"):
        return "G"
    if r.startswith("C"):
        return "C"
    if r.startswith(("U", "T")):
        return "U"
    return "N"


def sequence(residues):
    return "".join(base_of(resname(residues[k])) for k in keys(residues))


def target_name(base: str, policy: str = "preserve") -> str:
    if policy == "dna-like":
        return {"A": "ZAD", "U": "ZTH", "G": "ZGU", "C": "ZCY"}.get(base, "ZGN")
    return {"A": "ZAD", "U": "ZBU", "G": "ZGU", "C": "ZCY"}.get(base, "ZGN")


def gly_atom(base: str) -> str:
    return "N9" if base in {"A", "G"} else "N1"


def source_base_atoms(residue):
    nonbase = {
        "P", "OP1", "OP2", "O1P", "O2P",
        "O5'", "C5'", "C4'", "O4'", "C3'", "O3'",
        "C2'", "O2'", "C1'",
    }
    return {n: a for n, a in residue.items() if n not in nonbase and "'" not in n}


def clone(atom, *, coords=None, atom_name=None, res_name=None, chain=None, res_num=None, insertion_code=None, element=None):
    name = atom_name if atom_name is not None else atom.atom_name
    return Atom(
        record="HETATM",
        atom_name=name,
        res_name=res_name if res_name is not None else atom.res_name,
        chain=chain if chain is not None else atom.chain,
        res_num=res_num if res_num is not None else atom.res_num,
        insertion_code=insertion_code if insertion_code is not None else atom.insertion_code,
        coords=np.array(coords if coords is not None else atom.coords, dtype=float),
        occupancy=atom.occupancy,
        temp_factor=atom.temp_factor,
        element=element if element is not None else infer_element(name, atom.element),
    )


def kabsch(mobile, target):
    mobile = np.asarray(mobile, dtype=float)
    target = np.asarray(target, dtype=float)
    if mobile.shape != target.shape or mobile.shape[0] < 3:
        raise ValueError("Kabsch alignment requires matching coordinate arrays with at least 3 anchors")
    mc = mobile.mean(axis=0)
    tc = target.mean(axis=0)
    m = mobile - mc
    t = target - tc
    u, s, vt = np.linalg.svd(m.T @ t)
    r = vt.T @ u.T
    if np.linalg.det(r) < 0:
        vt[-1, :] *= -1
        r = vt.T @ u.T
    trans = tc - r @ mc
    fitted = (r @ mobile.T).T + trans
    rmsd = float(np.sqrt(np.mean(np.sum((fitted - target) ** 2, axis=1))))
    return r, trans, rmsd


def apply(coord, r, t):
    return r @ coord + t


def distance(res_a, atom_a, res_b, atom_b, default):
    if res_a is not None and res_b is not None and atom_a in res_a and atom_b in res_b:
        return float(np.linalg.norm(res_a[atom_a].coords - res_b[atom_b].coords))
    return default


def build_template_index(template):
    ks = keys(template)
    idx = defaultdict(list)
    for i, k in enumerate(ks):
        res = template[k]
        # skip phosphate-only terminal fragments
        if not all(a in res for a in ["C1G", "C2G", "C3G", "O2G", "O3G"]):
            continue
        nk = ks[i + 1] if i + 1 < len(ks) and ks[i + 1][0] == k[0] else None
        pk = ks[i - 1] if i > 0 and ks[i - 1][0] == k[0] else None
        idx[base_of(resname(res))].append((k, res, nk, pk))
    return dict(idx)


def select_template(base, idx, counter):
    if base in idx and idx[base]:
        i = counter.get(base, 0)
        counter[base] = i + 1
        return idx[base][i % len(idx[base])], "exact base-class GNA template"
    if base == "U" and "T" in idx and idx["T"]:
        i = counter.get("T", 0)
        counter["T"] = i + 1
        return idx["T"][i % len(idx["T"])], "T-like donor for RNA U"
    if base in {"A", "G"}:
        for alt in ["A", "G"]:
            if alt in idx and idx[alt]:
                i = counter.get(alt, 0)
                counter[alt] = i + 1
                return idx[alt][i % len(idx[alt])], f"purine fallback: {alt}-like donor"
    if base in {"C", "U"}:
        for alt in ["C", "U", "T"]:
            if alt in idx and idx[alt]:
                i = counter.get(alt, 0)
                counter[alt] = i + 1
                return idx[alt][i % len(idx[alt])], f"pyrimidine fallback: {alt}-like donor"
    first = sorted(idx)[0]
    i = counter.get(first, 0)
    counter[first] = i + 1
    return idx[first][i % len(idx[first])], "last-resort fallback"


def initial_transform(tres, next_tres, sres, next_sres):
    mobile = []
    target = []
    used = []

    if "P" in tres and "P" in sres:
        mobile.append(tres["P"].coords)
        target.append(sres["P"].coords)
        used.append("P")

    if next_tres is not None and next_sres is not None and "P" in next_tres and "P" in next_sres:
        mobile.append(next_tres["P"].coords)
        target.append(next_sres["P"].coords)
        used.append("NEXT_P")

    # C1G is the base-bearing atom; align it near source C1'.
    if "C1G" in tres and "C1'" in sres:
        mobile.append(tres["C1G"].coords)
        target.append(sres["C1'"].coords)
        used.append("C1G→C1'")

    # Weak geometric hints from RNA sugar atoms.
    if "C2G" in tres and "C2'" in sres:
        mobile.append(tres["C2G"].coords)
        target.append(sres["C2'"].coords)
        used.append("C2G→C2'")
    if "C3G" in tres and "C3'" in sres:
        mobile.append(tres["C3G"].coords)
        target.append(sres["C3'"].coords)
        used.append("C3G→C3'")

    if len(mobile) < 3:
        # fallback: current P + C1 only is not enough; add template-internal projection toward source C3 if possible
        mobile = []
        target = []
        used = []
        for ta, sa in [("P", "P"), ("C1G", "C1'"), ("C3G", "C3'")]:
            if ta in tres and sa in sres:
                mobile.append(tres[ta].coords)
                target.append(sres[sa].coords)
                used.append(f"{ta}→{sa}")

    if len(mobile) < 3:
        raise ValueError(f"Not enough GNA initial anchors: {used}")

    r, t, rmsd = kabsch(np.array(mobile), np.array(target))
    return r, t, rmsd, used


def optimize_gna(initial, sres, next_sres, tres, next_tres):
    atoms = GNA_ATOMS
    x0 = np.concatenate([initial[a] for a in atoms])

    pairs = [
        ("C1G", "C2G", distance(tres, "C1G", tres, "C2G", 1.52), 20.0),
        ("C2G", "C3G", distance(tres, "C2G", tres, "C3G", 1.52), 20.0),
        ("C2G", "O2G", distance(tres, "C2G", tres, "O2G", 1.42), 20.0),
        ("C3G", "O3G", distance(tres, "C3G", tres, "O3G", 1.42), 20.0),
        # Shape-supporting distances.
        ("C1G", "C3G", distance(tres, "C1G", tres, "C3G", 2.50), 5.0),
        ("C1G", "O2G", distance(tres, "C1G", tres, "O2G", 2.39), 3.0),
        ("C2G", "O3G", distance(tres, "C2G", tres, "O3G", 2.41), 3.0),
    ]

    p_current = sres["P"].coords if "P" in sres else None
    p_next = next_sres["P"].coords if next_sres is not None and "P" in next_sres else None
    d_p_o3 = distance(tres, "P", tres, "O3G", 1.59)
    d_o2_next = distance(tres, "O2G", next_tres, "P", 1.59)

    c1_source = sres["C1'"].coords if "C1'" in sres else initial["C1G"]

    def unpack(x):
        return {a: x[i * 3:(i + 1) * 3] for i, a in enumerate(atoms)}

    def residuals(x):
        c = unpack(x)
        res = []
        for a, b, d, w in pairs:
            res.append(w * (np.linalg.norm(c[a] - c[b]) - d))
        if p_current is not None:
            res.append(15.0 * (np.linalg.norm(c["O3G"] - p_current) - d_p_o3))
        if p_next is not None:
            res.append(15.0 * (np.linalg.norm(c["O2G"] - p_next) - d_o2_next))
        # Keep C1G near the source base-bearing C1' region, but allow movement.
        res.extend(list(0.30 * (c["C1G"] - c1_source)))
        # Weak regularization against the initial template placement.
        for a in atoms:
            weight = 0.03 if p_next is not None else 0.01
            res.extend(list(weight * (c[a] - initial[a])))
        return np.array(res, dtype=float)

    fit = least_squares(residuals, x0, max_nfev=500, xtol=1e-8, ftol=1e-8, gtol=1e-8)
    return unpack(fit.x), float(fit.cost)


def attach_base_from_source(out_res, source_base_atoms_, source_residue, base, target_distance):
    """Translate source base so glycosidic atom is attached to C1G."""
    g = gly_atom(base)
    if "C1G" not in out_res or g not in source_base_atoms_ or "C1'" not in source_residue:
        return None, 0.0

    # Preserve source base orientation relative to the RNA base, but re-anchor it to C1G.
    source_c1 = source_residue["C1'"].coords
    source_g = source_base_atoms_[g].coords
    vec = source_g - source_c1
    d = float(np.linalg.norm(vec))
    if d < 1e-8:
        return None, 0.0

    desired = target_distance if target_distance is not None else d
    unit = vec / d
    new_g = out_res["C1G"].coords + desired * unit
    shift = new_g - source_g

    for name, atom in source_base_atoms_.items():
        out_res[name] = clone(
            atom,
            coords=atom.coords + shift,
            res_name=out_res["C1G"].res_name,
            chain=out_res["C1G"].chain,
            res_num=out_res["C1G"].res_num,
            insertion_code=out_res["C1G"].insertion_code,
        )

    gly_dist = float(np.linalg.norm(out_res["C1G"].coords - out_res[g].coords))
    shift_mag = float(np.linalg.norm(shift))
    return gly_dist, shift_mag


def convert(source, template, policy="preserve"):
    idx = build_template_index(template)
    if not idx:
        raise ValueError("Could not build GNA template index")

    skeys = keys(source)
    out = {}
    records = []
    counter = {}

    for i, skey in enumerate(skeys):
        sres = source[skey]
        next_skey = (
            skeys[i + 1]
            if i + 1 < len(skeys)
            and skeys[i + 1][0] == skey[0]
            and skeys[i + 1][1] == skey[1] + 1
            and not skey[2]
            and not skeys[i + 1][2]
            else None
        )
        next_sres = source[next_skey] if next_skey is not None else None

        base = base_of(resname(sres))
        (tkey, tres, next_tkey, prev_tkey), note = select_template(base, idx, counter)
        next_tres = template[next_tkey] if next_tkey is not None and next_tkey in template else None

        r, t, rmsd, used = initial_transform(tres, next_tres, sres, next_sres)

        initial = {}
        for a in GNA_ATOMS:
            if a not in tres:
                raise ValueError(f"Template residue {tkey} lacks required GNA atom {a}")
            initial[a] = apply(tres[a].coords, r, t)

        opt, cost = optimize_gna(initial, sres, next_sres, tres, next_tres)

        target_res = target_name(base, policy)
        out_res = {}

        # Preserve source phosphate group position as global chain guide.
        for raw in ["P", "OP1", "OP2", "O1P", "O2P"]:
            if raw in sres:
                name = norm_phosphate_atom(raw)
                out_res[name] = clone(
                    sres[raw],
                    atom_name=name,
                    res_name=target_res,
                    chain=skey[0],
                    res_num=skey[1],
                    insertion_code=skey[2],
                    element=infer_element(name),
                )

        for a in GNA_ATOMS:
            out_res[a] = clone(
                tres[a],
                coords=opt[a],
                atom_name=a,
                res_name=target_res,
                chain=skey[0],
                res_num=skey[1],
                insertion_code=skey[2],
                element=infer_element(a),
            )

        # Base attachment: use template C1G->N distance if available.
        desired_gly = None
        g = gly_atom(base)
        if "C1G" in tres and g in tres:
            desired_gly = float(np.linalg.norm(tres["C1G"].coords - tres[g].coords))
        gly, base_shift = attach_base_from_source(out_res, source_base_atoms(sres), sres, base, desired_gly)

        p_o3 = float(np.linalg.norm(out_res["P"].coords - out_res["O3G"].coords)) if "P" in out_res else None
        o2_next = (
            float(np.linalg.norm(out_res["O2G"].coords - source[next_skey]["P"].coords))
            if next_skey is not None and "P" in source[next_skey]
            else None
        )

        out[skey] = out_res
        records.append(
            ConversionRecord(
                source_key=skey,
                source_base=base,
                target_res_name=target_res,
                template_key=tkey,
                template_res_name=resname(tres),
                align_rmsd=rmsd,
                base_shift=base_shift,
                opt_cost=cost,
                gly=gly,
                p_o3g=p_o3,
                o2g_next_p=o2_next,
                note=note + "; GNA linkage-optimized glycerol scaffold",
            )
        )

    return out, records


def fmt_atom(serial, atom):
    elem = (atom.element or infer_element(atom.atom_name))[:2].rjust(2)
    icode = (atom.insertion_code or " ")[:1]
    return (
        f"{atom.record:<6s}{serial:5d} {atom.atom_name[:4]:>4s} {atom.res_name[:3]:>3s} "
        f"{(atom.chain or 'A')[:1]}{atom.res_num:4d}{icode}   "
        f"{atom.coords[0]:8.3f}{atom.coords[1]:8.3f}{atom.coords[2]:8.3f}"
        f"{atom.occupancy:6.2f}{atom.temp_factor:6.2f}{'':>10s}{elem:>2s}"
    )


def atom_order(name):
    return (BACKBONE_ORDER.index(name), name) if name in BACKBONE_ORDER else (100, name)


def write_pdb(residues, path, src_seq, tmpl_seq):
    with path.open("w", encoding="utf-8") as f:
        f.write("REMARK   Digital Polymerase Prototype 007A\n")
        f.write("REMARK   RNA to GNA linkage-optimized candidate reconstruction\n")
        f.write(f"REMARK   Source RNA sequence: {src_seq}\n")
        f.write(f"REMARK   GNA template base-class sequence: {tmpl_seq}\n")
        f.write("REMARK   GNA linkage model: P(i)->O3G(i), O2G(i)->P(i+1)\n")
        f.write("REMARK   WARNING: Computational candidate only; not physically validated\n")
        f.write("CRYST1    1.000    1.000    1.000  90.00  90.00  90.00 P 1           1\n")
        serial = 1
        for k in keys(residues):
            for name in sorted(residues[k], key=atom_order):
                f.write(fmt_atom(serial, residues[k][name]) + "\n")
                serial += 1
        f.write("END\n")


def validate_intra(residues, a, b, lo, hi, label):
    vals = []
    missing = 0
    for k in keys(residues):
        if a not in residues[k] or b not in residues[k]:
            missing += 1
            continue
        vals.append(float(np.linalg.norm(residues[k][a].coords - residues[k][b].coords)))
    failed = sum(1 for v in vals if not (lo <= v <= hi))
    return DistanceSummary(
        label=label,
        measured=len(vals),
        missing=missing,
        failed=failed,
        mean=float(np.mean(vals)) if vals else float("nan"),
        minimum=float(np.min(vals)) if vals else float("nan"),
        maximum=float(np.max(vals)) if vals else float("nan"),
        lo=lo,
        hi=hi,
    )


def validate_inter(residues, a, b, lo, hi, label):
    ks = keys(residues)
    vals = []
    missing = 0
    for lk, rk in zip(ks[:-1], ks[1:]):
        if lk[0] != rk[0] or rk[1] != lk[1] + 1 or lk[2] or rk[2]:
            continue
        if a not in residues[lk] or b not in residues[rk]:
            missing += 1
            continue
        vals.append(float(np.linalg.norm(residues[lk][a].coords - residues[rk][b].coords)))
    failed = sum(1 for v in vals if not (lo <= v <= hi))
    return DistanceSummary(
        label=label,
        measured=len(vals),
        missing=missing,
        failed=failed,
        mean=float(np.mean(vals)) if vals else float("nan"),
        minimum=float(np.min(vals)) if vals else float("nan"),
        maximum=float(np.max(vals)) if vals else float("nan"),
        lo=lo,
        hi=hi,
    )


def validate_gly(residues):
    vals = []
    missing = 0
    for k in keys(residues):
        b = base_of(resname(residues[k]))
        g = gly_atom(b)
        if "C1G" not in residues[k] or g not in residues[k]:
            missing += 1
            continue
        vals.append(float(np.linalg.norm(residues[k]["C1G"].coords - residues[k][g].coords)))
    failed = sum(1 for v in vals if not (1.25 <= v <= 1.75))
    return DistanceSummary("C1G→glycosidic N", len(vals), missing, failed, float(np.mean(vals)) if vals else float("nan"), float(np.min(vals)) if vals else float("nan"), float(np.max(vals)) if vals else float("nan"), 1.25, 1.75)


def status(s):
    return "NO_DATA" if s.measured == 0 else ("PASS" if s.failed == 0 else "FAIL")


def build_validation(output):
    return {
        "GNA O2G(i)→P(i+1)": validate_inter(output, "O2G", "P", 1.25, 1.95, "GNA O2G(i)→P(i+1)"),
        "GNA P(i)→O3G(i)": validate_intra(output, "P", "O3G", 1.25, 1.95, "GNA P(i)→O3G(i)"),
        "C1G→glycosidic N": validate_gly(output),
        "C1G→C2G": validate_intra(output, "C1G", "C2G", 1.30, 1.80, "C1G→C2G"),
        "C2G→C3G": validate_intra(output, "C2G", "C3G", 1.30, 1.80, "C2G→C3G"),
        "C2G→O2G": validate_intra(output, "C2G", "O2G", 1.20, 1.65, "C2G→O2G"),
        "C3G→O3G": validate_intra(output, "C3G", "O3G", 1.20, 1.65, "C3G→O3G"),
    }


def validation_table(checks):
    lines = [
        "| Metric | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |",
        "|---|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for label, s in checks.items():
        lines.append(
            f"| {label} | {s.measured} | {s.missing} | {s.failed} | {s.mean:.3f} | {s.minimum:.3f} | {s.maximum:.3f} | {s.lo:.2f}–{s.hi:.2f} | {status(s)} |"
        )
    return "\n".join(lines)


def write_report(path, source_path, template_path, output_path, source, template, output, records):
    checks = build_validation(output)
    rmsd = [r.align_rmsd for r in records]
    shifts = [r.base_shift for r in records]
    costs = [r.opt_cost for r in records]
    gly = [r.gly for r in records if r.gly is not None]
    po3 = [r.p_o3g for r in records if r.p_o3g is not None]
    o2p = [r.o2g_next_p for r in records if r.o2g_next_p is not None]

    rec_lines = []
    for i, r in enumerate(records, 1):
        rec_lines.append(
            f"| {i} | {r.source_key[0]}{r.source_key[1]}{r.source_key[2]} | {r.source_base} | "
            f"{r.target_res_name} | {r.template_res_name} {r.template_key[0]}{r.template_key[1]}{r.template_key[2]} | "
            f"{r.align_rmsd:.4f} | {r.base_shift:.4f} | {r.opt_cost:.4f} | "
            f"{r.gly if r.gly is not None else 'NA'} | {r.p_o3g if r.p_o3g is not None else 'NA'} | "
            f"{r.o2g_next_p if r.o2g_next_p is not None else 'NA'} | {r.note} |"
        )

    md = f"""# RNA → GNA Conversion Report

**Project:** Digital Polymerase  
**Prototype:** 007A  
**Method:** Linkage-optimized GNA reconstruction  
**Status:** Experimental candidate, not physically validated  
**GNA chain-continuity status:** `O2G(i)→P(i+1) {status(checks["GNA O2G(i)→P(i+1)"])}`, `P(i)→O3G(i) {status(checks["GNA P(i)→O3G(i)"])}`  
**Base-attachment status:** `{status(checks["C1G→glycosidic N"])}`  
**Local GNA scaffold status:** `C1G→C2G {status(checks["C1G→C2G"])}`, `C2G→C3G {status(checks["C2G→C3G"])}`, `C2G→O2G {status(checks["C2G→O2G"])}`, `C3G→O3G {status(checks["C3G→O3G"])}`

---

## Inputs

- Source RNA PDB: `{source_path}`
- GNA template PDB: `{template_path}`
- Output PDB: `{output_path}`

---

## Source and Template

- Source RNA sequence: `{sequence(source)}`
- GNA template base-class sequence: `{sequence(template)}`
- Source residue count: `{len(keys(source))}`
- Template residue count: `{len(keys(template))}`
- Converted residues: `{len(records)}`

---

## Why GNA Is Difficult

GNA is not a pentose-like local edit. It uses a much smaller glycerol-like scaffold.

The uploaded GNA template uses atoms such as:

```text
C1G
C2G
C3G
O2G
O3G
```

The observed GNA-like linkage pattern is:

```text
P(i)    → O3G(i)
O2G(i) → P(i+1)
```

Therefore, this prototype treats GNA as a linkage-remapped and scaffold-optimized reconstruction problem, not as a simple RNA sugar modification.

---

## Method Summary

Prototype 007A performs linkage-optimized GNA reconstruction:

1. parse source RNA and GNA template PDB files
2. infer source base identity
3. select a GNA template residue by base class
4. use source RNA phosphate positions as the global chain guide
5. generate an initial GNA glycerol scaffold from the template
6. locally optimize GNA scaffold distances
7. attach source RNA bases to `C1G`
8. export a GNA-like candidate PDB
9. validate GNA-specific linkages and scaffold geometry

---

## Alignment / Optimization Summary

- Mean initial alignment RMSD: `{np.mean(rmsd):.4f} Å`
- Maximum initial alignment RMSD: `{np.max(rmsd):.4f} Å`
- Mean base shift: `{np.mean(shifts):.4f} Å`
- Maximum base shift: `{np.max(shifts):.4f} Å`
- Mean optimization cost: `{np.mean(costs):.4f}`
- Mean C1G→glycosidic N distance: `{np.mean(gly) if gly else float('nan'):.4f} Å`
- Mean P(i)→O3G(i) distance: `{np.mean(po3) if po3 else float('nan'):.4f} Å`
- Mean O2G(i)→P(i+1) distance: `{np.mean(o2p) if o2p else float('nan'):.4f} Å`

---

## Structural Validation

{validation_table(checks)}

---

## Per-Residue Conversion

| # | Source residue | Base | Output residue | Template used | Initial RMSD (Å) | Base shift (Å) | Opt. cost | C1G–N (Å) | P–O3G (Å) | O2G–next P (Å) | Note |
|---:|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
{chr(10).join(rec_lines)}

---

## Scientific Interpretation

This output should be interpreted as:

> a GNA-like computational candidate generated by linkage-optimized glycerol-scaffold reconstruction.

It should **not** be interpreted as:

> a chemically validated, experimentally confirmed, or MD-ready GNA structure.

---

## Important Limitations

- Not energy-minimized.
- No force-field parameters are generated.
- No topology files are generated.
- No explicit `CONECT` records are written.
- GNA stereochemistry requires expert inspection.
- Molecular viewers may not render standard nucleic-acid cartoon paths reliably for GNA-like structures.
- The output is a candidate geometry only; biological function, stability, replication, or catalytic activity is not implied.
"""
    path.write_text(md, encoding="utf-8")


def run(source_path: Path, template_path: Path, output_path: Path, report_path: Path):
    source = parse_pdb(source_path, normalize_phosphate=False)
    template = parse_pdb(template_path, normalize_phosphate=True)
    output, records = convert(source, template)
    write_pdb(output, output_path, sequence(source), sequence(template))
    write_report(report_path, source_path, template_path, output_path, source, template, output, records)

    checks = build_validation(output)
    print("=" * 80)
    print("Digital Polymerase Prototype 007A")
    print("RNA → GNA linkage-optimized candidate reconstruction")
    print("=" * 80)
    print(f"Source RNA: {source_path}")
    print(f"GNA template: {template_path}")
    print(f"Output PDB: {output_path}")
    print(f"Report: {report_path}")
    print(f"Source sequence: {sequence(source)}")
    print(f"Template sequence: {sequence(template)}")
    print(f"Converted residues: {len(records)}")
    print("-" * 80)
    for label in ["GNA O2G(i)→P(i+1)", "GNA P(i)→O3G(i)", "C1G→glycosidic N", "C1G→C2G", "C2G→C3G", "C2G→O2G", "C3G→O3G"]:
        s = checks[label]
        print(f"{label}: {status(s)} (measured={s.measured}, failed={s.failed}, mean={s.mean:.3f} Å)")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="Prototype 007A: RNA to GNA linkage-optimized converter.")
    parser.add_argument("--rna", required=True, type=Path, help="Source RNA PDB")
    parser.add_argument("--template", required=True, type=Path, help="GNA template PDB")
    parser.add_argument("--output", required=True, type=Path, help="Output GNA-like candidate PDB")
    parser.add_argument("--report", required=True, type=Path, help="Output Markdown report")
    args = parser.parse_args()
    run(args.rna, args.template, args.output, args.report)


if __name__ == "__main__":
    main()
