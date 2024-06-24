import logging
from fastapi import APIRouter, HTTPException
from models import Order, OrderIn
from db import db, orders
from typing import List
from werkzeug.security import generate_password_hash


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter()


@router.get("/orders/", response_model=List[Order])
async def get_orders():
    query = orders.select()
    return await db.fetch_all(query)


@router.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    existing_order = await db.fetch_one(query)
    if existing_order:
        query = orders.select().where(orders.c.id == order_id)
        return await db.fetch_one(query)
    raise HTTPException(status_code=404, detail="Order not found")


@router.post("/orders/", response_model=Order)
async def create_order(order: OrderIn):
    query = orders.insert().values(**order.model_dump())
    last_id = await db.execute(query)
    logger.info(f"Order = {order} added")
    return {**order.model_dump(), "id": last_id}


@router.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, new_order: OrderIn):
    query = orders.select().where(orders.c.id == order_id)
    existing_order = await db.fetch_one(query)
    if existing_order:
        
        query = (
            orders.update()
            .where(orders.c.id == order_id)
            .values(**new_order.model_dump())
        )
        await db.execute(query)
        logger.info(f"Order id={order_id} changed")
        return {**new_order.model_dump(), "id": order_id}
    raise HTTPException(status_code=404, detail="Order not found")


@router.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    existing_order = await db.fetch_one(query)
    if existing_order:
        query = orders.delete().where(orders.c.id == order_id)
        await db.execute(query)
        logger.info(f"Order id={order_id} deleted")
        return {"message": "Order deleted"}
    raise HTTPException(status_code=404, detail="Order not found")
