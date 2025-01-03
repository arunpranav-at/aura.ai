from pydantic import BaseModel


class TestResults(BaseModel):
    totalPrompts: int
    TruePositives: int
    TrueNegatives: int
    FalsePositives: int
    FalseNegatives: int
