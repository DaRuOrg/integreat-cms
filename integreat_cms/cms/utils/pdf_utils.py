import hashlib
import logging

from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.cache import caches
from django.db.models import Min
from django.http import HttpRequest, HttpResponse
from django.template.loader import get_template
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache

from xhtml2pdf import pisa

from ..constants import text_directions
from ..models import Language

logger = logging.getLogger(__name__)


@never_cache
# pylint: disable=too-many-locals
def generate_pdf(region, language_slug, pages):
    """
    Function for handling a pdf export request for pages.
    The pages were either selected by cms user or by API request (see :func:`~integreat_cms.api.v3.pdf_export`)
    For more information on xhtml2pdf, see :doc:`xhtml2pdf:index`

    :param region: region which requested the pdf document
    :type region: ~integreat_cms.cms.models.regions.region.Region

    :param language_slug: bcp47 slug of the current language
    :type language_slug: str

    :param pages: at least on page to render as PDF document
    :type pages: ~mptt.querysets.TreeQuerySet

    :return: PDF document wrapped in a HtmlResponse
    :rtype: ~django.http.HttpResponse
    """
    # first all necessary data for hashing are collected, starting at region slug
    # region last_updated field taking into account, to keep track of maybe edited region icons
    pdf_key_list = [region.slug, region.last_updated]
    for page in pages:
        # add translation id and last_updated to hash key list if they exist
        page_translation = page.get_public_translation(language_slug)
        if page_translation:
            # if translation for this language exists
            pdf_key_list.append(page_translation.id)
            pdf_key_list.append(page_translation.last_updated)
        else:
            # if the page has no translation for this language
            pages = pages.exclude(id=page.id)
    # finally combine all list entries to a single hash key
    pdf_key_string = "_".join(map(str, pdf_key_list))
    # compute the hash value based on the hash key
    pdf_hash = hashlib.sha256(bytes(pdf_key_string, "utf-8")).hexdigest()
    cache = caches["pdf"]
    cached_response = cache.get(pdf_hash, "has_expired")
    if cached_response != "has_expired":
        # if django cache already contains a response object
        return cached_response
    amount_pages = pages.count()
    if amount_pages == 0:
        return HttpResponse(
            _("No valid pages selected for PDF generation."), status=400
        )
    if amount_pages == 1:
        # If pdf contains only one page, take its title as filename
        title = pages.first().get_public_translation(language_slug).title
    else:
        # If pdf contains multiple pages, check the minimum level
        min_level = pages.aggregate(Min("level")).get("level__min")
        # Query all pages with this minimum level
        min_level_pages = pages.filter(level=min_level)
        if min_level_pages.count() == 1:
            # If there's exactly one page with the minimum level, take its title
            title = min_level_pages.first().get_public_translation(language_slug).title
        else:
            # In any other case, take the region name
            title = region.name
    language = Language.objects.get(slug=language_slug)
    filename = f"Integreat - {language.translated_name} - {title}.pdf"
    context = {
        "right_to_left": language.text_direction == text_directions.RIGHT_TO_LEFT,
        "region": region,
        "pages": pages,
        "language": language,
        "amount_pages": amount_pages,
        "prevent_italics": ["ar", "fa"],
        "request": HttpRequest(),
    }
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'filename="{filename}"'
    html = get_template("pages/page_pdf.html").render(context)
    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback, encoding="UTF-8"
    )
    # pylint: disable=no-member
    if pisa_status.err:
        logger.error(
            "The following PDF could not be rendered: %r, %r, %r",
            region,
            language,
            pages,
        )
        return HttpResponse(
            _("The PDF could not be successfully generated."), status=500
        )
    cache.set(pdf_hash, response, 60 * 60 * 24)
    return response


# pylint: disable=unused-argument
def link_callback(uri, rel):
    """
    According to xhtml2pdf documentation (see :doc:`xhtml2pdf:usage`),
    this function is necessary for resolving the django static files references.
    It returns the absolute paths to the files on the file system.

    :param uri: URI that is generated by django template tag 'static'
    :type uri: str

    :param rel: The relative path directory
    :type rel: str

    :return: The absolute path on the file system according to django's static file settings
    :rtype: str
    """
    if uri.startswith(settings.MEDIA_URL):
        # Remove the MEDIA_URL from the start of the uri
        uri = uri[len(settings.MEDIA_URL) :]
    elif uri.startswith(settings.STATIC_URL):
        # Remove the STATIC_URL from the start of the uri
        uri = uri[len(settings.STATIC_URL) :]
    elif uri.startswith("../"):
        # Remove ../ from the start of the uri
        uri = uri[3:]
    else:
        logger.warning(
            "The file %r is not inside the static directories %r and %r.",
            uri,
            settings.STATIC_URL,
            settings.MEDIA_URL,
        )
        return uri
    result = finders.find(uri)
    if not result:
        logger.exception(
            "The file %r was not found in the static directories %r.",
            uri,
            finders.searched_locations,
        )
    return result