from pydantic import BaseModel, Field

class DepositSchema(BaseModel):
    date: str
    periods: int = Field(ge=1, le=60)
    amount: int = Field(ge=10000, le=3000000)
    rate: float = Field(ge=1.0, le=8.0)