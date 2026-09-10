"""Erstellt den digitalen Anhang fuer Kapitel 5 aus lokalen Originalartefakten.

Der Lauf veraendert weder Quell- noch Messdateien. Er kopiert nur die zwei
eindeutigen Benchmark-JSONs und vorhandene, fachlich passende Grafikoutputs.
UI-Assets sind bewusst keine UI-Screenshots und werden daher nicht kopiert.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "digitaler_anhang" / "kapitel_5"
BENCHMARK_SOURCES = (
    ROOT / "docs/project/research_measurements/chapter_5_4/BENCH-CH5-4-V0425.json",
    ROOT / "docs/project/research_measurements/chapter_5_4/BENCH-CH5-4-PLOTS-V0425.json",
)
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
OUTPUT_ROOTS = (ROOT / "docs/examples", ROOT / "data/ma_weather/output", ROOT / "data/test_output")
EXCLUDED_IMAGE_PARTS = {"axis_gap_mockup"}


def git_value(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def humanize(stem: str) -> str:
    return stem.replace("_", " ").replace("-", " ").strip().title()


def output_module(path: Path) -> str:
    lowered = str(path).lower()
    return "ma_weather" if "weather" in lowered or "try_" in lowered else "ma_analyse"


def find_output_images() -> list[Path]:
    images: list[Path] = []
    for base in OUTPUT_ROOTS:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in IMAGE_SUFFIXES:
                continue
            relative_parts = set(path.relative_to(ROOT).parts)
            if relative_parts & EXCLUDED_IMAGE_PARTS:
                continue
            images.append(path)
    return sorted(images, key=lambda item: item.as_posix().lower())


def unique_images(images: list[Path]) -> list[tuple[Path, list[Path]]]:
    by_hash: dict[str, list[Path]] = defaultdict(list)
    for image in images:
        by_hash[sha256(image)].append(image)
    return sorted(
        ((paths[0], paths) for paths in by_hash.values()),
        key=lambda item: item[0].as_posix().lower(),
    )


def markdown_table(rows: list[list[str]], headings: list[str]) -> str:
    escaped = [[cell.replace("|", "\\|").replace("\n", "<br>") for cell in row] for row in rows]
    return "\n".join(
        ["| " + " | ".join(headings) + " |", "| " + " | ".join(["---"] * len(headings)) + " |"]
        + ["| " + " | ".join(row) + " |" for row in escaped]
    )


def write_benchmark_readme(records: list[dict[str, str]]) -> None:
    rows = []
    for record in records:
        payload = json.loads(record["source"].read_text(encoding="utf-8"))
        if "PLOTS" in record["source"].name:
            purpose = "Jahresdiagramm und Variantenvergleich (reproduzierbare Testdaten)."
            metrics = "Cold- und Warm-Start, Laufzeiten, statistische Kennwerte, 1.200 Punkte je Zeitreihe."
        else:
            purpose = "SmallOffice-V1-PreProcess einschließlich Variantenerzeugung und Setup-Materialisierung."
            metrics = "Gesamtlaufzeit, Teilzeiten je Workflow-Schritt, Cold Start und statistische Kennwerte."
        rows.append([
            record["source"].name,
            record["source"].relative_to(ROOT).as_posix(),
            purpose,
            payload.get("software_version", "v0.42.5"),
            payload.get("measurement_boundary", "Im JSON dokumentiert."),
            metrics,
            "5.4",
        ])
    text = "# Benchmarks zu Kapitel 5.4\n\n"
    text += "Die JSON-Dateien sind unveränderte Originalkopien. Es wurden keine Messwerte rekonstruiert.\n\n"
    text += markdown_table(rows, ["Originaldateiname", "Ursprünglicher Pfad", "Benchmarkzweck", "Softwarestand", "Messgrenze", "Enthaltene Messgrößen", "Zuordnung"]) + "\n"
    (TARGET / "01_Benchmarks" / "README_Benchmarks.md").write_text(text, encoding="utf-8")


def main() -> None:
    if TARGET.exists():
        raise SystemExit(f"Zielordner existiert bereits: {TARGET}")
    for source in BENCHMARK_SOURCES:
        if not source.is_file():
            raise SystemExit(f"Erforderlicher Benchmark fehlt: {source.relative_to(ROOT)}")

    head = git_value("rev-parse", "HEAD")
    tags = git_value("tag", "--points-at", "HEAD").splitlines()
    version_note = "Keine committed Änderungen seit v0.42.5; HEAD trägt den Tag v0.42.5." if "v0.42.5" in tags else "HEAD weicht vom Benchmark-Tag v0.42.5 ab."
    modules = sorted(
        path.name for path in (ROOT / "src").iterdir()
        if path.is_dir() and path.name.startswith("ma_") and not path.name.endswith(".egg-info")
    )

    (TARGET / "01_Benchmarks").mkdir(parents=True)
    (TARGET / "02_UI").mkdir()
    (TARGET / "03_Output_Bilder").mkdir()
    for module in modules:
        (TARGET / "02_UI" / module).mkdir()

    benchmark_records: list[dict[str, str]] = []
    for source in BENCHMARK_SOURCES:
        destination = TARGET / "01_Benchmarks" / source.name
        shutil.copy2(source, destination)
        benchmark_records.append({"source": source, "destination": destination})
    write_benchmark_readme(benchmark_records)

    records: list[list[str]] = []
    module_indices: dict[str, int] = defaultdict(int)
    for image, origins in unique_images(find_output_images()):
        module = output_module(image)
        module_indices[module] += 1
        index = module_indices[module]
        destination_dir = TARGET / "03_Output_Bilder" / module
        destination_dir.mkdir(exist_ok=True)
        destination_name = f"OUT_{module}_{index:03d}_{image.stem}.png"
        destination = destination_dir / destination_name
        shutil.copy2(image, destination)
        origin_paths = "<br>".join(path.relative_to(ROOT).as_posix() for path in origins)
        records.append([
            f"DA-5-OUT-{module.removeprefix('ma_').upper()}-{index:03d}", "Output", module,
            destination.relative_to(TARGET).as_posix(), image.name, origin_paths,
            f"Vorhandene Projektdokumentation/Testausgabe: {humanize(image.stem)}.",
            "vorhandenes Original", "5.3 / 5.4",
        ])

    for index, benchmark in enumerate(benchmark_records, start=1):
        records.insert(index - 1, [
            f"DA-5-BEN-{index:02d}", "Benchmark", "ma_workflow" if index == 1 else "ma_analyse",
            benchmark["destination"].relative_to(TARGET).as_posix(), benchmark["source"].name,
            benchmark["source"].relative_to(ROOT).as_posix(), "Unveränderte Benchmark-Rohmessung.",
            "vorhandenes Original", "5.4",
        ])

    readme = "# Digitaler Anhang zu Kapitel 5 – Prozessoptimierung\n\n"
    readme += "## Zweck\n\nDieser digitale Anhang dokumentiert Benchmarkdaten, vorhandene grafische Benutzeroberflächen und die durch den Softwareprototyp erzeugten Grafikausgaben. Er bezieht sich auf die Abschnitte 5.3 und 5.4. Der Softwarequellcode wird nicht dupliziert, sondern versioniert über das GitHub-Repository bereitgestellt.\n\n"
    readme += "## Softwarestand\n\n"
    readme += f"- Benchmarkstand: Git-Tag `v0.42.5`\n- Aktueller Commit/HEAD: `{head}`\n- Funktionsstand seit `v0.42.5`: {version_note}\n\n"
    readme += "## Ordner\n\n- `01_Benchmarks`: unveränderte Rohmessungen und ihre Einordnung für Abschnitt 5.4.\n- `02_UI`: Unterordner aller implementierten Module. Es wurden keine Screenshot-Dateien gefunden; vorhandene UI-Assets sind keine Bildschirmaufnahmen und werden nicht als solche ausgegeben. Es besteht keine Playwright-/Selenium- oder vergleichbare automatisierte Screenshot-Mechanik.\n- `03_Output_Bilder`: vorhandene Grafikausgaben aus `ma_weather` und `ma_analyse`, einschließlich dokumentierter Beispiel- und Testausgaben. Technisch identische Dateien wurden nur einmal kopiert; alle Ursprünge stehen in der Tabelle.\n\n"
    readme += "## Vollständige Inhaltsübersicht\n\n"
    readme += markdown_table(records, ["Kennung", "Bereich", "Modul", "Dateiname", "ursprünglicher Dateiname", "ursprünglicher Projektpfad", "Kurzbeschreibung", "Herkunft", "Bezug zur Masterarbeit"]) + "\n"
    (TARGET / "README_Kapitel_5.md").write_text(readme, encoding="utf-8")

    print(f"Anhang erstellt: {TARGET}")
    print(f"Benchmarks: {len(benchmark_records)}")
    print(f"UI-Bilder: 0; UI-Module: {len(modules)}")
    print(f"Output-Bilder (nach Byte-Deduplizierung): {len(records) - len(benchmark_records)}")


if __name__ == "__main__":
    main()
