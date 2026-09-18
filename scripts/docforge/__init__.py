"""docforge — one document lane for the whole federation.

Six independent axes, each swappable, so a new document type is a new
combination rather than a new script:

    SOURCE   .md | .html | .typ | .py(builder)
    TEMPLATE structure        templates/registry.json
    THEME    light | dark | print | accessible
    ENGINE   weasyprint | chromium | typst | reportlab
    GATES    print-light | screen-dark | accessible   (verification chain)
    SEAL     content hash + artifact hash + chain ledger

Order is the control: compose -> render -> GATE -> seal. Sealing is unreachable
when a gate fails, so a broken artifact cannot enter the permanent record.

    python3 -m docforge engines --selftest
    python3 -m docforge gates out.pdf --profile print-light
    python3 -m docforge build spec.json
    python3 -m docforge verify docforge-ledger.jsonl
"""
__version__ = "0.1.0"

__all__ = ["__version__"]
