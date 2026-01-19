from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


class BuildJSONResponses:
    @staticmethod
    def record_not_found():
        return JSONResponse(
            content={"data": [], "succeeded": True, "message": "Record Not Found"},
            status_code=status.HTTP_200_OK,
        )

    @staticmethod
    def success_response(
        data=None, message=None, status_code=status.HTTP_200_OK, succeeded=True
    ):
        return JSONResponse(
            content={
                "data": jsonable_encoder(data),
                "succeeded": succeeded,
                "message": message,
                "httpStatusCode": status_code,
            },
            status_code=status.HTTP_200_OK,
        )

    @staticmethod
    def success_response_with_pagination_metadata(
        data=None, message=None, paginated_response=None
    ):
        return JSONResponse(
            content={
                "data": jsonable_encoder(data),
                "succeeded": True,
                "message": message,
                "pagination_metadata": paginated_response,
            },
            status_code=status.HTTP_200_OK,
        )

    @staticmethod
    def invalid_input(message):
        return JSONResponse(
            content={"data": [], "succeeded": False, "message": message},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def raise_exception(message):
        return JSONResponse(
            content={"succeeded": False, "message": str(message)},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

