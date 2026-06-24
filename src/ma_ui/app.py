"""Stabiler Einstieg fuer die zentrale Streamlit-Oberflaeche."""

from ma_ui.streamlit_app.app import (
    _PAGE_RENDERERS,
    _render_page,
    get_renderable_page_keys,
    has_module_view,
    is_module_info_active,
    main,
    module_info_view,
)

__all__ = [
    "_PAGE_RENDERERS",
    "_render_page",
    "get_renderable_page_keys",
    "has_module_view",
    "is_module_info_active",
    "main",
    "module_info_view",
]


if __name__ == "__main__":
    main()
