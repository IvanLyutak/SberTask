from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class DepositSchema(BaseModel):
    date: str
    periods: int = Field(ge=1, le=60)
    amount: int = Field(ge=10000, le=3000000)
    rate: float = Field(ge=1.0, le=8.0)

    @field_validator('date')
    def parse_date(cls, date):
        return datetime.strptime(date, "%d.%m.%Y").date()