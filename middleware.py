from .tokens import get_request_token


class SessionMiddleware(object):
    def process_request(self, request):
        if getattr(request, 'user', None) and request.user.is_authenticated():
            return

        # Token-based authentication is attempting to be used, bypass CSRF
        # check
        if get_request_token(request):
            request.csrf_processing_done = True
            return

        session = request.session
        # Ensure the session is created view processing, but only if a cookie
        # had been previously set. This is to prevent creating exorbitant
        # numbers of sessions for non-browser clients, such as bots.
        if session.session_key is None:
            if session.test_cookie_worked():
                session.delete_test_cookie()
                request.session.create()
            else:
                session.set_test_cookie()
