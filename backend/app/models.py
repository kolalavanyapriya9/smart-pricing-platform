from sqlalchemy import (
    Column,
    String,
    DECIMAL,
    TIMESTAMP,
    text,
    Integer,
    ForeignKey,
    Date,
    DateTime,
    text
)

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Product(Base):
    __tablename__ = "Product"

    product_id = Column(String(30), primary_key=True)
    product_name = Column(String(150), nullable=False)
    category = Column(String(100), nullable=False)
    brand = Column(String(100), nullable=True)
    base_cost = Column(DECIMAL(10, 2), nullable=False)
    current_price = Column(DECIMAL(10, 2), nullable=False)
    minimum_margin = Column(DECIMAL(5, 2), nullable=False)
    maximum_price = Column(DECIMAL(10, 2), nullable=True)

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

from sqlalchemy import ForeignKey, Date


class CostRecord(Base):
    __tablename__ = "CostRecord"

    cost_id = Column(String(50), primary_key=True)

    product_id = Column(
        String(30),
        ForeignKey("Product.product_id"),
        nullable=False
    )

    cost_amount = Column(DECIMAL(10, 2), nullable=False)
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date, nullable=True)

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

from sqlalchemy import DateTime


class PriceHistory(Base):
    __tablename__ = "PriceHistory"

    price_id = Column(String(50), primary_key=True)

    product_id = Column(
        String(30),
        ForeignKey("Product.product_id"),
        nullable=False
    )

    selling_price = Column(DECIMAL(10, 2), nullable=False)
    effective_from = Column(DateTime, nullable=False)
    effective_to = Column(DateTime, nullable=True)
    change_reason = Column(String(255), nullable=False)

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

class CompetitorObservation(Base):
    __tablename__ = "CompetitorObservation"

    observation_id = Column(String(50), primary_key=True)

    product_id = Column(
        String(30),
        ForeignKey("Product.product_id"),
        nullable=False
    )

    competitor_name = Column(String(150), nullable=False)
    competitor_price = Column(DECIMAL(10, 2), nullable=False)
    observed_at = Column(DateTime, nullable=False)
    source_name = Column(String(150), nullable=True)

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

class InventorySnapshot(Base):
    __tablename__ = "InventorySnapshot"

    inventory_id = Column(String(50), primary_key=True)

    product_id = Column(
        String(30),
        ForeignKey("Product.product_id"),
        nullable=False
    )

    available_quantity = Column(Integer, nullable=False)
    reserved_quantity = Column(Integer, default=0)
    warehouse_location = Column(String(150), nullable=True)
    snapshot_at = Column(DateTime, nullable=False)

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

class Promotion(Base):
    __tablename__ = "Promotion"

    promotion_id = Column(String(50), primary_key=True)
    promotion_name = Column(String(150), nullable=False)
    promotion_type = Column(String(30), nullable=False)
    discount_type = Column(String(30), nullable=False)
    discount_value = Column(DECIMAL(10, 2), nullable=False)
    max_discount_amount = Column(DECIMAL(10, 2), nullable=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(String(30), default="DRAFT")

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

class PromotionRule(Base):
    __tablename__ = "PromotionRule"

    rule_id = Column(String(50), primary_key=True)

    promotion_id = Column(
        String(50),
        ForeignKey("Promotion.promotion_id"),
        nullable=False
    )

    rule_type = Column(String(50), nullable=False)
    rule_description = Column(String(255), nullable=True)
    rule_value = Column(String(255), nullable=True)
    is_active = Column(Integer, default=1)

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

class PromotionProduct(Base):
    __tablename__ = "PromotionProduct"
    promotion_id = Column(
        String(50),
        ForeignKey("Promotion.promotion_id"),
        primary_key=True
    )
    
    product_id = Column(
        String(30),
        ForeignKey("Product.product_id"),
        primary_key=True
    )

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

class Order(Base):
    __tablename__ = "Order"

    order_id = Column(String(50), primary_key=True)
    order_date = Column(DateTime, nullable=False)
    order_status = Column(String(30), nullable=False)

    total_amount = Column(DECIMAL(10, 2), nullable=False)
    discount_amount = Column(DECIMAL(10, 2), default=0)
    final_amount = Column(DECIMAL(10, 2), nullable=False)

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

class PriceDecision(Base):
    __tablename__ = "PriceDecision"

    decision_id = Column(String(50), primary_key=True)

    product_id = Column(
        String(30),
        ForeignKey("Product.product_id"),
        nullable=False
    )

    cost_id = Column(
        String(50),
        ForeignKey("CostRecord.cost_id"),
        nullable=True
    )

    observation_id = Column(
        String(50),
        ForeignKey("CompetitorObservation.observation_id"),
        nullable=True
    )

    inventory_id = Column(
        String(50),
        ForeignKey("InventorySnapshot.inventory_id"),
        nullable=True
    )

    promotion_id = Column(
        String(50),
        ForeignKey("Promotion.promotion_id"),
        nullable=True
    )

    current_price = Column(DECIMAL(10, 2), nullable=False)
    recommended_price = Column(DECIMAL(10, 2), nullable=False)
    final_customer_price = Column(DECIMAL(10, 2), nullable=False)
    expected_margin_percent = Column(DECIMAL(5, 2), nullable=False)

    decision_status = Column(String(30), nullable=False)
    decision_reason = Column(String(255), nullable=False)
    decided_at = Column(DateTime, nullable=False)

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )