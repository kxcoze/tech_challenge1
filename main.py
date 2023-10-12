from fastapi import FastAPI, HTTPException, Depends

from src.api.endpoints.questions import router as api_router
from db.init_db import init_db

init_db()


app = FastAPI()
app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
