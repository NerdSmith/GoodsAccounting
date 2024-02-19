from typing import TypeVar

from src.db.db import get_async_scoped_session

ServiceType = TypeVar("ServiceType")
RepositoryType = TypeVar("RepositoryType")


async def get_service(
    target_service: type[ServiceType], target_repo: type[RepositoryType]
) -> ServiceType:
    async with get_async_scoped_session() as session:
        repo: RepositoryType = target_repo(session)  # type: ignore
        service: ServiceType = target_service(repo)  # type: ignore
        return service
