import uvicorn

from fastapi import FastAPI
from src.routers.contacts import router as contact_rout
from src.routers.auth import router as auth_rout

app = FastAPI()

app.include_router(contact_rout)
app.include_router(auth_rout)


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0", port=8000,
    )