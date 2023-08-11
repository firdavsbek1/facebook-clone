from django.utils import timezone


class UpdateLastActivityMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request,
                       'user'), 'The UpdateLastActivityMiddleware requires authentication middleware to be installed.'
        if request.user.is_authenticated:
            request.user.last_activity = timezone.now()
