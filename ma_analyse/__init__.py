"""Launcher-Shim fuer das src-Layout im lokalen Projektcheckout."""

from pathlib import Path

_SRC_PACKAGE = Path(__file__).resolve().parent.parent / "src" / "ma_analyse"
if _SRC_PACKAGE.exists():
    __path__ = [str(_SRC_PACKAGE)]

try:
    from . import __version__  # type: ignore[attr-defined]
except ImportError:
    __version__ = "0.1.0"
