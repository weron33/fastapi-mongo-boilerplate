import typing

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


class SuccessResponse(JSONResponse):
    msg: str = 'Success'

    def __init__(self, content: typing.Any):
        # content = jsonable_encoder(content)
        super().__init__(content)
