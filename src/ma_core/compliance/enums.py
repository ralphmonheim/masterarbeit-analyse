"""Gemeinsame Wertemengen fuer die technische Compliance-Pruefung."""

from enum import StrEnum


class ComplianceLevel(StrEnum):
    """Ergebnisstufe einer Compliance-Entscheidung."""

    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"
    UNKNOWN = "unknown"


class SourceType(StrEnum):
    """Fachlich relevante Quellenarten des Projekts."""

    USER_OWNED = "user_owned"
    IDA_RESULT = "ida_result"
    IDA_IDM = "ida_idm"
    EQUA_LIBRARY = "equa_library"
    EQUA_PARAMETER = "equa_parameter"
    DIN_METADATA = "din_metadata"
    DIN_PARAPHRASE = "din_paraphrase"
    DIN_SHORT_QUOTE = "din_short_quote"
    DIN_CONTENT = "din_content"
    NAUTOS_CONTENT = "nautos_content"
    DWD_OPEN_DATA = "dwd_open_data"
    DWD_REGISTERED_DATA = "dwd_registered_data"
    DWD_THIRD_PARTY = "dwd_third_party"
    UNKNOWN = "unknown"


class ComplianceOperation(StrEnum):
    """Operationen, deren Zulaessigkeit getrennt bewertet wird."""

    READ = "read"
    PARSE = "parse"
    ANALYZE = "analyze"
    COMPARE = "compare"
    CONVERT = "convert"
    STORE = "store"
    PUBLISH = "publish"
    REDISTRIBUTE = "redistribute"
    UPLOAD_EXTERNAL = "upload_external"
    INDEX = "index"
    OCR = "ocr"
    RAG = "rag"
    EXTRACT = "extract"
    REVERSE_ENGINEER = "reverse_engineer"
    BINARY_ANALYSIS = "binary_analysis"
    EXECUTE_SIMULATION = "execute_simulation"
    BATCH_SIMULATION = "batch_simulation"


class ProcessingEnvironment(StrEnum):
    """Ort beziehungsweise Art der geplanten Verarbeitung."""

    LOCAL = "local"
    REPOSITORY = "repository"
    EXTERNAL_AI = "external_ai"
    CLOUD = "cloud"
    IDA_ICE = "ida_ice"
