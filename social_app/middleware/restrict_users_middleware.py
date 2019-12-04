from django.shortcuts import redirect


class RestrictAdminToAdminArea:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        is_authenticated = request.user.is_authenticated

        # For Admins
        if is_authenticated and request.user.is_superuser:
            if not request.path.startswith('/admin/'):
                return redirect('admin:index')

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
