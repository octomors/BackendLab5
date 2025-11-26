from typing import Annotated
from fastapi import Depends
from repositories.tag_repository import TagRepository
from repositories.category_repository import CategoryRepository
from repositories.post_repository import PostRepository
from queries.category_queries import CategoryQueries
from queries.post_queries import PostQueries
from queries.tag_queries import TagQueries
from schemas.post_schema import PostCreate, PostUpdate
from models import Post, SessionDep, Tag
from exceptions import CategoryNotFoundException, PostNotFoundException
from service.calculators import ReadTimeCalculatorDep
from tasks.post_email import send_email


class PostService:

    def __init__(
        self,
        uow: SessionDep,
        category_queries: Annotated[
            CategoryQueries,
            Depends(CategoryQueries),
        ],
        category_repository: Annotated[
            CategoryRepository,
            Depends(CategoryRepository),
        ],
        post_queries: Annotated[
            PostQueries,
            Depends(PostQueries),
        ],
        post_repository: Annotated[
            PostRepository,
            Depends(PostRepository),
        ],
        tag_queries: Annotated[
            TagQueries,
            Depends(TagQueries),
        ],
        tag_repository: Annotated[
            TagRepository,
            Depends(TagRepository),
        ],
        read_time_calculator: ReadTimeCalculatorDep,
    ):
        self.uow = uow
        self.category_queries = category_queries
        self.category_repository = category_repository
        self.post_queries = post_queries
        self.post_repository = post_repository
        self.tag_queries = tag_queries
        self.tag_repository = tag_repository
        self.read_time_calculator = read_time_calculator

    async def create(self, post_create: PostCreate) -> int:
        category = await self.category_queries.get_one(post_create.category_id)

        if not category:
            raise CategoryNotFoundException()

        tags = await self.resolve_tags(
            tag_ids=post_create.tag_ids, tag_names=post_create.tags
        )

        read_time = await self.read_time_calculator.calculate(post_create.description)

        post = Post(
            title=post_create.title,
            description=post_create.description,
            category=category,
            tags=tags,
            read_time=read_time,
        )
        self.post_repository.save(post)
        await self.uow.commit()

        await send_email.kiq(post_id=post.id)

        return post.id

    async def update(self, post_id: int, post_update: PostUpdate) -> int:
        post = await self.post_queries.get_one(post_id)
        if not post:
            raise PostNotFoundException()

        category = await self.category_queries.get_one(post_update.category_id)
        if not category:
            raise CategoryNotFoundException()

        tags = await self.resolve_tags(
            tag_ids=post_update.tag_ids, tag_names=post_update.tags
        )

        post.title = post_update.title
        post.description = post_update.description
        post.category = category
        post.tags = tags
        await self.uow.commit()
        return post.id

    async def destroy(self, id: int) -> None:
        post = await self.post_queries.get_one(id)

        if not post:
            raise PostNotFoundException()

        await self.post_repository.delete(post)
        await self.uow.commit()

    """
    В идеале этот функционал следует вынести в отдельный доменный сервис или функцию,
    PostService должен сосредотачиваться на бизнес-логике постов, а не на сборке коллекций тегов.
    #
    Можно создать domain service (например, TagResolver) или чистую функцию,
    которая принимает на вход:
    - tag_ids: список запрашиваемых ID тегов
    - tag_names: список запрашиваемых названий тегов
    - tags_by_ids: коллекция Tag-объектов, полученных из репозитория методом get_many(tag_ids)
    - tags_by_names: коллекция Tag-объектов, полученных из репозитория методом get_many_by_names(tag_names)
    #
    Тогда доменная функция resolve_tags будет заниматься исключительно бизнес-логикой:
    объединением существующих тегов, устранением дубликатов, созданием новых Tag-объектов для отсутствующих названий
    и возвращением итогового списка уникальных тегов.
    """

    async def resolve_tags(self, tag_ids: list[int], tag_names: list[str]) -> list[Tag]:

        all_tags = []

        if tag_ids:
            tags_by_id = await self.tag_queries.get_many(tag_ids)
            all_tags.extend(tags_by_id)

        if tag_names:
            existing_tags_by_name = await self.tag_queries.get_many_by_names(tag_names)
            existing_tag_names = {tag.name for tag in existing_tags_by_name}

            all_tags.extend(existing_tags_by_name)

            new_tag_names = set(tag_names) - existing_tag_names
            for tag_name in new_tag_names:
                all_tags.append(Tag(name=tag_name))

        unique_tags_dict = {tag.id: tag for tag in all_tags if tag.id}
        unique_tags = list(unique_tags_dict.values())

        unique_tags.extend([tag for tag in all_tags if not tag.id])

        return unique_tags
