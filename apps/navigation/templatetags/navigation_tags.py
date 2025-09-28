import logging
from django import template
from django.core.cache import cache
from apps.navigation.models import Menu

logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag
def get_menu(slug):
    """
    Returns a menu by slug with error handling.
    """
    try:
        return Menu.objects.get(slug=slug)
    except Menu.DoesNotExist:
        logger.warning(f"Menu with slug '{slug}' does not exist")
        return None
    except Exception as e:
        logger.error(f"Error retrieving menu with slug '{slug}': {str(e)}")
        return None


@register.simple_tag
def get_menu_tree(slug):
    """
    Returns the complete menu tree with nested structure for the given slug.
    Includes caching for performance optimization.
    """
    # Try to get from cache first
    cache_key = f"menu_tree_{slug}"
    cached_result = cache.get(cache_key)
    
    if cached_result is not None:
        return cached_result
    
    try:
        # Get menu with prefetched items
        menu = Menu.objects.prefetch_related(
            'menu_items__link_page',
            'menu_items__children__link_page'
        ).get(slug=slug)
        result = menu.get_menu_tree()
        
        # Cache for 15 minutes (adjust as needed)
        cache.set(cache_key, result, 900)
        return result
    except Menu.DoesNotExist:
        logger.warning(f"Menu with slug '{slug}' does not exist")
        return []
    except Exception as e:
        logger.error(f"Error retrieving menu tree for slug '{slug}': {str(e)}")
        return []


@register.simple_tag
def get_main_menu():
    """
    Convenience tag to get the main menu specifically.
    """
    return get_menu_tree('main-menu')


@register.simple_tag
def get_footer_menu():
    """
    Convenience tag to get the footer menu specifically.
    """
    return get_menu_tree('footer-menu')


@register.simple_tag
def get_legal_menu():
    """
    Convenience tag to get the legal menu specifically.
    """
    return get_menu_tree('legal-menu')
