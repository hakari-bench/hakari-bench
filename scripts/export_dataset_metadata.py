from __future__ import annotations

import argparse
import json
from pathlib import Path

from nano_ir_benchmark.metadata import export_bibtex, export_citation_catalog, export_latex_citations


def main() -> None:
    parser = argparse.ArgumentParser(description="Export dataset citation metadata.")
    parser.add_argument("--config-root", type=Path, default=Path("config"))
    parser.add_argument("--format", choices=["json", "bibtex", "latex"], default="json")
    args = parser.parse_args()

    if args.format == "json":
        print(json.dumps(export_citation_catalog(config_root=args.config_root), ensure_ascii=False, indent=2))
    elif args.format == "bibtex":
        print(export_bibtex(config_root=args.config_root), end="")
    else:
        print(export_latex_citations(config_root=args.config_root), end="")


if __name__ == "__main__":
    main()
