# Telecom Data Engineering & Analytics Platform

An end-to-end Telecom Data Engineering and Analytics project built using Databricks. The project implements the Medallion Architecture (Bronze, Silver, Gold), automated Data Quality validation, dimensional modeling, Customer 360 analytics, rule-based churn risk analysis, analytical views, and an interactive Databricks dashboard.

## Project Overview

Telecom companies generate large volumes of data from customers, subscriptions, calls, SMS, mobile data usage, billing, payments, and customer complaints.

The objective of this project is to build a scalable data engineering platform that:

- Ingests raw telecom data
- Validates data quality
- Identifies and isolates invalid records
- Cleans and standardizes data
- Builds business-ready analytical datasets
- Implements a dimensional/star schema
- Creates a unified Customer 360 view
- Calculates customer churn risk
- Provides executive-level business analytics
- Visualizes insights through a Databricks dashboard

The complete pipeline follows:

SOURCE DATA
    |
    v
DATA GENERATION
    |
    v
BRONZE LAYER
    |
    v
DATA QUALITY
    |
    v
SILVER LAYER
    |
    v
GOLD LAYER
    |
    +------------------+
    |                  |
    v                  v
STAR SCHEMA       CUSTOMER 360
    |                  |
    +--------+---------+
             |
             v
     ANALYTICAL VIEWS
             |
             v
         DASHBOARD

## Architecture

The project uses the Medallion Architecture.

### Bronze Layer

The Bronze layer stores the ingested source data with minimal transformation.

Schema:

`telecom.bronze`

The Bronze layer contains 17 telecom source tables:

1. customers
2. customer_addresses
3. customer_contacts
4. mobile_plans
5. service_types
6. plan_services
7. subscriptions
8. subscription_services
9. call_records
10. sms_records
11. data_usage
12. bills
13. bill_items
14. payments
15. complaint_categories
16. complaints
17. service_areas

## Data Quality Layer

A dedicated Data Quality framework was implemented before Silver transformation.

Schema:

`telecom.quality`

Audit tables:

`telecom.quality.dq_results`

`telecom.quality.rejected_records`

### Data Quality Checks

The project implements the following validation categories:

1. NULL checks
2. Primary key duplicate checks
3. Range checks
4. Date consistency checks
5. Foreign key checks

### NULL Checks

Required columns were checked for missing values.

Examples:

- customer_id
- subscription_id
- bill_id
- payment_id
- call_id
- amount
- quantity
- unit_price
- payment_amount

All validated NULL checks passed.

### Primary Key Duplicate Checks

Primary keys were checked for duplicate records across all source tables.

Result:

Duplicate records: 0

Examples:

customers: 1,000 records, 0 duplicates

subscriptions: 1,242 records, 0 duplicates

call_records: 50,000 records, 0 duplicates

sms_records: 100,000 records, 0 duplicates

data_usage: 75,000 records, 0 duplicates

### Range Checks

Business rules were applied to numeric columns.

Examples:

- amount >= 0
- quantity > 0
- unit_price >= 0
- monthly_charge >= 0
- payment_amount > 0
- data_consumed_mb >= 0
- call_duration_seconds >= 0
- sms_count > 0

All validated range rules passed.

### Date Consistency Checks

Temporal relationships were validated.

Examples:

- bill_date >= billing_period_start
- billing_period_end >= billing_period_start
- due_date >= bill_date
- call_end_time >= call_start_time
- resolution_date >= complaint_date
- usage_end_time >= usage_start_time
- payment_date >= bill_date
- deactivation_date >= activation_date

All validated date rules passed.

### Foreign Key Checks

Referential integrity was validated between parent and child tables.

Examples:

bill_items.bill_id -> bills.bill_id

bills.customer_id -> customers.customer_id

bills.subscription_id -> subscriptions.subscription_id

subscriptions.customer_id -> customers.customer_id

subscriptions.plan_id -> mobile_plans.plan_id

call_records.subscription_id -> subscriptions.subscription_id

data_usage.subscription_id -> subscriptions.subscription_id

payments.bill_id -> bills.bill_id

payments.customer_id -> customers.customer_id

complaints.customer_id -> customers.customer_id

complaints.category_id -> complaint_categories.category_id

All validated foreign key relationships passed.

## Rejected Records

Invalid records are captured separately for auditing instead of being silently deleted.

Example rejection reasons include:

- Negative call duration
- Call end time before start time
- Invalid subscription reference
- Unknown data quality failure

Example rejected records:

DQ_BAD_001 - Negative call duration

DQ_BAD_002 - Invalid subscription reference

DQ_BAD_003 - Negative call duration

This provides traceability and makes the pipeline auditable.

## Silver Layer

The Silver layer contains cleaned, validated, and standardized telecom data.

Schema:

`telecom.silver`

The Silver layer contains 17 tables:

- customers
- customer_addresses
- customer_contacts
- mobile_plans
- service_types
- plan_services
- subscriptions
- subscription_services
- call_records
- sms_records
- data_usage
- bills
- bill_items
- payments
- complaint_categories
- complaints
- service_areas

Silver validation result:

Expected tables: 17

Passed tables: 17

Result: 17/17 tables passed validation.

## Gold Layer

The Gold layer contains business-ready analytical datasets.

Schema:

`telecom.gold`

The Gold layer follows a dimensional/star-schema design.

## Dimension Tables

### dim_date

1,095 records

Provides date-based analysis.

### dim_customer

1,000 records

Contains customer-level attributes.

### dim_plan

5 records

Contains mobile plan information.

### dim_service

10 records

Contains telecom service information.

### dim_subscription

1,242 records

Contains subscription information.

### dim_service_area

50 records

Contains service-area information.

## Fact Tables

### fact_call_usage

50,000 records

Stores call usage metrics.

### fact_sms_usage

100,000 records

Stores SMS usage metrics.

### fact_data_usage

75,000 records

Stores mobile data usage metrics.

### fact_billing

5,039 records

Stores billing transactions.

### fact_payments

4,074 records

Stores payment transactions.

### fact_complaints

500 records

Stores customer complaint information.

## Gold Validation

Expected tables: 12

Passed tables: 12

Result: 12/12 Gold tables passed validation.

## Customer 360

A unified customer-level analytical dataset was created:

`telecom.gold.customer_360`

Records:

1,000 customers

Customer 360 combines information from:

- Customer profile
- Subscriptions
- Plans
- Calls
- SMS
- Data usage
- Billing
- Payments
- Complaints
- Churn risk

### Customer 360 Metrics

The Customer 360 dataset contains:

- customer_id
- customer_name
- age
- gender
- customer_status
- current_plan
- current_plan_type
- total_subscriptions
- active_subscriptions
- cancelled_subscriptions
- total_calls
- total_call_minutes
- total_sms
- total_data_gb
- total_billed_amount
- total_successful_payments
- outstanding_amount
- total_payments
- successful_payment_count
- failed_payments
- payment_success_rate
- total_complaints
- resolved_complaints
- high_priority_complaints
- complaint_resolution_rate
- churn_risk_score
- churn_risk_level
- customer_tenure_days
- customer_tenure_years

### Customer 360 Validation

Total customers: 1,000

Duplicate customers: 0

Null customer IDs: 0

Negative outstanding amounts: 0

Invalid risk levels: 0

Result: Customer 360 validation passed.

## Churn Risk Analysis

A rule-based churn risk scoring framework was implemented.

The scoring framework considers customer behavior and account indicators such as:

- Cancelled subscriptions
- Outstanding balances
- Failed payments
- Payment success rate
- Customer complaints
- High-priority complaints
- Subscription activity

Customers are categorized into:

- LOW
- MEDIUM
- HIGH

Current distribution:

HIGH: 11 customers

MEDIUM: 222 customers

LOW: 767 customers

Total: 1,000 customers

The current churn score is a business-rule-based analytical score and is not a machine-learning prediction model.

## Analytical Views

The Gold layer provides business-focused analytical views.

### Executive KPIs

`vw_executive_kpis`

Provides:

- Total customers
- Active subscriptions
- Total billed revenue
- Total collected revenue
- Outstanding amount
- Total calls
- Total call minutes
- Total SMS
- Total data usage
- Total complaints
- High-risk customers

### Revenue Analysis

`vw_revenue_analysis`

Provides:

- Monthly bills
- Gross billed amount
- Tax
- Discounts
- Net billed amount
- Paid bills
- Unpaid bills
- Overdue bills

### Usage Analysis

`vw_usage_analysis`

Provides:

- Total calls
- Call minutes
- Call charges
- SMS
- SMS charges
- Data usage
- Data charges
- Total usage charges

### Plan Performance

`vw_plan_performance`

Provides:

- Subscription counts
- Active subscriptions
- Cancelled subscriptions
- Bills
- Revenue
- Calls
- Call minutes
- Data usage

### Complaint Analysis

`vw_complaint_analysis`

Provides:

- Total complaints
- Open complaints
- In-progress complaints
- Resolved complaints
- High-priority complaints
- Critical complaints
- Average resolution time

### Churn Risk

`vw_churn_risk`

Provides customer-level churn risk information.

## Key Business Results

| Metric | Value |
|---|---:|
| Total Customers | 1,000 |
| Active Subscriptions | 1,071 |
| Total Billed Revenue | 6,141,891.90 |
| Total Collected Revenue | 4,353,523.52 |
| Outstanding Amount | 1,788,368.38 |
| Total Calls | 50,000 |
| Total Call Minutes | 1,506,569.85 |
| Total SMS | 100,000 |
| Total Data Usage (GB) | 38,182.53 |
| Total Complaints | 500 |
| High-Risk Customers | 11 |
| Medium-Risk Customers | 222 |
| Low-Risk Customers | 767 |

## Monthly Revenue Analysis

The project contains billing data across 2026.

| Month | Total Bills | Net Billed Amount |
|---|---:|---:|
| March | 255 | 299,770.89 |
| April | 549 | 665,286.27 |
| May | 863 | 1,050,331.76 |
| June | 1,124 | 1,375,258.52 |
| July | 1,124 | 1,377,664.24 |
| August | 1,124 | 1,373,580.22 |

This allows the business to analyze revenue growth and billing trends over time.

## Usage Analytics

Monthly telecom usage is analyzed across three major areas.

### Voice

- Total calls
- Call minutes
- Call charges

### SMS

- SMS count
- SMS charges

### Data

- Data GB
- Data charges

This allows telecom operators to understand customer consumption patterns and usage-driven revenue.

## Plan Performance

The project analyzes performance across five plans:

- PLAN001 - Basic
- PLAN002 - Standard
- PLAN003 - Premium
- PLAN004 - Unlimited
- PLAN005 - Family Pack

Metrics include:

- Total subscriptions
- Active subscriptions
- Cancelled subscriptions
- Bills
- Revenue
- Calls
- Call minutes
- Data usage

This enables comparison of plan popularity and revenue contribution.

## Complaint Analytics

The project contains 500 complaints.

Complaint categories include:

- Billing Issue
- Network Issue
- Service Quality
- Data Speed
- Customer Service
- Plan Change
- Device Issue

The dashboard analyzes:

- Complaint volume
- Complaint status
- High-priority complaints
- Critical complaints
- Average resolution time

## Databricks Dashboard

An interactive dashboard was created using the Gold analytical views.

Dashboard name:

Telecom Customer & Revenue Analytics Dashboard

The dashboard contains the following sections.

### Executive Overview

- Total Customers
- Active Subscriptions
- Total Revenue
- Collected Revenue
- Outstanding Amount
- Total Complaints
- High-Risk Customers

### Revenue and Billing

- Monthly Revenue Trend
- Billing Status
- Revenue by Plan

### Usage Analytics

- Monthly Call Minutes
- Monthly SMS Usage
- Monthly Data Usage

### Customer and Churn

- Churn Risk Distribution
- Outstanding Amount by Risk Level
- High-Risk Customer Table

### Service Quality

- Complaints by Category
- Complaint Resolution Status
- Average Resolution Time

## Technology Stack

| Technology | Purpose |
|---|---|
| Databricks | Data engineering and analytics platform |
| Apache Spark | Distributed data processing |
| PySpark | Data transformation |
| Spark SQL | Analytical queries |
| Delta Lake | Reliable data storage |
| Python | Data generation and transformation |
| SQL | Data quality and analytics |
| Databricks SQL | Dashboard and visualization |
| GitHub | Version control |

## Repository Structure

```text
telecom-data-engineering-databricks/
│
├── README.md
│
└── notebooks/
    ├── 01_mysql_schema.sql
    ├── 02_Data_Generation.py
    ├── 03_Bronze_Ingestion.ipynb
    ├── 04_Data_Quality.ipynb
    ├── 05_Silver_Transformation.ipynb
    ├── 06_Gold_Analytics.ipynb
    └── 07_Dashboard_Analytics.ipynb

End-to-End Pipeline

01 MySQL Schema
      |
      v
02 Data Generation
      |
      v
03 Bronze Ingestion
      |
      v
04 Data Quality
      |
      v
05 Silver Transformation
      |
      v
06 Gold Analytics
      |
      v
Customer 360
      |
      v
07 Dashboard Analytics
      |
      v
Databricks Dashboard



Validation Summary

The project includes validation at multiple stages.

BRONZE
17 source tables
        |
        v
DATA QUALITY
NULL checks       PASS
PK checks         PASS
Range checks      PASS
Date checks       PASS
FK checks         PASS
        |
        v
SILVER
17 / 17 tables PASS
        |
        v
GOLD
12 / 12 tables PASS
        |
        v
CUSTOMER 360
1,000 / 1,000 validated
        |
        v
DASHBOARD
Business analytics available
Data and Security

The project uses generated and synthetic telecom data for development and demonstration.

No production customer information, passwords, API keys, access tokens, or other credentials should be committed to this repository.

Sensitive credentials should be managed through secure secret-management mechanisms rather than source code.

Project Highlights
17 Bronze tables
17 Silver tables
12 Gold tables
6 Dimension tables
6 Fact tables
1 Customer 360 dataset
6 Analytical views
1,000 Customers
50,000 Call Records
100,000 SMS Records
75,000 Data Usage Records
5,039 Bills
4,074 Payment Records
500 Complaints
17/17 Silver Validation Passed
12/12 Gold Validation Passed
Customer 360 Validation Passed
Interactive Databricks Dashboard
Project Outcome

This project demonstrates a complete modern data engineering workflow from raw telecom data to business intelligence.

                    TELECOM DATA
                         |
                         v
                 DATA ENGINEERING
                         |
        +----------------+----------------+
        |                |                |
        v                v                v
    INGESTION       DATA QUALITY     TRANSFORMATION
        |                |                |
        +----------------+----------------+
                         |
                         v
                    SILVER DATA
                         |
                         v
                    GOLD MODEL
                         |
              +----------+----------+
              |                     |
              v                     v
        CUSTOMER 360           ANALYTICS
              |                     |
              +----------+----------+
                         |
                         v
                    DASHBOARD
                         |
                         v
                  BUSINESS INSIGHTS

The platform provides a foundation for scalable telecom analytics, customer intelligence, revenue analysis, usage monitoring, service-quality analysis, and future predictive analytics.
