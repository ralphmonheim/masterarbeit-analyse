"""Kanonische Parameter- und Optionskataloge fuer Fachmodule.

Der Namespace enthaelt die fachlich neutralen Python-Modelle und Importhelfer.
Historische ``ma_variants``-Importpfade werden ausserhalb dieses Pakets als
einseitige Kompatibilitaetsadapter weitergefuehrt.
"""

from .importing import import_catalog
from .models import OptionSet, OptionValue, Parameter
from .options import import_options
from .parameters import import_parameters
from .reports import CatalogImportResult, ImportValidationError

__all__ = [
    "CatalogImportResult",
    "ImportValidationError",
    "OptionSet",
    "OptionValue",
    "Parameter",
    "import_catalog",
    "import_options",
    "import_parameters",
]
