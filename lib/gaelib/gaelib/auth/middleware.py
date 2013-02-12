from google.appengine.api import users


class AuthenticationMiddleware(object):
    def process_request(self, request):
        try:
            request.user = users.get_current_user()
        except users.UserNotFoundError:
            request.user = None
