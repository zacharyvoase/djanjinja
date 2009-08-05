# -*- coding: utf-8 -*-

from django.http import HttpResponse

import djanjinja


local_env = djanjinja.get_env().copy()
local_env.load('djanjinja', 'cache')


def global_(request):
    """Renders a template which uses the global cache object."""
    
    template = local_env.get_template('cache_global.txt')
    content = template.render().strip()
    return HttpResponse(content=content)
