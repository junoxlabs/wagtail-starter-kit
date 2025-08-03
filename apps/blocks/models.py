from django.db import models
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.snippets.blocks import SnippetChooserBlock


class HeadingBlock(blocks.StructBlock):
    """
    Custom heading block with size options.
    """
    heading_text = blocks.CharBlock(required=True, max_length=255)
    size = blocks.ChoiceBlock(choices=[
        ('', 'Select a header size'),
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4'),
    ], blank=True, required=False)
    
    class Meta:
        icon = 'title'
        template = 'blocks/heading_block.html'


class RichTextBlock(blocks.RichTextBlock):
    """
    Custom rich text block with limited formatting options.
    """
    
    class Meta:
        icon = 'doc-full'
        template = 'blocks/rich_text_block.html'


class ImageBlock(blocks.StructBlock):
    """
    Custom image block with alt text and caption.
    """
    image = ImageChooserBlock(required=True)
    caption = blocks.CharBlock(required=False)
    attribution = blocks.CharBlock(required=False)
    
    class Meta:
        icon = 'image'
        template = 'blocks/image_block.html'


class QuoteBlock(blocks.StructBlock):
    """
    Custom quote block.
    """
    quote = blocks.TextBlock(required=True)
    author = blocks.CharBlock(required=False)
    author_title = blocks.CharBlock(required=False)
    
    class Meta:
        icon = 'openquote'
        template = 'blocks/quote_block.html'


class EmbedBlock(EmbedBlock):
    """
    Custom embed block with additional options.
    """
    
    class Meta:
        icon = 'media'
        template = 'blocks/embed_block.html'


class ButtonBlock(blocks.StructBlock):
    """
    Custom button block with text, link, and style choices.
    """
    button_text = blocks.CharBlock(required=True, max_length=50)
    link = blocks.URLBlock(required=True)
    style = blocks.ChoiceBlock(choices=[
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('outline', 'Outline'),
    ], default='primary')
    
    class Meta:
        icon = 'link'
        template = 'blocks/button_block.html'


class CardBlock(blocks.StructBlock):
    """
    Custom card block with image, title, text, and link.
    """
    title = blocks.CharBlock(required=True, max_length=100)
    text = blocks.RichTextBlock(required=True)
    image = ImageChooserBlock(required=False)
    link = blocks.URLBlock(required=False)
    link_text = blocks.CharBlock(required=False, max_length=50)
    
    class Meta:
        icon = 'form'
        template = 'blocks/card_block.html'


class CallToActionBlock(blocks.StructBlock):
    """
    Custom call to action block.
    """
    title = blocks.CharBlock(required=True, max_length=100)
    text = blocks.RichTextBlock(required=True)
    button_text = blocks.CharBlock(required=True, max_length=50)
    button_link = blocks.URLBlock(required=True)
    button_style = blocks.ChoiceBlock(choices=[
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('outline', 'Outline'),
    ], default='primary')
    
    class Meta:
        icon = 'arrow-right'
        template = 'blocks/cta_block.html'


class TwoColumnBlock(blocks.StructBlock):
    """
    Two column layout block.
    """
    left_column = blocks.StreamBlock([
        ('heading', HeadingBlock()),
        ('paragraph', RichTextBlock()),
        ('image', ImageBlock()),
        ('quote', QuoteBlock()),
        ('button', ButtonBlock()),
    ], required=False)
    
    right_column = blocks.StreamBlock([
        ('heading', HeadingBlock()),
        ('paragraph', RichTextBlock()),
        ('image', ImageBlock()),
        ('quote', QuoteBlock()),
        ('button', ButtonBlock()),
    ], required=False)
    
    class Meta:
        icon = 'grip'
        template = 'blocks/two_column_block.html'


class ThreeColumnBlock(blocks.StructBlock):
    """
    Three column layout block.
    """
    left_column = blocks.StreamBlock([
        ('heading', HeadingBlock()),
        ('paragraph', RichTextBlock()),
        ('image', ImageBlock()),
        ('quote', QuoteBlock()),
        ('button', ButtonBlock()),
    ], required=False)
    
    middle_column = blocks.StreamBlock([
        ('heading', HeadingBlock()),
        ('paragraph', RichTextBlock()),
        ('image', ImageBlock()),
        ('quote', QuoteBlock()),
        ('button', ButtonBlock()),
    ], required=False)
    
    right_column = blocks.StreamBlock([
        ('heading', HeadingBlock()),
        ('paragraph', RichTextBlock()),
        ('image', ImageBlock()),
        ('quote', QuoteBlock()),
        ('button', ButtonBlock()),
    ], required=False)
    
    class Meta:
        icon = 'grip'
        template = 'blocks/three_column_block.html'


class HeroBlock(blocks.StructBlock):
    """
    Custom hero block for primary page headers.
    """
    title = blocks.CharBlock(required=True, max_length=100)
    subtitle = blocks.CharBlock(required=False, max_length=200)
    background_image = ImageChooserBlock(required=False)
    text_color = blocks.ChoiceBlock(choices=[
        ('text-white', 'White'),
        ('text-black', 'Black'),
        ('text-gray-800', 'Dark Gray'),
    ], default='text-white')
    cta_button_text = blocks.CharBlock(required=False, max_length=50)
    cta_button_link = blocks.URLBlock(required=False)
    cta_button_style = blocks.ChoiceBlock(choices=[
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('outline', 'Outline'),
    ], default='primary')
    
    class Meta:
        icon = 'image'
        template = 'blocks/hero_block.html'


# Base StreamBlock for all pages
class BaseStreamBlock(blocks.StreamBlock):
    """
    Base StreamBlock that can be used across all page types.
    """
    heading = HeadingBlock()
    paragraph = RichTextBlock()
    image = ImageBlock()
    quote = QuoteBlock()
    embed = EmbedBlock()
    button = ButtonBlock()
    card = CardBlock()
    cta = CallToActionBlock()
    two_column = TwoColumnBlock()
    three_column = ThreeColumnBlock()
    hero = HeroBlock()
    
    class Meta:
        required = False
