#!/usr/bin/env python3
from __future__ import annotations

import argparse
import io
import json
import re
import sys
import urllib.request
import zipfile
from pathlib import Path

UA = "Arcade-Catalog-MiSTer-Builder/0.3.1"

def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()

def safe_id(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", s)

def normalize_member(name: str) -> list[str]:
    return [x for x in name.replace("\\", "/").split("/") if x]

def is_main_arcade_mra(parts: list[str]) -> bool:
    """
    Aceita somente MRAs diretamente sob uma pasta chamada _Arcade:
      Repo-root/_Arcade/Game.mra
    Rejeita:
      _Arcade/_alternatives/...
      _Arcade/cores/...
      qualquer outra subpasta.
    """
    if not parts or not parts[-1].lower().endswith(".mra"):
        return False
    try:
        i = next(i for i, p in enumerate(parts) if p.lower() == "_arcade")
    except StopIteration:
        return False
    return len(parts) == i + 2

def logical_path(parts: list[str]) -> str:
    i = next(i for i, p in enumerate(parts) if p.lower() == "_arcade")
    return "/".join(parts[i:])

def collect_archive(src: dict, out: Path):
    sid = src["id"]
    url = src["archive_url"]
    required = bool(src.get("required", False))

    print(f"[repo] {sid}", file=sys.stderr)
    try:
        raw = fetch(url)
        z = zipfile.ZipFile(io.BytesIO(raw))
    except Exception as e:
        if required:
            raise SystemExit(f"ERRO: fonte obrigatoria {sid}: {e}")
        print(f"[aviso] {sid}: {e}", file=sys.stderr)
        return [], 0

    rows = []
    target_dir = out / safe_id(sid)
    target_dir.mkdir(parents=True, exist_ok=True)

    try:
        for info in z.infolist():
            if info.is_dir():
                continue
            parts = normalize_member(info.filename)
            if not is_main_arcade_mra(parts):
                continue

            lpath = logical_path(parts)
            filename = parts[-1]
            data = z.read(info)

            # Mantém arquivos de fontes diferentes separados e evita colisões.
            local_name = safe_id(lpath.replace("/", "__"))
            if not local_name.lower().endswith(".mra"):
                local_name += ".mra"
            target = target_dir / local_name
            target.write_bytes(data)

            rows.append((sid, lpath, filename, str(target.relative_to(out))))
    finally:
        z.close()

    print(f"[ok] {sid}: {len(rows)} MRAs", file=sys.stderr)
    return rows, len(rows)

def main():
    ap = argparse.ArgumentParser(
        description="Coleta MRAs principais diretamente dos repositorios publicos MiSTer."
    )
    ap.add_argument("--sources", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    cfg = json.loads(args.sources.read_text(encoding="utf-8"))
    args.out.mkdir(parents=True, exist_ok=True)

    manifest = []
    per_source = []

    for src in cfg["sources"]:
        if not src.get("enabled", True):
            continue
        rows, count = collect_archive(src, args.out)
        manifest.extend(rows)
        per_source.append((src["id"], count, bool(src.get("required", False))))

        min_source = int(src.get("minimum_mras", 0))
        if count < min_source:
            raise SystemExit(
                f"ERRO: {src['id']} retornou {count} MRAs; minimo esperado={min_source}."
            )

    minimum_total = int(cfg.get("minimum_total_mras", 1))
    if len(manifest) < minimum_total:
        raise SystemExit(
            f"ERRO: coleta retornou apenas {len(manifest)} MRAs; "
            f"minimo de seguranca={minimum_total}. Nenhuma base deve ser publicada."
        )

    with (args.out / "_manifest.tsv").open("w", encoding="utf-8", newline="") as f:
        f.write("source\tpath\tfilename\tlocal\n")
        for row in manifest:
            f.write("\t".join(row) + "\n")

    with (args.out / "_sources_report.tsv").open("w", encoding="utf-8", newline="") as f:
        f.write("source\tmras\trequired\n")
        for sid, count, required in per_source:
            f.write(f"{sid}\t{count}\t{1 if required else 0}\n")

    print(f"Coletados: {len(manifest)} MRAs")
    for sid, count, _ in per_source:
        print(f"  {sid}: {count}")

if __name__ == "__main__":
    main()
