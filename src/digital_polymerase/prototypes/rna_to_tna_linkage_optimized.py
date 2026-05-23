#!/usr/bin/env python3
"""
Prototype 006B.4: RNA to TNA Linkage-Optimized Converter

Digital Polymerase / XNA World Project

This prototype was built after Prototype 006A/006A.1 showed that TNA cannot be
handled as a simple chain-preserving local replacement.

TNA linkage logic:
    P(i)    -> O3'(i)
    O2'(i) -> P(i+1)

The converter:
1. uses source RNA phosphate positions as a global guide,
2. places a TNA-like sugar scaffold from a TNA template segment,
3. locally optimizes each TNA sugar so P(i)-O3'(i), O2'(i)-P(i+1), and internal
   sugar distances are simultaneously improved,
4. transplants the RNA base onto the optimized TNA-like sugar.

Outputs are computational candidates only.
"""

from __future__ import annotations
import argparse, re
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Tuple, List, Optional
import numpy as np
from scipy.optimize import least_squares

ResidueKey = Tuple[str, int, str]
SUGAR_ATOMS = ["C1'", "C2'", "C3'", "C4'", "O4'", "O2'", "O3'"]
BACKBONE_ORDER = ["P", "OP1", "OP2", "O3'", "C3'", "C2'", "O2'", "C1'", "O4'", "C4'"]

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
    base_rmsd: float
    opt_cost: float
    gly: Optional[float]
    p_o3: Optional[float]
    o2_next_p: Optional[float]
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


def infer_element(atom_name, pdb_element=""):
    elem = (pdb_element or "").strip()
    if elem and re.match(r"^[A-Za-z]{1,2}$", elem):
        return elem[0].upper() + elem[1:].lower()
    cleaned = re.sub(r"[^A-Za-z]", "", atom_name)
    return cleaned[0].upper() if cleaned else ""


def norm_atom(name):
    return {
        "C1T": "C1'", "C2T": "C2'", "C3T": "C3'", "C4T": "C4'",
        "O2T": "O2'", "O3T": "O3'", "O4T": "O4'",
        "O1P": "OP1", "O2P": "OP2",
    }.get(name.strip(), name.strip())


def parse_pdb(path: Path, normalize=False):
    residues = defaultdict(dict)
    for line in path.read_text(errors="replace").splitlines():
        if not line.startswith(("ATOM", "HETATM")):
            continue
        try:
            raw = line[12:16].strip()
            name = norm_atom(raw) if normalize else raw
            resn = line[17:20].strip()
            chain = line[21].strip() or "A"
            rn = int(line[22:26])
            ic = line[26].strip()
            xyz = np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])], dtype=float)
            occ = float(line[54:60].strip()) if len(line) >= 60 and line[54:60].strip() else 1.0
            temp = float(line[60:66].strip()) if len(line) >= 66 and line[60:66].strip() else 0.0
            elem = line[76:78].strip() if len(line) >= 78 else ""
            residues[(chain, rn, ic)][name] = Atom("HETATM", name, resn, chain, rn, ic, xyz, occ, temp, infer_element(name, elem))
        except Exception:
            continue
    return dict(residues)


def keys(residues):
    return sorted(residues.keys(), key=lambda k: (k[0], k[1], k[2]))


def resname(residue):
    return next(iter(residue.values())).res_name


def base_of(resname_):
    r = resname_.upper().strip()
    if r in {"A", "U", "G", "C"}: return r
    if r in {"FA2", "TA"} or r.endswith("A"): return "A"
    if r in {"TG"} or r.endswith("G"): return "G"
    if r in {"TC"} or r.endswith("C"): return "C"
    if r in {"TFT", "TU", "TT"} or r.endswith("T") or r.endswith("U"): return "U"
    if r.startswith("A"): return "A"
    if r.startswith("G"): return "G"
    if r.startswith("C"): return "C"
    if r.startswith(("T","U")): return "U"
    return "N"


def sequence(residues):
    return "".join(base_of(resname(residues[k])) for k in keys(residues))


def target_name(base, policy="preserve"):
    if policy == "dna-like":
        return {"A":"FA2", "U":"TFT", "G":"TG", "C":"TC"}.get(base, "TN")
    return {"A":"FA2", "U":"TU", "G":"TG", "C":"TC"}.get(base, "TN")


def gly_atom(base):
    return "N9" if base in {"A","G"} else "N1"


def source_base_atoms(residue):
    nonbase = {"P","OP1","OP2","O1P","O2P","O5'","C5'","C4'","O4'","C3'","O3'","C2'","O2'","C1'"}
    return {n:a for n,a in residue.items() if n not in nonbase and "'" not in n}


def clone(atom, *, coords=None, atom_name=None, res_name=None, chain=None, res_num=None, insertion_code=None, element=None):
    name = atom_name if atom_name is not None else atom.atom_name
    return Atom("HETATM", name, res_name or atom.res_name, chain or atom.chain,
                res_num if res_num is not None else atom.res_num,
                insertion_code if insertion_code is not None else atom.insertion_code,
                np.array(coords if coords is not None else atom.coords, dtype=float),
                atom.occupancy, atom.temp_factor, element or infer_element(name, atom.element))


def kabsch(mobile, target):
    mobile = np.asarray(mobile, dtype=float); target = np.asarray(target, dtype=float)
    mc = mobile.mean(axis=0); tc = target.mean(axis=0)
    m = mobile - mc; t = target - tc
    u, s, vt = np.linalg.svd(m.T @ t)
    r = vt.T @ u.T
    if np.linalg.det(r) < 0:
        vt[-1,:] *= -1
        r = vt.T @ u.T
    trans = tc - r @ mc
    fitted = (r @ mobile.T).T + trans
    rmsd = float(np.sqrt(np.mean(np.sum((fitted-target)**2, axis=1))))
    return r, trans, rmsd


def apply(coord, r, t):
    return r @ coord + t


def template_distance(res_a, atom_a, res_b, atom_b, default):
    if res_a is not None and res_b is not None and atom_a in res_a and atom_b in res_b:
        return float(np.linalg.norm(res_a[atom_a].coords - res_b[atom_b].coords))
    return default


def build_index(template):
    ks = keys(template)
    idx = defaultdict(list)
    for i,k in enumerate(ks):
        nk = ks[i+1] if i+1 < len(ks) and ks[i+1][0] == k[0] else None
        pk = ks[i-1] if i > 0 and ks[i-1][0] == k[0] else None
        idx[base_of(resname(template[k]))].append((k, template[k], nk, pk))
    return dict(idx)


def select_template(base, idx, counter):
    if base in idx and idx[base]:
        i = counter.get(base, 0); counter[base] = i+1
        return idx[base][i % len(idx[base])], "exact base-class TNA template"
    if base == "U" and "T" in idx and idx["T"]:
        i = counter.get("T", 0); counter["T"] = i+1
        return idx["T"][i % len(idx["T"])], "T-like donor for RNA U"
    for alt in (["G","A"] if base in {"A","G"} else ["C","U","T"]):
        if alt in idx and idx[alt]:
            i = counter.get(alt,0); counter[alt]=i+1
            return idx[alt][i % len(idx[alt])], f"fallback {alt}-like donor"
    first = sorted(idx)[0]
    i = counter.get(first,0); counter[first]=i+1
    return idx[first][i % len(idx[first])], "last-resort fallback"


def initial_transform(tres, next_tres, sres, next_sres):
    mobile=[]; target=[]; used=[]
    if "P" in tres and "P" in sres:
        mobile.append(tres["P"].coords); target.append(sres["P"].coords); used.append("P")
    if next_tres is not None and next_sres is not None and "P" in next_tres and "P" in next_sres:
        mobile.append(next_tres["P"].coords); target.append(next_sres["P"].coords); used.append("NEXT_P")
    for a in ["C1'","C3'","C4'"]:
        if a in tres and a in sres:
            mobile.append(tres[a].coords); target.append(sres[a].coords); used.append(a)
    if len(mobile) < 3:
        mobile=[]; target=[]; used=[]
        for a in ["P","C1'","C3'","C4'"]:
            if a in tres and a in sres:
                mobile.append(tres[a].coords); target.append(sres[a].coords); used.append(a)
    if len(mobile) < 3:
        raise ValueError("Not enough segment anchors")
    return kabsch(np.array(mobile), np.array(target)) + (used,)


def optimize_sugar(initial, sres, next_sres, tres, next_tres):
    atoms = SUGAR_ATOMS
    x0 = np.concatenate([initial[a] for a in atoms])

    # Template-derived internal distances.
    pairs = [
        ("C1'","C2'", template_distance(tres,"C1'",tres,"C2'",1.47), 12.0),
        ("C2'","C3'", template_distance(tres,"C2'",tres,"C3'",1.43), 18.0),
        ("C3'","C4'", template_distance(tres,"C3'",tres,"C4'",1.53), 12.0),
        ("C4'","O4'", template_distance(tres,"C4'",tres,"O4'",1.53), 12.0),
        ("C1'","O4'", template_distance(tres,"C1'",tres,"O4'",1.49), 12.0),
        ("C2'","O2'", template_distance(tres,"C2'",tres,"O2'",1.20), 18.0),
        ("C3'","O3'", template_distance(tres,"C3'",tres,"O3'",1.43), 18.0),
        # Shape-supporting distances.
        ("C1'","C3'", template_distance(tres,"C1'",tres,"C3'",2.45), 1.0),
        ("C2'","C4'", template_distance(tres,"C2'",tres,"C4'",2.45), 1.0),
        ("C2'","O4'", template_distance(tres,"C2'",tres,"O4'",2.40), 1.0),
    ]

    p_current = sres["P"].coords if "P" in sres else initial["P"] if "P" in initial else None
    p_next = next_sres["P"].coords if next_sres is not None and "P" in next_sres else None
    d_p_o3 = template_distance(tres, "P", tres, "O3'", 1.60)
    d_o2_next = template_distance(tres, "O2'", next_tres, "P", 1.58)

    # Keep C1 near original source C1/base attachment region, but weakly.
    c1_source = sres["C1'"].coords if "C1'" in sres else initial["C1'"]

    def unpack(x):
        return {a: x[i*3:(i+1)*3] for i,a in enumerate(atoms)}

    def residuals(x):
        c = unpack(x)
        res = []
        for a,b,d,w in pairs:
            res.append(w * (np.linalg.norm(c[a]-c[b]) - d))
        if p_current is not None:
            res.append(10.0 * (np.linalg.norm(c["O3'"] - p_current) - d_p_o3))
        if p_next is not None:
            res.append(10.0 * (np.linalg.norm(c["O2'"] - p_next) - d_o2_next))
        # Weak positional regularization to avoid wild flips.
        # If there is no next phosphate, this residue is terminal/gap-adjacent
        # for TNA linkage fitting; do not over-constrain it to the RNA sugar frame.
        for a in atoms:
            if p_next is None:
                weight = 0.005 if a not in {"O2'","O3'"} else 0.002
            else:
                weight = 0.08 if a not in {"O2'","O3'"} else 0.03
            res.extend(list(weight * (c[a] - initial[a])))
        if p_next is not None:
            res.extend(list(0.05 * (c["C1'"] - c1_source)))
        return np.array(res, dtype=float)

    fit = least_squares(residuals, x0, max_nfev=300, xtol=1e-8, ftol=1e-8, gtol=1e-8)
    c = unpack(fit.x)
    return c, float(fit.cost)


def adjust_base(out_res, base_names, base, desired=1.46):
    g = gly_atom(base)
    if "C1'" not in out_res or g not in out_res:
        return None
    c1 = out_res["C1'"].coords; n = out_res[g].coords
    v = n - c1; d = float(np.linalg.norm(v))
    if d < 1e-8:
        return None
    shift = (desired - d) * (v/d)
    for name in base_names:
        if name in out_res:
            out_res[name].coords = out_res[name].coords + shift
    return float(np.linalg.norm(out_res[g].coords - c1))


def convert(source, template, policy="preserve"):
    idx = build_index(template)
    skeys = keys(source)
    out = {}; records=[]; counter={}
    for i,skey in enumerate(skeys):
        sres = source[skey]
        next_skey = (
            skeys[i+1]
            if i+1 < len(skeys)
            and skeys[i+1][0] == skey[0]
            and skeys[i+1][1] == skey[1] + 1
            and not skey[2]
            and not skeys[i+1][2]
            else None
        )
        next_sres = source[next_skey] if next_skey is not None else None
        b = base_of(resname(sres))
        (tkey, tres, next_tkey, prev_tkey), note = select_template(b, idx, counter)
        next_tres = template[next_tkey] if next_tkey is not None and next_tkey in template else None
        r, t, rmsd, used = initial_transform(tres, next_tres, sres, next_sres)

        # Initial transformed TNA sugar.
        init = {}
        for a in SUGAR_ATOMS:
            if a in tres:
                init[a] = apply(tres[a].coords, r, t)
        if any(a not in init for a in SUGAR_ATOMS):
            raise ValueError(f"TNA template residue {tkey} lacks required sugar atoms")

        opt, cost = optimize_sugar(init, sres, next_sres, tres, next_tres)

        # Rescue for terminal/gap-adjacent residues:
        # if no next P exists and the optimized sugar still cannot satisfy P(i)->O3'(i),
        # fall back to a rigid template-local sugar translated so template P overlays source P.
        # This sacrifices local RNA-frame preservation at that residue but keeps the TNA linkage sane.
        if next_sres is None and "P" in sres and "P" in tres and "O3'" in opt:
            p_o3_now = float(np.linalg.norm(sres["P"].coords - opt["O3'"]))
            if p_o3_now > 1.90:
                shift = sres["P"].coords - apply(tres["P"].coords, r, t)
                opt = {a: apply(tres[a].coords, r, t) + shift for a in SUGAR_ATOMS}
                cost = cost + 999.0  # mark rescue in report-level optimization cost

        target_res = target_name(b, policy)
        out_res = {}

        # Phosphate from source RNA.
        for raw in ["P","OP1","OP2","O1P","O2P"]:
            if raw in sres:
                name = "OP1" if raw == "O1P" else ("OP2" if raw == "O2P" else raw)
                out_res[name] = clone(sres[raw], atom_name=name, res_name=target_res, chain=skey[0], res_num=skey[1], insertion_code=skey[2], element=infer_element(name))

        for a in SUGAR_ATOMS:
            out_res[a] = clone(tres[a], coords=opt[a], atom_name=a, res_name=target_res, chain=skey[0], res_num=skey[1], insertion_code=skey[2], element=infer_element(a))

        # Base transplant.
        base_atoms = source_base_atoms(sres)
        anchors = [a for a in ["C1'","C2'","C3'","C4'"] if a in sres and a in out_res]
        rb, tb, base_rmsd = kabsch(np.array([sres[a].coords for a in anchors]), np.array([out_res[a].coords for a in anchors]))
        base_names=[]
        for name, atom in base_atoms.items():
            out_res[name] = clone(atom, coords=apply(atom.coords, rb, tb), res_name=target_res, chain=skey[0], res_num=skey[1], insertion_code=skey[2])
            base_names.append(name)

        # Template-derived C1-gly target if available.
        desired_gly = 1.46
        g = gly_atom(b)
        if "C1'" in tres and g in tres:
            desired_gly = float(np.linalg.norm(tres["C1'"].coords - tres[g].coords))
        gly = adjust_base(out_res, base_names, b, desired_gly)

        p_o3 = float(np.linalg.norm(out_res["P"].coords - out_res["O3'"].coords)) if "P" in out_res else None
        o2_next = float(np.linalg.norm(out_res["O2'"].coords - source[next_skey]["P"].coords)) if next_skey is not None and "P" in source[next_skey] else None

        out[skey] = out_res
        records.append(ConversionRecord(skey, b, target_res, tkey, resname(tres), rmsd, base_rmsd, cost, gly, p_o3, o2_next, note + "; linkage-optimized"))
    return out, records


def fmt_atom(serial, atom):
    elem = (atom.element or infer_element(atom.atom_name))[:2].rjust(2)
    icode = (atom.insertion_code or " ")[:1]
    return (f"{atom.record:<6s}{serial:5d} {atom.atom_name[:4]:>4s} {atom.res_name[:3]:>3s} "
            f"{(atom.chain or 'A')[:1]}{atom.res_num:4d}{icode}   "
            f"{atom.coords[0]:8.3f}{atom.coords[1]:8.3f}{atom.coords[2]:8.3f}"
            f"{atom.occupancy:6.2f}{atom.temp_factor:6.2f}{'':>10s}{elem:>2s}")


def atom_order(name):
    return (BACKBONE_ORDER.index(name), name) if name in BACKBONE_ORDER else (100, name)


def write_pdb(residues, path, src_seq, tmpl_seq):
    with path.open("w") as f:
        f.write("REMARK   Digital Polymerase Prototype 006B.4\n")
        f.write("REMARK   RNA to TNA linkage-optimized candidate reconstruction\n")
        f.write(f"REMARK   Source RNA sequence: {src_seq}\n")
        f.write(f"REMARK   TNA template base-class sequence: {tmpl_seq}\n")
        f.write("REMARK   TNA linkage model: P(i)->O3'(i), O2'(i)->P(i+1)\n")
        f.write("REMARK   WARNING: Computational candidate only; not physically validated\n")
        f.write("CRYST1    1.000    1.000    1.000  90.00  90.00  90.00 P 1           1\n")
        serial=1
        for k in keys(residues):
            for name in sorted(residues[k], key=atom_order):
                f.write(fmt_atom(serial, residues[k][name]) + "\n")
                serial += 1
        f.write("END\n")


def validate_intra(residues, a, b, lo, hi, label):
    vals=[]; missing=0
    for k in keys(residues):
        if a not in residues[k] or b not in residues[k]:
            missing += 1; continue
        vals.append(float(np.linalg.norm(residues[k][a].coords - residues[k][b].coords)))
    failed=sum(1 for v in vals if not(lo <= v <= hi))
    return DistanceSummary(label, len(vals), missing, failed, float(np.mean(vals)) if vals else float("nan"), float(np.min(vals)) if vals else float("nan"), float(np.max(vals)) if vals else float("nan"), lo, hi)


def validate_inter(residues, a, b, lo, hi, label):
    ks=keys(residues); vals=[]; missing=0
    for lk,rk in zip(ks[:-1], ks[1:]):
        if lk[0] != rk[0] or rk[1] != lk[1]+1 or lk[2] or rk[2]:
            continue
        if a not in residues[lk] or b not in residues[rk]:
            missing += 1; continue
        vals.append(float(np.linalg.norm(residues[lk][a].coords - residues[rk][b].coords)))
    failed=sum(1 for v in vals if not(lo <= v <= hi))
    return DistanceSummary(label, len(vals), missing, failed, float(np.mean(vals)) if vals else float("nan"), float(np.min(vals)) if vals else float("nan"), float(np.max(vals)) if vals else float("nan"), lo, hi)


def validate_gly(residues):
    vals=[]; missing=0
    for k in keys(residues):
        b=base_of(resname(residues[k])); g=gly_atom(b)
        if "C1'" not in residues[k] or g not in residues[k]:
            missing += 1; continue
        vals.append(float(np.linalg.norm(residues[k]["C1'"].coords - residues[k][g].coords)))
    failed=sum(1 for v in vals if not(1.30 <= v <= 1.75))
    return DistanceSummary("C1'→glycosidic N", len(vals), missing, failed, float(np.mean(vals)) if vals else float("nan"), float(np.min(vals)) if vals else float("nan"), float(np.max(vals)) if vals else float("nan"), 1.30, 1.75)


def status(s):
    return "NO_DATA" if s.measured == 0 else ("PASS" if s.failed == 0 else "FAIL")


def build_validation(output):
    checks = {
        "TNA O2'(i)→P(i+1)": validate_inter(output, "O2'", "P", 1.25, 1.90, "TNA O2'(i)→P(i+1)"),
        "TNA P(i)→O3'(i)": validate_intra(output, "P", "O3'", 1.35, 1.90, "TNA P(i)→O3'(i)"),
        "C1'→glycosidic N": validate_gly(output),
        "C1'→C2'": validate_intra(output, "C1'", "C2'", 1.25, 1.90, "C1'→C2'"),
        "C2'→C3'": validate_intra(output, "C2'", "C3'", 1.20, 1.90, "C2'→C3'"),
        "C3'→C4'": validate_intra(output, "C3'", "C4'", 1.25, 2.00, "C3'→C4'"),
        "C2'→O2'": validate_intra(output, "C2'", "O2'", 1.05, 1.65, "C2'→O2'"),
        "C3'→O3'": validate_intra(output, "C3'", "O3'", 1.10, 1.75, "C3'→O3'"),
        "C1'→O4'": validate_intra(output, "C1'", "O4'", 1.20, 1.85, "C1'→O4'"),
        "C4'→O4'": validate_intra(output, "C4'", "O4'", 1.20, 1.95, "C4'→O4'"),
    }
    return checks


def table(checks):
    lines=["| Metric | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |",
           "|---|---:|---:|---:|---:|---:|---:|---|---|"]
    for label,s in checks.items():
        lines.append(f"| {label} | {s.measured} | {s.missing} | {s.failed} | {s.mean:.3f} | {s.minimum:.3f} | {s.maximum:.3f} | {s.lo:.2f}–{s.hi:.2f} | {status(s)} |")
    return "\n".join(lines)


def write_report(path, source_path, template_path, output_path, source, template, output, records):
    checks = build_validation(output)
    rmsd=[r.align_rmsd for r in records]; br=[r.base_rmsd for r in records]
    costs=[r.opt_cost for r in records]; gly=[r.gly for r in records if r.gly is not None]
    po3=[r.p_o3 for r in records if r.p_o3 is not None]; o2p=[r.o2_next_p for r in records if r.o2_next_p is not None]
    rec_lines=[]
    for i,r in enumerate(records,1):
        rec_lines.append(f"| {i} | {r.source_key[0]}{r.source_key[1]}{r.source_key[2]} | {r.source_base} | {r.target_res_name} | {r.template_res_name} {r.template_key[0]}{r.template_key[1]}{r.template_key[2]} | {r.align_rmsd:.4f} | {r.base_rmsd:.4f} | {r.opt_cost:.4f} | {r.gly if r.gly is not None else 'NA'} | {r.p_o3 if r.p_o3 is not None else 'NA'} | {r.o2_next_p if r.o2_next_p is not None else 'NA'} | {r.note} |")
    md=f"""# RNA → TNA Conversion Report

**Project:** Digital Polymerase  
**Prototype:** 006B  
**Method:** Linkage-optimized TNA reconstruction  
**Status:** Experimental candidate, not physically validated  
**TNA chain-continuity status:** `O2′(i)→P(i+1) {status(checks["TNA O2'(i)→P(i+1)"])}`, `P(i)→O3′(i) {status(checks["TNA P(i)→O3'(i)"])}`  
**Base-attachment status:** `{status(checks["C1'→glycosidic N"])}`  
**Local TNA sugar status:** `C2′→O2′ {status(checks["C2'→O2'"])}`, `C3′→O3′ {status(checks["C3'→O3'"])}`

---

## Inputs

- Source RNA PDB: `{source_path}`
- TNA template PDB: `{template_path}`
- Output PDB: `{output_path}`

---

## Source and Template

- Source RNA sequence: `{sequence(source)}`
- TNA template base-class sequence: `{sequence(template)}`
- Source residue count: `{len(keys(source))}`
- Template residue count: `{len(keys(template))}`
- Converted residues: `{len(records)}`

---

## Why TNA Needed Prototype 006B.4

Prototype 006A showed the correct conceptual issue: TNA does not use RNA-like O3′→P chain logic.  
Prototype 006A.1 added direct O2′/O3′ linkage correction, but some residues still could not satisfy both sugar and phosphate distances while keeping the initial sugar fixed.

Prototype 006B.4 therefore locally optimizes each TNA-like sugar scaffold so that:

```text
P(i)    → O3′(i)
O2′(i) → P(i+1)
C2′    → O2′
C3′    → O3′
internal threose-like sugar distances
```

are improved simultaneously.

---

## Alignment / Optimization Summary

- Mean initial segment RMSD: `{np.mean(rmsd):.4f} Å`
- Maximum initial segment RMSD: `{np.max(rmsd):.4f} Å`
- Mean base-transplant RMSD: `{np.mean(br):.4f} Å`
- Maximum base-transplant RMSD: `{np.max(br):.4f} Å`
- Mean optimization cost: `{np.mean(costs):.4f}`
- Mean C1′→glycosidic N distance: `{np.mean(gly) if gly else float('nan'):.4f} Å`
- Mean P(i)→O3′(i) distance: `{np.mean(po3) if po3 else float('nan'):.4f} Å`
- Mean O2′(i)→P(i+1) distance: `{np.mean(o2p) if o2p else float('nan'):.4f} Å`

---

## Structural Validation

{table(checks)}

---

## Per-Residue Conversion

| # | Source residue | Base | Output residue | Template used | Initial RMSD (Å) | Base RMSD (Å) | Opt. cost | C1′–N (Å) | P–O3′ (Å) | O2′–next P (Å) | Note |
|---:|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
{chr(10).join(rec_lines)}

---

## Scientific Interpretation

This output should be interpreted as:

> a TNA-like computational candidate generated by linkage-optimized reconstruction.

It should **not** be interpreted as:

> a chemically validated, experimentally confirmed, or MD-ready TNA structure.

---

## Important Limitations

- Not energy-minimized.
- No force-field parameters are generated.
- No topology files are generated.
- No explicit `CONECT` records are written.
- TNA stereochemistry requires expert inspection.
- The output lacks RNA-like O5′/C5′ sugar-extension atoms because TNA is shorter.
- Molecular viewers may not render standard nucleic-acid cartoon paths reliably for TNA-like structures.
- Biological function, stability, replication, or catalytic activity is not implied.
"""
    path.write_text(md)


def run(source_path, template_path, output_path, report_path):
    source=parse_pdb(source_path, normalize=False)
    template=parse_pdb(template_path, normalize=True)
    output, records=convert(source, template)
    write_pdb(output, output_path, sequence(source), sequence(template))
    write_report(report_path, source_path, template_path, output_path, source, template, output, records)
    checks=build_validation(output)
    print("="*80)
    print("Digital Polymerase Prototype 006B.4")
    print("RNA → TNA linkage-optimized candidate reconstruction")
    print("="*80)
    print(f"Source RNA: {source_path}")
    print(f"TNA template: {template_path}")
    print(f"Output PDB: {output_path}")
    print(f"Report: {report_path}")
    print(f"Source sequence: {sequence(source)}")
    print(f"Template sequence: {sequence(template)}")
    print(f"Converted residues: {len(records)}")
    print("-"*80)
    for label in ["TNA O2'(i)→P(i+1)", "TNA P(i)→O3'(i)", "C1'→glycosidic N", "C2'→O2'", "C3'→O3'"]:
        s=checks[label]
        print(f"{label}: {status(s)} (measured={s.measured}, failed={s.failed}, mean={s.mean:.3f} Å)")
    print("="*80)


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--rna", required=True, type=Path)
    p.add_argument("--template", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--report", required=True, type=Path)
    args=p.parse_args()
    run(args.rna, args.template, args.output, args.report)

if __name__ == "__main__":
    main()
