import typing

from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


class SuccessResponse(JSONResponse):
    msg: str = 'Success'
    code = status.HTTP_200_OK
    items: list

    def __init__(self, items: list, **kwargs):
        self.items = items
        # content = jsonable_encoder(content)
        kwargs['msg'] = self.msg
        content = dict(self.__dict__, **kwargs)
        super().__init__(content, status_code=self.code)


class CreatedResponse(JSONResponse):
    msg: str = 'Created'
    code = status.HTTP_201_CREATED

    def __init__(self, **kwargs):
        # content = jsonable_encoder(content)
        kwargs['msg'] = self.msg
        content = dict(self.__dict__, **kwargs)
        super().__init__(content, status_code=self.code)


class NotFoundResponse(JSONResponse):
    msg: str = 'Doc does not exist'
    code = status.HTTP_404_NOT_FOUND
    items: list = []

    def __init__(self, **kwargs):
        kwargs['msg'] = self.msg
        content = dict(self.__dict__, **kwargs)
        # content = jsonable_encoder(content)
        super().__init__(content, status_code=self.code)


class ConflictResponse(JSONResponse):
    msg: str = 'Docs/Doc already exist/s'
    code = status.HTTP_409_CONFLICT

    def __init__(self, **kwargs):
        kwargs['msg'] = self.msg
        content = dict(self.__dict__, **kwargs)
        # content = jsonable_encoder(content)
        super().__init__(content, status_code=self.code)


class NotModifiedResponse(JSONResponse):
    msg: str = 'This request would clear the very whole collection'
    code = status.HTTP_304_NOT_MODIFIED

    def __init__(self, **kwargs):
        kwargs['msg'] = self.msg
        content = dict(self.__dict__, **kwargs)
        # content = jsonable_encoder(content)
        super().__init__(content, status_code=self.code)
