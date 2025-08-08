from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from apps.core.models import BasePage
from apps.blocks.models import ContentStreamBlock


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
