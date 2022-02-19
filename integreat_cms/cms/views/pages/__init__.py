"""
This package contains all views related to pages
"""
from .page_tree_view import PageTreeView
from .page_form_view import PageFormView
from .page_actions import (
    archive_page,
    restore_page,
    view_page,
    delete_page,
    expand_page_translation_id,
    export_pdf,
    download_xliff,
    upload_xliff,
    move_page,
    grant_page_permission_ajax,
    revoke_page_permission_ajax,
    get_page_order_table_ajax,
    render_mirrored_page_field,
    cancel_translation_process_ajax,
)
from .page_sbs_view import PageSideBySideView
from .page_revision_view import PageRevisionView
from .page_xliff_import_view import PageXliffImportView
from .partial_page_tree_view import PartialPageTreeView
