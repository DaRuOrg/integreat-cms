"""
This modules contains the config for the API tests
"""

#: The API endpoints
API_ENDPOINTS = [
    (
        "/api/regions/",
        "/wp-json/extensions/v3/sites/",
        "tests/api/expected-outputs/regions.json",
        200,
    ),
    (
        "/api/regions/live/",
        "/wp-json/extensions/v3/sites/live/",
        "tests/api/expected-outputs/regions_live.json",
        200,
    ),
    (
        "/api/augsburg/de/pages/",
        "/augsburg/de/wp-json/extensions/v3/pages/",
        "tests/api/expected-outputs/augsburg_de_pages.json",
        200,
    ),
    (
        "/api/augsburg/de/locations/",
        "/augsburg/de/wp-json/extensions/v3/locations/",
        "tests/api/expected-outputs/augsburg_de_locations.json",
        200,
    ),
    (
        "/api/augsburg/de/children/",
        "/augsburg/de/wp-json/extensions/v3/children/",
        "tests/api/expected-outputs/augsburg_de_children.json",
        200,
    ),
    (
        "/api/augsburg/de/children/?depth=3&url=/augsburg/de/behörden-und-beratung/behörden/",
        "/augsburg/de/wp-json/extensions/v3/children/?depth=3&url=/augsburg/de/behörden-und-beratung/behörden/",
        "tests/api/expected-outputs/augsburg_de_children_archived_descendants.json",
        200,
    ),
    (
        "/augsburg/de/wp-json/extensions/v3/page/?url=/augsburg/de/behörden-und-beratung/behörden/archiviertes-amt/",
        "/augsburg/de/wp-json/extensions/v3/page/?url=/augsburg/de/behörden-und-beratung/behörden/archiviertes-amt/",
        "tests/api/expected-outputs/augsburg_de_page_archived.json",
        404,
    ),
    (
        "/api/augsburg/de/children/?depth=2",
        "/augsburg/de/wp-json/extensions/v3/children/?depth=2",
        "tests/api/expected-outputs/api_augsburg_de_children_depth_2.json",
        200,
    ),
    (
        "/api/augsburg/de/events/",
        "/augsburg/de/wp-json/extensions/v3/events/",
        "tests/api/expected-outputs/augsburg_de_events.json",
        200,
    ),
    (
        "/api/augsburg/de/page/?id=1",
        "/augsburg/de/wp-json/extensions/v3/page/?id=1",
        "tests/api/expected-outputs/augsburg_de_page_1.json",
        200,
    ),
    (
        "/api/nurnberg/de/fcm/",
        "/nurnberg/de/wp-json/extensions/v3/fcm/",
        "tests/api/expected-outputs/nurnberg_de_fcm.json",
        200,
    ),
    (
        "/api/nurnberg/en/fcm/",
        "/nurnberg/en/wp-json/extensions/v3/fcm/",
        "tests/api/expected-outputs/nurnberg_en_fcm.json",
        200,
    ),
    (
        "/api/nurnberg/ar/fcm/",
        "/nurnberg/ar/wp-json/extensions/v3/fcm/",
        "tests/api/expected-outputs/nurnberg_ar_fcm.json",
        200,
    ),
]
