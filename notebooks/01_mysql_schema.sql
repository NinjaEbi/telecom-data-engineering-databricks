-- =====================================================
-- TELECOM OLTP DATABASE SCHEMA (MySQL)
-- Group 8 - Telecom Data Engineering Project
-- =====================================================

CREATE DATABASE IF NOT EXISTS telecom_oltp;
USE telecom_oltp;

-- =====================================================
-- CUSTOMER MANAGEMENT
-- =====================================================

CREATE TABLE customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10),
    email VARCHAR(100) UNIQUE NOT NULL,
    registration_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    customer_status VARCHAR(20) DEFAULT 'ACTIVE',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CHECK (customer_status IN ('ACTIVE', 'INACTIVE', 'SUSPENDED'))
);

CREATE TABLE customer_addresses (
    address_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id VARCHAR(20) NOT NULL,
    address_type VARCHAR(20) NOT NULL,
    street_address VARCHAR(200) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    postal_code VARCHAR(10) NOT NULL,
    country VARCHAR(50) NOT NULL DEFAULT 'USA',
    is_primary BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    CHECK (address_type IN ('HOME', 'WORK', 'BILLING'))
);

CREATE TABLE customer_contacts (
    contact_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id VARCHAR(20) NOT NULL,
    contact_type VARCHAR(20) NOT NULL,
    contact_value VARCHAR(100) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    CHECK (contact_type IN ('PHONE', 'EMAIL', 'ALTERNATE_PHONE'))
);

-- =====================================================
-- MOBILE PLAN MANAGEMENT
-- =====================================================

CREATE TABLE mobile_plans (
    plan_id VARCHAR(20) PRIMARY KEY,
    plan_name VARCHAR(100) NOT NULL,
    plan_type VARCHAR(20) NOT NULL,
    monthly_charge DECIMAL(10, 2) NOT NULL,
    plan_status VARCHAR(20) DEFAULT 'ACTIVE',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CHECK (plan_type IN ('PREPAID', 'POSTPAID')),
    CHECK (plan_status IN ('ACTIVE', 'INACTIVE', 'DISCONTINUED')),
    CHECK (monthly_charge >= 0)
);

CREATE TABLE service_types (
    service_id VARCHAR(20) PRIMARY KEY,
    service_name VARCHAR(50) NOT NULL,
    service_category VARCHAR(30) NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CHECK (service_category IN ('VOICE', 'SMS', 'DATA', 'VALUE_ADDED'))
);

CREATE TABLE plan_services (
    plan_service_id INT PRIMARY KEY AUTO_INCREMENT,
    plan_id VARCHAR(20) NOT NULL,
    service_id VARCHAR(20) NOT NULL,
    service_limit VARCHAR(50),
    overage_charge DECIMAL(10, 4),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (plan_id) REFERENCES mobile_plans(plan_id),
    FOREIGN KEY (service_id) REFERENCES service_types(service_id),
    UNIQUE KEY unique_plan_service (plan_id, service_id)
);

-- =====================================================
-- SUBSCRIPTION MANAGEMENT
-- =====================================================

CREATE TABLE subscriptions (
    subscription_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    plan_id VARCHAR(20) NOT NULL,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    subscription_status VARCHAR(20) DEFAULT 'ACTIVE',
    activation_date DATETIME NOT NULL,
    deactivation_date DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (plan_id) REFERENCES mobile_plans(plan_id),
    CHECK (subscription_status IN ('ACTIVE', 'SUSPENDED', 'CANCELLED', 'PENDING')),
    CHECK (deactivation_date IS NULL OR deactivation_date >= activation_date)
);

CREATE TABLE subscription_services (
    subscription_service_id INT PRIMARY KEY AUTO_INCREMENT,
    subscription_id VARCHAR(20) NOT NULL,
    service_id VARCHAR(20) NOT NULL,
    service_status VARCHAR(20) DEFAULT 'ACTIVE',
    activation_date DATETIME NOT NULL,
    deactivation_date DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subscription_id) REFERENCES subscriptions(subscription_id),
    FOREIGN KEY (service_id) REFERENCES service_types(service_id),
    CHECK (service_status IN ('ACTIVE', 'INACTIVE'))
);

-- =====================================================
-- USAGE MANAGEMENT
-- =====================================================

CREATE TABLE call_records (
    call_id VARCHAR(30) PRIMARY KEY,
    subscription_id VARCHAR(20) NOT NULL,
    call_type VARCHAR(20) NOT NULL,
    call_direction VARCHAR(10) NOT NULL,
    destination_number VARCHAR(20),
    call_start_time DATETIME NOT NULL,
    call_end_time DATETIME NOT NULL,
    call_duration_seconds INT NOT NULL,
    call_charges DECIMAL(10, 4),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subscription_id) REFERENCES subscriptions(subscription_id),
    CHECK (call_type IN ('LOCAL', 'STD', 'ISD', 'ROAMING')),
    CHECK (call_direction IN ('INCOMING', 'OUTGOING')),
    CHECK (call_duration_seconds >= 0),
    CHECK (call_end_time >= call_start_time)
);

CREATE TABLE sms_records (
    sms_id VARCHAR(30) PRIMARY KEY,
    subscription_id VARCHAR(20) NOT NULL,
    sms_type VARCHAR(20) NOT NULL,
    sms_direction VARCHAR(10) NOT NULL,
    destination_number VARCHAR(20),
    sms_timestamp DATETIME NOT NULL,
    sms_count INT DEFAULT 1,
    sms_charges DECIMAL(10, 4),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subscription_id) REFERENCES subscriptions(subscription_id),
    CHECK (sms_type IN ('STANDARD', 'PROMOTIONAL', 'INTERNATIONAL')),
    CHECK (sms_direction IN ('INCOMING', 'OUTGOING')),
    CHECK (sms_count > 0)
);

CREATE TABLE data_usage (
    usage_id VARCHAR(30) PRIMARY KEY,
    subscription_id VARCHAR(20) NOT NULL,
    usage_date DATE NOT NULL,
    usage_start_time DATETIME NOT NULL,
    usage_end_time DATETIME NOT NULL,
    data_consumed_mb DECIMAL(15, 4) NOT NULL,
    data_charges DECIMAL(10, 4),
    network_type VARCHAR(10),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subscription_id) REFERENCES subscriptions(subscription_id),
    CHECK (data_consumed_mb >= 0),
    CHECK (network_type IN ('2G', '3G', '4G', '5G')),
    CHECK (usage_end_time >= usage_start_time)
);

-- =====================================================
-- BILLING MANAGEMENT
-- =====================================================

CREATE TABLE bills (
    bill_id VARCHAR(30) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    subscription_id VARCHAR(20) NOT NULL,
    bill_date DATE NOT NULL,
    billing_period_start DATE NOT NULL,
    billing_period_end DATE NOT NULL,
    total_amount DECIMAL(12, 2) NOT NULL,
    tax_amount DECIMAL(10, 2),
    discount_amount DECIMAL(10, 2) DEFAULT 0,
    net_amount DECIMAL(12, 2) NOT NULL,
    due_date DATE NOT NULL,
    bill_status VARCHAR(20) DEFAULT 'UNPAID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (subscription_id) REFERENCES subscriptions(subscription_id),
    CHECK (bill_status IN ('UNPAID', 'PAID', 'PARTIAL', 'OVERDUE')),
    CHECK (total_amount >= 0),
    CHECK (net_amount >= 0),
    CHECK (billing_period_end >= billing_period_start)
);

CREATE TABLE bill_items (
    bill_item_id INT PRIMARY KEY AUTO_INCREMENT,
    bill_id VARCHAR(30) NOT NULL,
    item_type VARCHAR(30) NOT NULL,
    description VARCHAR(200),
    quantity DECIMAL(10, 2),
    unit_price DECIMAL(10, 4),
    amount DECIMAL(10, 2) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bill_id) REFERENCES bills(bill_id),
    CHECK (item_type IN ('MONTHLY_CHARGE', 'CALL_CHARGES', 'SMS_CHARGES', 'DATA_CHARGES', 'OTHER')),
    CHECK (amount >= 0)
);

CREATE TABLE payments (
    payment_id VARCHAR(30) PRIMARY KEY,
    bill_id VARCHAR(30) NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
    payment_date DATETIME NOT NULL,
    payment_amount DECIMAL(12, 2) NOT NULL,
    payment_method VARCHAR(20) NOT NULL,
    payment_status VARCHAR(20) DEFAULT 'SUCCESS',
    transaction_reference VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bill_id) REFERENCES bills(bill_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    CHECK (payment_method IN ('CREDIT_CARD', 'DEBIT_CARD', 'NET_BANKING', 'UPI', 'WALLET', 'CASH')),
    CHECK (payment_status IN ('SUCCESS', 'FAILED', 'PENDING', 'REFUNDED')),
    CHECK (payment_amount > 0)
);

-- =====================================================
-- COMPLAINT MANAGEMENT
-- =====================================================

CREATE TABLE complaint_categories (
    category_id VARCHAR(20) PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE complaints (
    complaint_id VARCHAR(30) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    subscription_id VARCHAR(20),
    category_id VARCHAR(20) NOT NULL,
    complaint_date DATETIME NOT NULL,
    complaint_description TEXT NOT NULL,
    complaint_status VARCHAR(20) DEFAULT 'OPEN',
    priority VARCHAR(10) DEFAULT 'MEDIUM',
    resolution_date DATETIME,
    resolution_notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (subscription_id) REFERENCES subscriptions(subscription_id),
    FOREIGN KEY (category_id) REFERENCES complaint_categories(category_id),
    CHECK (complaint_status IN ('OPEN', 'IN_PROGRESS', 'RESOLVED', 'CLOSED', 'ESCALATED')),
    CHECK (priority IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL'))
);

-- =====================================================
-- NETWORK / SERVICE AREAS
-- =====================================================

CREATE TABLE service_areas (
    area_id VARCHAR(20) PRIMARY KEY,
    area_name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    region VARCHAR(50),
    network_coverage VARCHAR(10),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CHECK (network_coverage IN ('2G', '3G', '4G', '5G'))
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

CREATE INDEX idx_customer_email ON customers(email);
CREATE INDEX idx_customer_status ON customers(customer_status);
CREATE INDEX idx_subscription_customer ON subscriptions(customer_id);
CREATE INDEX idx_subscription_plan ON subscriptions(plan_id);
CREATE INDEX idx_subscription_status ON subscriptions(subscription_status);
CREATE INDEX idx_call_subscription ON call_records(subscription_id);
CREATE INDEX idx_call_start_time ON call_records(call_start_time);
CREATE INDEX idx_sms_subscription ON sms_records(subscription_id);
CREATE INDEX idx_sms_timestamp ON sms_records(sms_timestamp);
CREATE INDEX idx_data_subscription ON data_usage(subscription_id);
CREATE INDEX idx_data_date ON data_usage(usage_date);
CREATE INDEX idx_bill_customer ON bills(customer_id);
CREATE INDEX idx_bill_date ON bills(bill_date);
CREATE INDEX idx_bill_status ON bills(bill_status);
CREATE INDEX idx_payment_bill ON payments(bill_id);
CREATE INDEX idx_payment_date ON payments(payment_date);
CREATE INDEX idx_complaint_customer ON complaints(customer_id);
CREATE INDEX idx_complaint_status ON complaints(complaint_status);