from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from functools import wraps


def return_solo_key(function):
    @wraps(function)
    def wrapper(self, request, *args, **kwargs):
        response: Response = function(self, request, *args, **kwargs)
        if response.status_code == 200:
            response.data = {self.value: response.data}
        return response
    return wrapper


def return_plural_key(function):
    @wraps(function)
    def wrapper(self, request, *args, **kwargs):
        response: Response = function(self, request, *args, **kwargs)
        if response.status_code == 200:
            response.data = {self.plural_value: response.data}
        return response
    return wrapper


class ReturnModelViewSetMixin(ModelViewSet):
    value = None
    plural_value = None

    @return_solo_key
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @return_solo_key
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @return_solo_key
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @return_solo_key
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @return_plural_key
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ReturnReadOnlyModelViewSetMixin(ReadOnlyModelViewSet):
    value = None
    plural_value = None

    @return_solo_key
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @return_plural_key
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
