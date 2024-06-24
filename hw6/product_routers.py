import logging
from fastapi import APIRouter, HTTPException
from models import Product, ProductIn
from db import db, products
from typing import List
from werkzeug.security import generate_password_hash


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter()


@router.get("/product/", response_model=List[Product])
async def get_products():
    query = products.select()
    return await db.fetch_all(query)


@router.get("/product/{product_id}", response_model=Product)
async def get_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    existing_product = await db.fetch_one(query)
    if existing_product:
        query = products.select().where(products.c.id == product_id)
        return await db.fetch_one(query)
    raise HTTPException(status_code=404, detail="Product not found")


@router.post("/product/", response_model=Product)
async def create_product(product: ProductIn):
    query = products.insert().values(**product.model_dump())
    last_id = await db.execute(query)
    logger.info(f"Product = {product} added")
    return {**product.model_dump(), "id": last_id}


@router.put("/product/{product_id}", response_model=Product)
async def update_product(product_id: int, new_product: ProductIn):
    query = products.select().where(products.c.id == product_id)
    existing_product = await db.fetch_one(query)
    if existing_product:
        
        query = (
            products.update()
            .where(products.c.id == product_id)
            .values(**new_product.model_dump())
        )
        await db.execute(query)
        logger.info(f"Product id={product_id} changed")
        return {**new_product.model_dump(), "id": product_id}
    raise HTTPException(status_code=404, detail="Product not found")


@router.delete("/product/{product_id}")
async def delete_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    existing_product = await db.fetch_one(query)
    if existing_product:
        query = products.delete().where(products.c.id == product_id)
        await db.execute(query)
        logger.info(f"Product id={product_id} deleted")
        return {"message": "Product deleted"}
    raise HTTPException(status_code=404, detail="Product not found")
