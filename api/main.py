from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
async def read_root():
    return {"Hello": "World"}