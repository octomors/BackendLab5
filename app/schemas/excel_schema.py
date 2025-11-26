from pydantic import BaseModel, ConfigDict
from io import BytesIO


class ExcelExportResult(BaseModel):
    content: BytesIO
    filename: str

    # BytesIO is not a valid type for BaseModel, so we need to allow arbitrary types
    model_config = ConfigDict(arbitrary_types_allowed=True)
