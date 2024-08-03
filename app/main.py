import uvicorn
from fastapi import FastAPI

from app.domain.store.api import router as store_router
from app.domain.data.api import router as data_router
from app.database import Base, engine


def get_app():
    app = FastAPI()
    app.include_router(store_router)
    app.include_router(data_router)

    @app.on_event("startup")
    async def startup():
        Base.metadata.create_all(bind=engine)

    return app


def main():
    uvicorn.run(
        "app.main:get_app",
        host="0.0.0.0",
        port=8443,
        reload=False,
        factory=True
    )


if __name__ == "__main__":
    main()
