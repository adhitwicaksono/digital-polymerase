"""Stable/semi-stable converter layer for Digital Polymerase.

The converter layer is intentionally conservative.

Current status:
    The project is only beginning to promote prototype logic into stable
    converter wrappers. Most reconstruction scripts should remain in
    ``digital_polymerase.prototypes`` until they pass regression tests and
    standardized reporting.

Recommended first stable candidate:
    RNA → FANA, because it is chain-preserving, benchmarked from 8 nt to
    111 nt, and has a clear target-specific local geometry marker
    (C2′→F2′).

Future imports may look like:

    from digital_polymerase.converters.rna_to_fana import convert_rna_to_fana

For now, this package exposes shared converter dataclasses only.
"""

from .base import (
    ConversionResult,
    ConverterConfig,
    ConverterPaths,
    ConverterStatus,
    ensure_output_dirs,
    summarize_result,
)

__all__ = [
    "ConversionResult",
    "ConverterConfig",
    "ConverterPaths",
    "ConverterStatus",
    "ensure_output_dirs",
    "summarize_result",
]
