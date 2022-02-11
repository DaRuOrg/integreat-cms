from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from linkcheck.models import Link

from .languages.language import Language
from ..constants import status
from ..utils.translation_utils import ugettext_many_lazy as __


class AbstractContentTranslation(models.Model):
    """
    Data model representing a translation of some kind of content (e.g. pages or events)
    """

    title = models.CharField(max_length=1024, verbose_name=_("title"))
    slug = models.SlugField(
        max_length=1024,
        allow_unicode=True,
        verbose_name=_("link"),
        help_text=__(
            _("String identifier without spaces and special characters."),
            _("Unique per region and language."),
            _("Leave blank to generate unique parameter from title."),
        ),
    )
    #: Manage choices in :mod:`~integreat_cms.cms.constants.status`
    status = models.CharField(
        max_length=9,
        choices=status.CHOICES,
        default=status.DRAFT,
        verbose_name=_("status"),
    )
    content = models.TextField(blank=True, verbose_name=_("content"))
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        verbose_name=_("language"),
    )
    currently_in_translation = models.BooleanField(
        default=False,
        verbose_name=_("currently in translation"),
        help_text=_(
            "Flag to indicate a translation is being updated by an external translator"
        ),
    )
    version = models.PositiveIntegerField(default=0, verbose_name=_("revision"))
    minor_edit = models.BooleanField(
        default=False,
        verbose_name=_("minor edit"),
        help_text=_(
            "Tick if this change does not require an update of translations in other languages."
        ),
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_("modification date"),
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("creator"),
    )
    links = GenericRelation(Link)

    @staticmethod
    def foreign_field():
        """
        The field name of the reference to the foreign object which the translation belongs to

        To be implemented in the inheriting model
        """
        raise NotImplementedError

    @cached_property
    def foreign_object(self):
        """
        Returns the object the translation belongs to
        This is needed to generalize the :mod:`~integreat_cms.cms.utils.slug_utils` for all content types

        To be implemented in the inheriting model
        """
        raise NotImplementedError

    @cached_property
    def url_prefix(self):
        """
        Generates the prefix of the url of the content translation object

        For information about the components of such an url,
        see :meth:`~integreat_cms.cms.models.abstract_content_translation.AbstractContentTranslation.get_absolute_url`

        :return: The prefix to the url
        :rtype: str
        """
        return (
            "/"
            + "/".join(
                filter(
                    None,
                    [
                        self.foreign_object.region.slug,
                        self.language.slug,
                        self.url_infix,
                    ],
                )
            )
            + "/"
        )

    @cached_property
    def url_infix(self):
        """
        Generates the infix of the url of the content translation object

        For information about the components of such an url,
        see :meth:`~integreat_cms.cms.models.abstract_content_translation.AbstractContentTranslation.get_absolute_url`

        To be implemented in the inheriting model
        """
        raise NotImplementedError

    @cached_property
    def base_link(self):
        """
        Generates the base link which is the whole url without slug

        For information about the components of such an url,
        see :meth:`~integreat_cms.cms.models.abstract_content_translation.AbstractContentTranslation.get_absolute_url`

        :return: the base link of the content
        :rtype: str
        """
        if not self.id:
            return settings.WEBAPP_URL + "/"
        return settings.WEBAPP_URL + self.url_prefix

    def get_absolute_url(self):
        """
        Generates the absolute url of the content translation object

        Here is an example for demonstrating the components of a page url::

            https://integreat.app/augsburg/en/welcome/city-map/attractions/
                                 |----------------------------------------|    get_absolute_url()
            |-------------------------------------------------|                base_link
                                 |----------------------------|                url_prefix
                                             |----------------|                url_infix
                                                              |-----------|    slug

        Here is an example for demonstrating the components of an event url::

            https://integreat.app/augsburg/en/events/test-event/
                                 |-----------------------------|    get_absolute_url()
            |---------------------------------------|               base_link
                                 |------------------|               url_prefix
                                             |------|               url_infix
                                                    |----------|    slug

        :return: The absolute url
        :rtype: str
        """
        return self.url_prefix + self.slug + "/"

    @cached_property
    def backend_edit_link(self):
        """
        Generates the url of the edit page for the content

        To be implemented in the inheriting model
        """
        raise NotImplementedError

    @cached_property
    def available_languages(self):
        """
        This property checks in which :class:`~integreat_cms.cms.models.languages.language.Language` the content is
        translated apart from ``self.language``.
        It only returns languages which have a public translation, so drafts are not included here.
        The returned dict has the following format::

            {
                available_translation.language.slug: {
                    'id': available_translation.id,
                    'url': available_translation.permalink
                    'path': available_translation.path
                },
                ...
            }

        :return: A dictionary containing the available languages of a content translation
        :rtype: dict
        """
        available_languages = {}
        for language in self.foreign_object.public_languages:
            if language == self.language:
                continue
            other_translation = self.foreign_object.get_public_translation(
                language.slug
            )
            if other_translation:
                absolute_url = other_translation.get_absolute_url()
                available_languages[language.slug] = {
                    "id": other_translation.id,
                    "url": settings.BASE_URL + absolute_url,
                    "path": absolute_url,
                }
        return available_languages

    @cached_property
    def sitemap_alternates(self):
        """
        This property returns the language alternatives of a content translation for the use in sitemaps.
        Similar to :func:`~integreat_cms.cms.models.abstract_content_translation.AbstractContentTranslation.available_languages`,
        but in a slightly different format.

        :return: A list of dictionaries containing the alternative translations of a content translation
        :rtype: list [ dict ]
        """
        available_languages = []
        for language in self.foreign_object.public_languages:
            if language == self.language:
                continue
            other_translation = self.foreign_object.get_public_translation(
                language.slug
            )
            if other_translation:
                available_languages.append(
                    {
                        "location": f"{settings.WEBAPP_URL}{other_translation.get_absolute_url()}",
                        "lang_slug": other_translation.language.slug,
                    }
                )
        return available_languages

    @cached_property
    def source_translation(self):
        """
        This property returns the translation which was used to create the ``self`` translation.
        It derives this information from the :class:`~integreat_cms.cms.models.regions.region.Region`'s root
        :class:`~integreat_cms.cms.models.languages.language_tree_node.LanguageTreeNode`.

        :return: The content translation in the source :class:`~integreat_cms.cms.models.languages.language.Language`
                 (:obj:`None` if the translation is in the :class:`~integreat_cms.cms.models.regions.region.Region`'s
                 default :class:`~integreat_cms.cms.models.languages.language.Language`)
        :rtype: ~integreat_cms.cms.models.abstract_content_translation.AbstractContentTranslation
        """
        source_language = self.foreign_object.region.get_source_language(
            self.language.slug
        )
        if source_language:
            return self.foreign_object.get_translation(source_language.slug)
        return None

    @cached_property
    def latest_revision(self):
        """
        This property is a link to the most recent version of this translation.

        :return: The latest revision of the translation
        :rtype: ~integreat_cms.cms.models.abstract_content_translation.AbstractContentTranslation
        """
        return self.foreign_object.translations.filter(
            language=self.language,
        ).first()

    @cached_property
    def latest_public_revision(self):
        """
        This property is a link to the most recent public version of this translation.
        If the translation itself is not public, this property can return a revision which is older than ``self``.

        :return: The latest public revision of the translation
        :rtype: ~integreat_cms.cms.models.abstract_content_translation.AbstractContentTranslation
        """
        return self.foreign_object.translations.filter(
            language=self.language,
            status=status.PUBLIC,
        ).first()

    @cached_property
    def latest_major_revision(self):
        """
        This property is a link to the most recent major version of this translation.

        :return: The latest major revision of the translation
        :rtype: ~integreat_cms.cms.models.abstract_content_translation.AbstractContentTranslation
        """
        return self.foreign_object.translations.filter(
            language=self.language,
            minor_edit=False,
        ).first()

    @cached_property
    def latest_major_public_revision(self):
        """
        This property is a link to the most recent major public version of this translation.
        This is used when translations, which are derived from this translation, check whether they are up to date.

        :return: The latest major public revision of the translation
        :rtype: ~integreat_cms.cms.models.abstract_content_translation.AbstractContentTranslation
        """
        return self.foreign_object.translations.filter(
            language=self.language,
            status=status.PUBLIC,
            minor_edit=False,
        ).first()

    @cached_property
    def previous_revision(self):
        """
        This property is a shortcut to the previous revision of this translation

        :return: The previous translation
        :rtype: ~integreat_cms.cms.models.abstract_content_translation.AbstractContentTranslation
        """
        version = self.version - 1
        return self.foreign_object.translations.filter(
            language=self.language,
            version=version,
        ).first()

    @cached_property
    def is_outdated(self):
        """
        This property checks whether a translation is outdated and thus needs a new revision of the content.
        This happens, when the source translation is updated and the update is no `minor_edit`.

        * If the translation is currently being translated, it is considered not outdated.
        * If the translation's language is the region's default language, it is defined to be never outdated.
        * If the translation's source translation is already outdated, then the translation itself also is.
        * If neither the translation nor its source translation have a latest major public translation, it is defined as
          not outdated.
        * If neither the translation nor its source translation have a latest major public translation, it is defined as
          not outdated.

        Otherwise, the outdated flag is calculated by comparing the `last_updated`-field of the translation and its
        source translation.

        :return: Flag to indicate whether the translation is outdated
        :rtype: bool
        """
        # If the translation is currently in translation, it is defined as not outdated
        if self.currently_in_translation:
            return False
        return self.is_outdated_helper

    @cached_property
    def is_outdated_helper(self):
        """
        See :meth:`~integreat_cms.cms.models.abstract_content_translation.AbstractContentTranslation.is_outdated`
        with the difference that it does not return ``False`` when ``currently_in_translation`` is ``True``.

        :return: Flag to indicate whether the translation is outdated
        :rtype: bool
        """
        source_translation = self.source_translation
        # If self.language is the root language, this translation can never be outdated
        if not source_translation:
            return False
        # If the source translation is outdated, this translation can not be up to date
        if source_translation.is_outdated:
            return True
        self_revision = self.latest_major_public_revision
        source_revision = source_translation.latest_major_public_revision
        # If one of the translations has no major public revision, it cannot be outdated
        if not self_revision or not source_revision:
            return False
        return self_revision.last_updated < source_revision.last_updated

    @cached_property
    def is_up_to_date(self):
        """
        This property checks whether a translation is up to date.
        A translation is considered up to date when it is not outdated and not being translated at the moment.

        :return: Flag which indicates whether a translation is up to date
        :rtype: bool
        """
        return not self.currently_in_translation and not self.is_outdated

    @classmethod
    def search(cls, region, language_slug, query):
        """
        Searches for all content translations which match the given `query` in their title or slug.
        :param region: The current region
        :type region: ~integreat_cms.cms.models.regions.region.Region
        :param language_slug: The language slug
        :type language_slug: str
        :param query: The query string used for filtering the content translations
        :type query: str
        :return: A query for all matching objects
        :rtype: ~django.db.models.QuerySet
        """
        return (
            cls.objects.filter(
                **{cls.foreign_field() + "__region": region},
                language__slug=language_slug,
            )
            .filter(Q(slug__icontains=query) | Q(title__icontains=query))
            .distinct(cls.foreign_field())
        )

    def __str__(self):
        """
        This overwrites the default Django :meth:`~django.db.models.Model.__str__` method.
        It is used in the Django admin backend and as label for ModelChoiceFields.

        :return: A readable string representation of the content translation
        :rtype: str
        """
        return self.title

    def __repr__(self):
        """
        This overwrites the default Django ``__repr__()`` method.
        It is used for logging.

        :return: The canonical string representation of the content translation
        :rtype: str
        """
        return (
            f"<{type(self).__name__} ("
            f"id: {self.id}, "
            f"{self.foreign_field()}_id: {self.foreign_object.id}, "
            f"language: {self.language.slug}, "
            f"slug: {self.slug})>"
        )

    class Meta:
        #: This model is an abstract base class
        abstract = True