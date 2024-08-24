from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from api.dependencies.stubs import get_sessionmaker


def setup_dependencies(app: FastAPI, sessionmaker: async_sessionmaker[AsyncSession]) -> None:
    app.dependency_overrides[get_sessionmaker] = lambda: sessionmaker
