from typing import Any


class AppException(Exception):

    status_code: int = 500
    code: str = "internal_error"
    message: str = "Внутренняя ошибка сервера"

    def __init__(
        self,
        message: str | None = None,
        *,
        code: str | None = None,
        extra: dict[str, Any] | None = None,
    ):
        if message:
            self.message = message
        if code:
            self.code = code
        self.extra = extra or {}

    def to_dict(self) -> dict[str, Any]:
        data = {
            "error": {
                "code": self.code,
                "message": self.message,
            }
        }
        if self.extra:
            data["error"]["extra"] = self.extra
        return data


class DependencyException(AppException):
    status_code = 400
    code = "dependency_exists"
    message = "Невозможно удалить объект, так как существуют зависимые объекты"


class NotFoundException(AppException):
    status_code = 404
    code = "not_found"
    message = "Объект не найден"


class PostNotFoundException(NotFoundException):
    message = "Пост не найден"


class CategoryNotFoundException(NotFoundException):
    message = "Категория не найдена"


class CategoryHasPostsException(DependencyException):
    message = "Категория не может быть удалена, так как существуют зависимые посты"


class TagNotFoundException(NotFoundException):
    message = "Некоторые теги не найдены"

    def __init__(self, missing_tag_ids: list[int]):
        super().__init__(
            extra={"missing_tag_ids": missing_tag_ids},
        )
