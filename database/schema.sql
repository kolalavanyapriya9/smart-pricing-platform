CREATE DATABASE IF NOT EXISTS smart_pricing_db;

USE smart_pricing_db;

CREATE TABLE IF NOT EXISTS Product (
    product_id VARCHAR(30) PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(100) NOT NULL,
    brand VARCHAR(100),
    base_cost DECIMAL(10,2) NOT NULL,
    current_price DECIMAL(10,2) NOT NULL,
    minimum_margin DECIMAL(5,2) NOT NULL,
    maximum_price DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS CostRecord (
    cost_id VARCHAR(50) PRIMARY KEY,
    product_id VARCHAR(30) NOT NULL,
    cost_amount DECIMAL(10,2) NOT NULL,
    effective_from DATE NOT NULL,
    effective_to DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_cost_product
        FOREIGN KEY (product_id)
        REFERENCES Product(product_id),

    CONSTRAINT chk_cost_positive
        CHECK (cost_amount > 0)
);

CREATE TABLE IF NOT EXISTS PriceHistory (
    price_id VARCHAR(50) PRIMARY KEY,
    product_id VARCHAR(30) NOT NULL,
    selling_price DECIMAL(10,2) NOT NULL,
    effective_from DATETIME NOT NULL,
    effective_to DATETIME,
    change_reason VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_price_product
        FOREIGN KEY (product_id)
        REFERENCES Product(product_id),

    CONSTRAINT chk_selling_price_positive
        CHECK (selling_price > 0)
);

CREATE TABLE IF NOT EXISTS CompetitorObservation (
    observation_id VARCHAR(50) PRIMARY KEY,
    product_id VARCHAR(30) NOT NULL,
    competitor_name VARCHAR(150) NOT NULL,
    competitor_price DECIMAL(10,2) NOT NULL,
    observed_at DATETIME NOT NULL,
    source_name VARCHAR(150),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_competitor_product
        FOREIGN KEY (product_id)
        REFERENCES Product(product_id),

    CONSTRAINT chk_competitor_price_positive
        CHECK (competitor_price > 0)
);

CREATE TABLE IF NOT EXISTS InventorySnapshot (
    inventory_id VARCHAR(50) PRIMARY KEY,
    product_id VARCHAR(30) NOT NULL,
    available_quantity INT NOT NULL,
    reserved_quantity INT DEFAULT 0,
    warehouse_location VARCHAR(150),
    snapshot_at DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_inventory_product
        FOREIGN KEY (product_id)
        REFERENCES Product(product_id),

    CONSTRAINT chk_available_quantity
        CHECK (available_quantity >= 0),

    CONSTRAINT chk_reserved_quantity
        CHECK (reserved_quantity >= 0)
);

CREATE TABLE IF NOT EXISTS Promotion (
    promotion_id VARCHAR(50) PRIMARY KEY,
    promotion_name VARCHAR(150) NOT NULL,
    promotion_type VARCHAR(30) NOT NULL,
    discount_type VARCHAR(20) NOT NULL,
    discount_value DECIMAL(10,2) NOT NULL,
    max_discount_amount DECIMAL(10,2),
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    status VARCHAR(20) DEFAULT 'DRAFT',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_promotion_type
        CHECK (promotion_type IN ('PRODUCT', 'CATEGORY', 'ORDER')),

    CONSTRAINT chk_discount_type
        CHECK (discount_type IN ('PERCENTAGE', 'FIXED')),

    CONSTRAINT chk_discount_value
        CHECK (discount_value > 0),

    CONSTRAINT chk_promotion_dates
        CHECK (end_date > start_date)
);

CREATE TABLE IF NOT EXISTS PromotionRule (
    rule_id VARCHAR(50) PRIMARY KEY,
    promotion_id VARCHAR(50) NOT NULL,
    rule_type VARCHAR(30) NOT NULL,
    rule_description VARCHAR(255) NOT NULL,
    rule_value VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_rule_promotion
        FOREIGN KEY (promotion_id)
        REFERENCES Promotion(promotion_id),

    CONSTRAINT chk_rule_type
        CHECK (rule_type IN (
            'STACKING',
            'EXCLUSION',
            'MIN_ORDER_VALUE',
            'CUSTOMER_LIMIT'
        ))
);

CREATE TABLE IF NOT EXISTS PromotionProduct (
    promotion_id VARCHAR(50) NOT NULL,
    product_id VARCHAR(30) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (promotion_id, product_id),

    CONSTRAINT fk_pp_promotion
        FOREIGN KEY (promotion_id)
        REFERENCES Promotion(promotion_id),

    CONSTRAINT fk_pp_product
        FOREIGN KEY (product_id)
        REFERENCES Product(product_id)
);

CREATE TABLE IF NOT EXISTS `Order` (
    order_id VARCHAR(50) PRIMARY KEY,
    order_date DATETIME NOT NULL,
    order_status VARCHAR(30) NOT NULL,
    total_amount DECIMAL(12,2) NOT NULL,
    discount_amount DECIMAL(12,2) DEFAULT 0,
    final_amount DECIMAL(12,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_order_status
        CHECK (order_status IN (
            'PLACED',
            'CONFIRMED',
            'SHIPPED',
            'DELIVERED',
            'CANCELLED',
            'RETURNED'
        )),

    CONSTRAINT chk_order_amounts
        CHECK (
            total_amount >= 0
            AND discount_amount >= 0
            AND final_amount >= 0
            AND final_amount <= total_amount
        )
);

CREATE TABLE IF NOT EXISTS PriceDecision (
    decision_id VARCHAR(50) PRIMARY KEY,
    product_id VARCHAR(30) NOT NULL,
    cost_id VARCHAR(50),
    observation_id VARCHAR(50),
    inventory_id VARCHAR(50),
    promotion_id VARCHAR(50),

    current_price DECIMAL(10,2) NOT NULL,
    recommended_price DECIMAL(10,2) NOT NULL,
    final_customer_price DECIMAL(10,2),
    expected_margin_percent DECIMAL(5,2),

    decision_status VARCHAR(30) NOT NULL,
    decision_reason VARCHAR(500) NOT NULL,
    decided_at DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_decision_product
        FOREIGN KEY (product_id)
        REFERENCES Product(product_id),

    CONSTRAINT fk_decision_cost
        FOREIGN KEY (cost_id)
        REFERENCES CostRecord(cost_id),

    CONSTRAINT fk_decision_competitor
        FOREIGN KEY (observation_id)
        REFERENCES CompetitorObservation(observation_id),

    CONSTRAINT fk_decision_inventory
        FOREIGN KEY (inventory_id)
        REFERENCES InventorySnapshot(inventory_id),

    CONSTRAINT fk_decision_promotion
        FOREIGN KEY (promotion_id)
        REFERENCES Promotion(promotion_id),

    CONSTRAINT chk_recommended_price
        CHECK (recommended_price > 0),

    CONSTRAINT chk_decision_status
        CHECK (decision_status IN (
            'APPROVED',
            'REJECTED',
            'PENDING'
        ))
);