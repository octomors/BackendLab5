from models import Category, SessionDep


class CategoryRepository:
    def __init__(
        self,
        session: SessionDep,
    ):
        self.session = session

    def save(self, category: Category) -> None:
        self.session.add(category)

    async def delete(self, category: Category) -> None:
        await self.session.delete(category)
