from functools import wraps

from settings import FARMINGCONCRETE_YEAR

def year_in_session(f):
    """
    Stores year in session for use in places like templates
    """
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        year = kwargs.get('year', None) or FARMINGCONCRETE_YEAR
        request.session['year'] = kwargs['year'] = year
        return f(request, *args, **kwargs)
    return wrapper

def garden_type_aware(f):
    """
    Ensures that the garden_type session variable is set to 'all' if it's not already set
    """
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        if 'garden_type' not in request.session:
            request.session['garden_type'] = 'all'
        return f(request, *args, **kwargs)
    return wrapper

def in_section(section):
    """
    Sets a session variable for the section of the site a view is in.
    """
    def decorator(f):
        @wraps(f)
        def wrapper(request, *args, **kwargs):
            if section:
                request.session['section'] = section
            return f(request, *args, **kwargs)
        return wrapper
    return decorator
