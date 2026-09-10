"""Erstellt Browseraufnahmen der lokal laufenden Streamlit-Navigation.

Dieses Hilfsskript verwendet ausschließlich den vorhandenen Microsoft Edge und
die bereits installierte Bibliothek ``websockets``. Es installiert nichts und
führt keine Fachaktionen aus; es betätigt nur die Navigation „Weiter“.
"""

from __future__ import annotations

import asyncio
import base64
import json
import subprocess
import time
import urllib.request
from pathlib import Path

import websockets


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / ".tmp" / "ui_screenshot_run" / "captured"
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
DEBUG_PORT = 9223
APP_URL = "http://127.0.0.1:8510"


def debugger_url() -> str:
    with urllib.request.urlopen(f"http://127.0.0.1:{DEBUG_PORT}/json", timeout=2) as response:
        targets = json.load(response)
    return next(target["webSocketDebuggerUrl"] for target in targets if target["type"] == "page")


async def capture() -> list[dict[str, str]]:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    command_id = 0
    async with websockets.connect(debugger_url(), max_size=20_000_000) as socket:
        async def command(method: str, params: dict | None = None) -> dict:
            nonlocal command_id
            command_id += 1
            await socket.send(json.dumps({"id": command_id, "method": method, "params": params or {}}))
            while True:
                response = json.loads(await socket.recv())
                if response.get("id") == command_id:
                    return response["result"]

        await command("Page.enable")
        await command("Runtime.enable")
        await command("Page.navigate", {"url": APP_URL})
        await asyncio.sleep(8)
        snapshots: list[dict[str, str]] = []
        for number in range(1, 32):
            body = await command("Runtime.evaluate", {
                "expression": "document.body.innerText",
                "returnByValue": True,
            })
            text = body["result"].get("value", "")
            if "Aktueller Bereich:" not in text:
                raise RuntimeError("Die Streamlit-Oberfläche wurde nicht vollständig gerendert.")
            area = text.split("Aktueller Bereich:", 1)[1].split("|", 1)[0].strip()
            image = await command("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True})
            image_path = OUTPUT / f"{number:02d}_{area.replace('/', '_')}.png"
            image_path.write_bytes(base64.b64decode(image["data"]))
            buttons = await command("Runtime.evaluate", {
                "expression": "Array.from(document.querySelectorAll('button')).map(item => item.innerText.trim()).filter(Boolean)",
                "returnByValue": True,
            })
            snapshots.append({"area": area, "file": str(image_path), "buttons": buttons["result"].get("value", [])})
            if number == 31:
                break
            await command("Page.navigate", {"url": f"{APP_URL}/?capture={number}"})
            await asyncio.sleep(8)
            opened = await command("Runtime.evaluate", {
                "expression": f"(() => {{ const buttons = Array.from(document.querySelectorAll('button')).filter(item => item.innerText.trim() === 'Oeffnen'); if (!buttons[{number - 1}]) return false; buttons[{number - 1}].click(); return true; }})()",
                "returnByValue": True,
            })
            if not opened["result"].get("value"):
                break
            await asyncio.sleep(3)
    return snapshots


def main() -> None:
    if not EDGE.is_file():
        raise SystemExit("Microsoft Edge wurde nicht gefunden.")
    process = subprocess.Popen([
        str(EDGE), "--headless=new", "--disable-gpu", "--no-first-run",
        f"--remote-debugging-port={DEBUG_PORT}",
        f"--user-data-dir={ROOT / '.tmp' / 'ui_screenshot_run' / 'edge_profile'}", "about:blank",
    ])
    try:
        for _ in range(20):
            try:
                debugger_url()
                break
            except Exception:
                time.sleep(0.5)
        else:
            raise RuntimeError("Der lokale Edge-Debugger wurde nicht verfügbar.")
        print(json.dumps(asyncio.run(capture()), ensure_ascii=False, indent=2))
    finally:
        process.terminate()
        process.wait(timeout=10)


if __name__ == "__main__":
    main()
