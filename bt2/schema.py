from pydantic import BaseModel,Field,ConfigDict

class CreatePlan(BaseModel):
    plan_code: str = Field(...)
    plan_name: str = Field(...)
    device_quantity: int = Field(...)
    price: float = Field(...)

class Response(BaseModel):
    id:int
    plan_code: str 
    plan_name: str 
    device_quantity: int 
    price: float
    class config():
        model_config = ConfigDict(from_attributes=True)