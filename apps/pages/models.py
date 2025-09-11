from django.db import models
from django.core.exceptions import ValidationError
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Orderable
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey
from apps.core.models import BasePage
from apps.blocks.models import ContentStreamBlock
import uuid


class FlexPage(BasePage):
    """
    A flexible page model that can be used for the homepage or other standard pages.
    It uses a StreamField for maximum content flexibility.
    """

    # Main content area as a StreamField for flexible content
    body = StreamField(
        ContentStreamBlock(),
        use_json_field=True,
        blank=True,
    )

    content_panels = BasePage.content_panels + [
        FieldPanel("body"),
    ]

    promote_panels = BasePage.promote_panels
    settings_panels = BasePage.settings_panels

    # Allow only one instance at the root level
    parent_page_types = ["wagtailcore.Page", "home.FlexPage"]

    # Specify the template for this page
    template = "pages/flex_page.html"

    class Meta:
        verbose_name = "Flex Page"
        verbose_name_plural = "Flex Pages"


@register_snippet
class Category(models.Model):
    """
    A category for organizing showcase entities.
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]


@register_snippet
class Link(models.Model):
    """
    A link with title, URL, and type.
    """

    LINK_TYPE_CHOICES = [
        ("website", "Website"),
        ("github", "GitHub"),
        ("demo", "Demo"),
        ("documentation", "Documentation"),
        ("other", "Other"),
    ]

    title = models.CharField(max_length=200)
    url = models.URLField()
    link_type = models.CharField(
        max_length=20, choices=LINK_TYPE_CHOICES, default="website"
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("url"),
        FieldPanel("link_type"),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Link"
        verbose_name_plural = "Links"


class BaseEntityPage(FlexPage):
    """
    Abstract base page for all showcase entities with common fields.
    """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    category = models.ForeignKey(
        "pages.Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    URL_TYPE_CHOICES = [
        ("seo", "SEO-friendly Slug"),
        ("uuid", "UUID-based"),
    ]
    url_type_preference = models.CharField(
        max_length=10,
        choices=URL_TYPE_CHOICES,
        default="seo",
        help_text="Choose whether to display SEO-friendly URLs or UUID-based URLs",
    )

    # Add category to content panels
    content_panels = FlexPage.content_panels + [
        FieldPanel("category"),
        FieldPanel("url_type_preference"),
    ]

    template = "pages/entity_base.html"

    class Meta:
        abstract = True

    def get_url_parts(self, request=None, current_site=None):
        """
        Override URL generation to support both SEO-friendly and UUID-based URLs.
        """
        url_parts = super().get_url_parts(request, current_site)
        if url_parts is None:
            return None

        if self.url_type_preference == "uuid" and self.uuid:
            # Replace the slug part with the UUID
            site_id, root_url, page_path = url_parts
            # Split the path and replace the last part (slug) with UUID
            path_parts = page_path.rstrip("/").split("/")
            if path_parts:
                path_parts[-1] = str(self.uuid)
                page_path = "/".join(path_parts) + "/"
            return (site_id, root_url, page_path)

        return url_parts

    def get_uuid_url(self):
        """
        Get the UUID-based URL for this page.
        """
        if self.uuid:
            # Get the parent URL and append the UUID
            if self.get_parent():
                parent_url = self.get_parent().specific.get_url()
                return f"{parent_url}uuid/{self.uuid}/"
            return f"/uuid/{self.uuid}/"
        return "#"


class ProjectLink(Orderable):
    """
    Links for a project.
    """

    project = ParentalKey(
        "pages.ProjectPage", on_delete=models.CASCADE, related_name="links"
    )
    link = models.ForeignKey("pages.Link", on_delete=models.CASCADE, related_name="+")

    panels = [
        FieldPanel("link"),
    ]

    def __str__(self):
        return f"{self.project.title} -> {self.link.title}"


class ProjectPage(BaseEntityPage):
    """
    A project page that may or may not have child pages.
    """

    has_page = models.BooleanField(
        default=False, help_text="Check this box if this project has its own page"
    )

    content_panels = BaseEntityPage.content_panels + [
        FieldPanel("has_page"),
        InlinePanel("links", label="Links"),
    ]

    parent_page_types = ["pages.ShowcasePage"]
    subpage_types = ["pages.FlexPage"]  # Only if has_page is True
    template = "pages/project_page.html"

    def clean(self):
        # If has_page is False, ensure no child pages exist
        if not self.has_page and self.get_children().exists():
            raise ValidationError("Cannot have child pages when 'has_page' is False.")

    def save(self, *args, **kwargs):
        # Update subpage_types based on has_page value
        if self.has_page:
            self.subpage_types = ["pages.FlexPage"]
        else:
            self.subpage_types = []
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Project Page"
        verbose_name_plural = "Project Pages"


class ServicePage(BaseEntityPage):
    """
    A service page that always has child pages.
    """

    content_panels = BaseEntityPage.content_panels + [
        InlinePanel(
            "links",
            label="Links",
            help_text="Services typically don't have links in list view, but you can add them here if needed",
        ),
    ]

    parent_page_types = ["pages.ShowcasePage"]
    subpage_types = ["pages.FlexPage"]
    template = "pages/service_page.html"

    def save(self, *args, **kwargs):
        # Services always have pages, so we don't need to modify subpage_types
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Service Page"
        verbose_name_plural = "Service Pages"


class PortfolioItemLink(Orderable):
    """
    Links for a portfolio item.
    """

    portfolio_item = ParentalKey(
        "pages.PortfolioItemPage", on_delete=models.CASCADE, related_name="links"
    )
    link = models.ForeignKey("pages.Link", on_delete=models.CASCADE, related_name="+")

    panels = [
        FieldPanel("link"),
    ]

    def __str__(self):
        return f"{self.portfolio_item.title} -> {self.link.title}"


class PortfolioItemPage(BaseEntityPage):
    """
    A portfolio item page that always has child pages and includes an image.
    """

    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    content_panels = BaseEntityPage.content_panels + [
        FieldPanel("image"),
        InlinePanel("links", label="Links"),
    ]

    parent_page_types = ["pages.ShowcasePage"]
    subpage_types = ["pages.FlexPage"]
    template = "pages/portfolio_item_page.html"

    class Meta:
        verbose_name = "Portfolio Item Page"
        verbose_name_plural = "Portfolio Item Pages"


class ResourceLink(Orderable):
    """
    Links for a resource.
    """

    resource = ParentalKey(
        "pages.ResourcePage", on_delete=models.CASCADE, related_name="links"
    )
    link = models.ForeignKey("pages.Link", on_delete=models.CASCADE, related_name="+")

    panels = [
        FieldPanel("link"),
    ]

    def __str__(self):
        return f"{self.resource.title} -> {self.link.title}"


class ResourcePage(BaseEntityPage):
    """
    A resource page that doesn't have its own page (no child pages).
    """

    content_panels = BaseEntityPage.content_panels + [
        InlinePanel("links", label="Links"),
    ]

    parent_page_types = ["pages.ShowcasePage"]
    subpage_types = []  # Resources don't have child pages
    template = "pages/resource_page.html"

    def save(self, *args, **kwargs):
        # Resources never have pages, so ensure subpage_types is empty
        self.subpage_types = []
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Resource Page"
        verbose_name_plural = "Resource Pages"


class ShowcasePage(BasePage):
    """
    A page that showcases different types of entities (projects, services, portfolio items, resources).
    Can display entities by category.
    """

    ENTITY_TYPE_CHOICES = [
        ("projects", "Projects"),
        ("services", "Services"),
        ("portfolio", "Portfolio Items"),
        ("resources", "Resources"),
    ]

    entity_types_to_display = models.CharField(
        max_length=100,
        choices=ENTITY_TYPE_CHOICES,
        default="projects",
        help_text="Select which entity type to display",
    )

    category_filter = models.ForeignKey(
        "pages.Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        help_text="Filter entities by category (leave blank to show all)",
    )

    content_panels = BasePage.content_panels + [
        FieldPanel("entity_types_to_display"),
        FieldPanel("category_filter"),
    ]

    parent_page_types = ["wagtailcore.Page"]
    subpage_types = [
        "pages.ProjectPage",
        "pages.ServicePage",
        "pages.PortfolioItemPage",
        "pages.ResourcePage",
    ]

    template = "pages/showcase_page.html"

    class Meta:
        verbose_name = "Showcase Page"
        verbose_name_plural = "Showcase Pages"

    def get_entities(self):
        """
        Get entities based on the selected entity type and category filter.
        """
        # Get the appropriate page model based on entity type
        if self.entity_types_to_display == "projects":
            entities = ProjectPage.objects.live().descendant_of(self)
        elif self.entity_types_to_display == "services":
            entities = ServicePage.objects.live().descendant_of(self)
        elif self.entity_types_to_display == "portfolio":
            entities = PortfolioItemPage.objects.live().descendant_of(self)
        elif self.entity_types_to_display == "resources":
            entities = ResourcePage.objects.live().descendant_of(self)
        else:
            entities = ProjectPage.objects.none()

        # Apply category filter if specified
        if self.category_filter:
            entities = entities.filter(category=self.category_filter)

        return entities

    def get_entities_by_category(self):
        """
        Get entities organized by category.
        """
        entities = self.get_entities()

        # Group entities by category
        categories = {}
        for entity in entities:
            category_name = entity.category.name if entity.category else "Uncategorized"
            if category_name not in categories:
                categories[category_name] = []
            categories[category_name].append(entity)

        return categories
