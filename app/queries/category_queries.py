from sqlalchemy import Select, select
from models import SessionDep, Category
from exceptions import CategoryNotFoundException


class CategoryQueries:

    def __init__(
        self,
        session: SessionDep,
    ):
        self.session = session

    def get_categories_query(self) -> Select[tuple[Category]]:
        return select(Category).order_by(Category.id)

    async def get_by_id(self, category_id: int) -> Category | None:
        category = await self.session.get(Category, category_id)
        if not category:
            raise CategoryNotFoundException()
        # В идеале возвращать DTO, а не модель
        return category
