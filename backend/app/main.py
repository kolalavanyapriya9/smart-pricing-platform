
from fastapi import FastAPI

app = FastAPI(
    title="Smart Pricing and Promotion Optimization Platform",
    description=(
        "A platform that simulates product pricing using "
        "demand, inventory, competitor prices and margin constraints."
    ),
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "project": "Smart Pricing Platform",
        "message": "Backend API is running successfully",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "FastAPI Backend"
    }

from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

@app.get("/db-check")
def database_check(db: Session = Depends(get_db)):
    from sqlalchemy import text

    result = db.execute(text("SELECT DATABASE()")).scalar()

    return {
        "status": "success",
        "connected_database": result,
        "message": "FastAPI is connected to MySQL"
    }

from app.models import Product


@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()

    return [
        {
            "product_id": product.product_id,
            "product_name": product.product_name,
            "category": product.category,
            "brand": product.brand,
            "base_cost": float(product.base_cost),
            "current_price": float(product.current_price),
            "minimum_margin": float(product.minimum_margin),
            "maximum_price": (
                float(product.maximum_price)
                if product.maximum_price is not None
                else None
            )
        }
        for product in products
    ]

from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    product_id: str
    product_name: str
    category: str
    brand: str | None = None
    base_cost: float = Field(gt=0)
    current_price: float = Field(gt=0)
    minimum_margin: float = Field(ge=0, lt=100)
    maximum_price: float | None = None

@app.post("/products")
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db)
):
    new_product = Product(
        product_id=product_data.product_id,
        product_name=product_data.product_name,
        category=product_data.category,
        brand=product_data.brand,
        base_cost=product_data.base_cost,
        current_price=product_data.current_price,
        minimum_margin=product_data.minimum_margin,
        maximum_price=product_data.maximum_price
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "message": "Product created successfully",
        "product_id": new_product.product_id
    }

@app.get("/products/{product_id}")
def get_product(
    product_id: str,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.product_id == product_id
    ).first()

    if product is None:
        return {
            "status": "error",
            "message": "Product not found"
        }

    return {
        "product_id": product.product_id,
        "product_name": product.product_name,
        "category": product.category,
        "brand": product.brand,
        "base_cost": float(product.base_cost),
        "current_price": float(product.current_price),
        "minimum_margin": float(product.minimum_margin),
        "maximum_price": (
            float(product.maximum_price)
            if product.maximum_price is not None
            else None
        )
    }

@app.put("/products/{product_id}")
def update_product(
    product_id: str,
    product_data: ProductCreate,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.product_id == product_id
    ).first()

    if product is None:
        return {
            "status": "error",
            "message": "Product not found"
        }

    product.product_name = product_data.product_name
    product.category = product_data.category
    product.brand = product_data.brand
    product.base_cost = product_data.base_cost
    product.current_price = product_data.current_price
    product.minimum_margin = product_data.minimum_margin
    product.maximum_price = product_data.maximum_price

    db.commit()
    db.refresh(product)

    return {
        "message": "Product updated successfully",
        "product_id": product.product_id
    }

