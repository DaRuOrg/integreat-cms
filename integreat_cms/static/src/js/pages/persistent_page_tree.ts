/**
 * This file contains functions for persisting and restoring the expanded state of the page tree.
 */

import { toggleSubpagesForElement } from "./toggle-subpages";

/**
 * This function restores the state of the page tree.
 * Rows that are not visible won't get expanded.
 */
export function restorePageLayout() {
    const collapsed_rows: number[] = JSON.parse(window.sessionStorage.getItem("page_state"));
    const all_spans = Array.from(document.querySelectorAll(".toggle-subpages"));

    // Try expanding rows until no new visible rows can get expanded.
    // This approach is used because pages that are not visible should not get expanded,
    // and expanding a page can make its children visible.
    while (collapsed_rows && collapsed_rows.length > 0) {
        const previous_size = collapsed_rows.length;

        for (let i = collapsed_rows.length - 1; i >= 0; i -= 1) {
            const row = collapsed_rows[i];
            const span = all_spans.find((span) => JSON.parse(span.getAttribute("data-page-id")) == row);
            if (span && !span.closest("tr").classList.contains("hidden")) {
                toggleSubpagesForElement(span as HTMLSpanElement);
                collapsed_rows.splice(i, 1);
            }
        }
        if (collapsed_rows.length == previous_size) {
            break;
        }
    }
}

/**
 * This function updates the expanded state of the given page row.
 * This state is stored in the session storage.
 * 
 * @param page_id The id of the page to update
 * @param expanded Whether the page is now expanded or collapsed
 */
export function storeExpandedState(page_id: number, expanded: boolean) {
    var collapsed_rows = new Set(JSON.parse(window.sessionStorage.getItem("page_state")) || []);
    if (expanded) {
        collapsed_rows.add(page_id);
    } else {
        collapsed_rows.delete(page_id);
    }
    // The key can be independent of a region id, because different urls have different sessionStorage
    window.sessionStorage.setItem("page_state", JSON.stringify(Array.from(collapsed_rows)));
}