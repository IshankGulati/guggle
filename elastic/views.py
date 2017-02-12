from django.views.generic.base import TemplateView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator


class Index(TemplateView):
    template_name = "partials/index.html"

    def dispatch(self, *args, **kwargs):
        return super(Index, self).dispatch(*args, **kwargs)
