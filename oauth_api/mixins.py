from oauthlib.oauth2 import Server

from oauth_api.validators import OAuthValidator
from oauth_api.handlers import OAuthHandler
from oauth_api.settings import oauth_api_settings


class OAuthViewMixin(object):
    """
    Base mixin for all views.
    """

    oauth_handler_class = None
    oauth_server_class = None
    oauth_validator_class = None

    def get_server_class(self):
        """
        Return the class to use for the endpoint.
        Defaults to `oauthlib.oauth2.Server`.
        """
        server_class = self.oauth_server_class
        if server_class is not None:
            return server_class
        return Server

    def get_validator_class(self):
        """
        Return the class to use validating the request.
        Defaults to `oauth_api.validators.OAuthValidator`.
        """
        validator_class = self.oauth_validator_class
        if validator_class is not None:
            return validator_class
        return OAuthValidator

    def get_handler_class(self):
        """
        Return the class to use with request data.
        Defaults to `oauth_api.handlers.RequestHandler.`
        """
        handler_class = self.oauth_handler_class
        if handler_class is not None:
            return handler_class
        return OAuthHandler

    def get_request_handler(self):
        """
        Return request handler instance from cache. New instance will be created if not available otherwise.
        """
        if not hasattr(self, '_oauth_handler'):
            handler_class = self.get_handler_class()
            server_class = self.get_server_class()
            validator_class = self.get_validator_class()
            validator = validator_class()
            server = server_class(validator, token_expires_in=oauth_api_settings.ACCESS_TOKEN_EXPIRATION)
            self._oauth_handler = handler_class(server)
        return self._oauth_handler

    def create_token_response(self, request):
        handler = self.get_request_handler()
        return handler.create_token_response(request)