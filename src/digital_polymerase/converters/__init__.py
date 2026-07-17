"""Stable/semi-stable converter layer for Digital Polymerase.

The converter layer is intentionally conservative.

Current stable candidate:
    RNA → FANA, promoted from Prototype 003A after chain-preserving benchmarks
    from 8 nt to 111 nt.

Public import:

    from digital_polymerase.converters.rna_to_fana import convert_rna_to_fana

"""

from .base import (
    ConversionResult,
    ConverterConfig,
    ConverterPaths,
    ConverterStatus,
    ensure_output_dirs,
    summarize_result,
)
from .rna_to_fana import FANAResidueRecord, convert_rna_to_fana

__all__ = [
    "ConversionResult",
    "ConverterConfig",
    "ConverterPaths",
    "ConverterStatus",
    "ensure_output_dirs",
    "summarize_result",
    "FANAResidueRecord",
    "convert_rna_to_fana",
]
