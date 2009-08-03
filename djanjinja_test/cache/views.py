# -*- coding: utf-8 -*-

from django.http import HttpResponse

import djanjinja


def global_(request):
    """Renders a template which uses the global cache object."""
    
    template = djanjinja.get_template('cache_global.txt')
    content = template.render().strip()
    return HttpResponse(content=content)
