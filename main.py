from contextlib import asynccontextmanager
from fastapi import FastAPI, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from src.settings import settings
import uvicorn
from src import api_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        pass
    except Exception as e:
        print("Error during initialization:", e)
        raise
    yield


app = FastAPI(lifespan=lifespan, **settings.fastapi_kwargs)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/", response_model=dict, status_code=status.HTTP_200_OK)
async def root() -> dict:

    return {"message": f"Welcome to the {settings.PROJECT_NAME}"}


if __name__ == "__main__":
    uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)
