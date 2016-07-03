from django.template import Library, Node, TemplateSyntaxError
register = Library()

#custom template filter - place this in your custom template tags file
@register.filter
def only_hours(value):
    """
    Filter - removes the minutes, seconds, and milliseconds from a datetime

    Example usage in template:

    {{ my_datetime|only_hours|timesince }}

    This would show the hours in my_datetime without showing the minutes or seconds.
    """
    #replace returns a new object instead of modifying in place
    return value.replace(minute=0, second=0, microsecond=0)