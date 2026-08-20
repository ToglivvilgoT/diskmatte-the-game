from django import template

register = template.Library()


@register.inclusion_tag("cosmetics/_skin_orb.html")
def skin_orb(skin, size_class, fallback="D"):
    """Render a skin's visual (image, css class or color) as a single reusable element."""
    return {
        "skin": skin,
        "size_class": size_class,
        "fallback": fallback,
    }
