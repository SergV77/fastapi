from fastapi import FastAPI, HTTPException, Depends
from starlette import status
from starlette.requests import Request

import settings
from router import api_router
from utils import check_auth

docs_kwargs = {}
if settings.ENVIRONMENT == 'production':
    docs_kwargs = dict(docs_url=None, redoc_url=None)

app = FastAPI(**docs_kwargs)


async def check_auth_middleware(request: Request):
    if settings.ENVIRONMENT in ('prodection', 'test'):
        body = await request.body()
        if not check_auth(body, request.headers.get('X-Hub-Signature', '')):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

app.include_router(api_router, dependencies=[Depends(check_auth_middleware)])
#
# @app.post("/release/")
# async def release(*,
#                body: Body,
#                chat_id: str = None
#                ):
#     await proceed_release(body, chat_id)
#     return Response(status_code=status.HTTP_200_OK)

# @app.get("/")
# async def root():
#     return {"message": "Hello, world!"}



