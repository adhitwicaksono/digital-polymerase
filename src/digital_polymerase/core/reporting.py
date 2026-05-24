"""Markdown and JSON reporting helpers."""
from __future__ import annotations
from pathlib import Path
from typing import Mapping, Any
import json
from .validation import DistanceSummary, ClashSummary

def result_status(v):
    if isinstance(v, DistanceSummary): return v.status
    if isinstance(v, dict): return str(v.get('status', 'UNKNOWN'))
    return 'UNKNOWN'

def validation_table(results: Mapping[str, Any]) -> str:
    lines=["| Check | Measured/Residues | Missing | Failed | Mean | Min | Max | Expected | Status |", "|---|---:|---:|---:|---:|---:|---:|---|---|"]
    for label, v in results.items():
        if isinstance(v, DistanceSummary):
            lines.append(f"| {label} | {v.measured} | {v.missing} | {v.failed} | {v.mean:.3f} | {v.minimum:.3f} | {v.maximum:.3f} | {v.lo:.2f}–{v.hi:.2f} | {v.status} |")
        elif isinstance(v, dict):
            measured=v.get('residues', v.get('expected','NA')); missing=v.get('missing','NA')
            lines.append(f"| {label} | {measured} | {missing} | NA | NA | NA | NA | count audit | {v.get('status','UNKNOWN')} |")
    return "\n".join(lines)

def validation_to_jsonable(results):
    out={}
    for label, v in results.items():
        if isinstance(v, DistanceSummary): out[label] = v.__dict__ | {"status": v.status}
        elif isinstance(v, ClashSummary): out[label] = v.__dict__
        elif isinstance(v, dict): out[label] = v
        else: out[label] = str(v)
    return out

def write_json_metrics(results, path):
    path=Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(validation_to_jsonable(results), indent=2), encoding='utf-8')

def write_basic_report(*, path, title, target, method, input_file, output_file, sequence, validation_results, template_file=None, notes=None):
    notes = notes or []
    template_line = f"- Template file: `{template_file}`\n" if template_file else ""
    notes_md = "\n".join(f"- {n}" for n in notes) if notes else "- No additional notes."
    md = f"""# {title}\n\n**Project:** Digital Polymerase  \n**Target:** {target}  \n**Method:** {method}  \n**Status:** Computational candidate; not physically validated\n\n---\n\n## Inputs\n\n- Input file: `{input_file}`\n{template_line}- Output file: `{output_file}`\n\n---\n\n## Sequence\n\n```text\n{sequence}\n```\n\nLength: `{len(sequence)}`\n\n---\n\n## Validation\n\n{validation_table(validation_results)}\n\n---\n\n## Notes\n\n{notes_md}\n"""
    path=Path(path); path.parent.mkdir(parents=True, exist_ok=True); path.write_text(md, encoding='utf-8')
