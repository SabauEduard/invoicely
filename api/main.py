import signal

import os

import fastapi
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from routers.auth_router import auth_router, get_current_user
from routers.role_router import role_router
from routers.user_router import user_router


app = FastAPI(
    title="Invoicely API",
    summary="An API to manage invoices",
)

origins = [
    "http://localhost",
    "http://localhost:3050", 
]

# Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/users")
app.include_router(auth_router, prefix="/auth")
app.include_router(role_router, prefix="/roles", dependencies=[Depends(get_current_user)])


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/shutdown")
async def shutdown():
    os.kill(os.getpid(), signal.SIGTERM)
    return fastapi.Response(status_code=200, content='Server shutting down...')


@app.get("/health")
async def health():
    return fastapi.Response(status_code=200, content='OK')


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
openapi_schema = app.openapi()
openapi_schema["components"]["securitySchemes"] = {
    "BearerAuth": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }
}
