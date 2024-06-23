from datetime import date
from pydantic import BaseModel, EmailStr, Field
from enum import Enum


class Status(str, Enum):
    available = "available"
    reserv = "reserv"
    sold = "sold"

class UserIn(BaseModel):
    name: str = Field(..., title="Name", min_length=2)
    surname: str = Field(..., title="surname", min_length=2)
    email: EmailStr = Field(..., title="Email", max_length=128)
    password: str = Field(..., title="Password", min_length=5)

class User(UserIn):
    id: int

class ProductIn(BaseModel):
    name: str = Field(..., title="Name Product", min_length=2)
    description: str = Field(title="Description Product")
    price: float = Field(..., title="Price")
    
class Product(ProductIn):
    id: int
    
class OrderIn(BaseModel):
    user_id: int = Field(..., title="User_ID")
    product_id: int = Field(..., title="Product_ID")
    order_date: date = Field(..., title="Day order", description="YYYY-MM-DD")
    status: Status = Field(..., title='Status', description="available-resrv-sold")

class Order(OrderIn):
    id: int