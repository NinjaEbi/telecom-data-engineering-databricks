# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# DBTITLE 1,Telecom Sample Data Generation
# MAGIC %md
# MAGIC # Telecom Sample Data Generation
# MAGIC
# MAGIC This notebook generates realistic sample data for the Telecom OLTP database.
# MAGIC
# MAGIC **Data to Generate:**
# MAGIC * 1,000 Customers
# MAGIC * 5 Mobile Plans
# MAGIC * 10 Service Types
# MAGIC * 1,500 Subscriptions
# MAGIC * 50,000 Call Records
# MAGIC * 100,000 SMS Records
# MAGIC * 75,000 Data Usage Records
# MAGIC * 5,000 Bills
# MAGIC * 6,000 Payments
# MAGIC * 500 Complaints
# MAGIC
# MAGIC **Output:** CSV files for each table that can be loaded into MySQL

# COMMAND ----------

# DBTITLE 1,Install Required Libraries
# Install Faker for generating realistic data
!pip install -q Faker

# COMMAND ----------

# DBTITLE 1,Import Libraries and Initialize
from faker import Faker
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import uuid

# Initialize Faker
fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)

print("Libraries imported successfully!")

# COMMAND ----------

# DBTITLE 1,Generate Customers
# Generate 1,000 customers
num_customers = 1000

customers = []
for i in range(1, num_customers + 1):
    customer_id = f"CUST{str(i).zfill(6)}"
    first_name = fake.first_name()
    last_name = fake.last_name()
    date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=75)
    gender = random.choice(['Male', 'Female', 'Other'])
    email = f"{first_name.lower()}.{last_name.lower()}{i}@{fake.free_email_domain()}"
    registration_date = fake.date_time_between(start_date='-3y', end_date='now')
    customer_status = random.choices(['ACTIVE', 'INACTIVE', 'SUSPENDED'], weights=[85, 10, 5])[0]
    
    customers.append({
        'customer_id': customer_id,
        'first_name': first_name,
        'last_name': last_name,
        'date_of_birth': date_of_birth,
        'gender': gender,
        'email': email,
        'registration_date': registration_date,
        'customer_status': customer_status,
        'created_at': registration_date,
        'updated_at': registration_date
    })

customers_df = pd.DataFrame(customers)
print(f"Generated {len(customers_df)} customers")
customers_df.head()

# COMMAND ----------

# DBTITLE 1,Generate Customer Addresses
# Generate addresses for customers (1-2 addresses per customer)
addresses = []
address_id = 1

for _, customer in customers_df.iterrows():
    num_addresses = random.choices([1, 2], weights=[70, 30])[0]
    
    for j in range(num_addresses):
        address_type = random.choice(['HOME', 'WORK', 'BILLING'])
        is_primary = True if j == 0 else False
        
        addresses.append({
            'address_id': address_id,
            'customer_id': customer['customer_id'],
            'address_type': address_type,
            'street_address': fake.street_address(),
            'city': fake.city(),
            'state': fake.state(),
            'postal_code': fake.postcode(),
            'country': 'USA',
            'is_primary': is_primary,
            'created_at': customer['created_at']
        })
        address_id += 1

addresses_df = pd.DataFrame(addresses)
print(f"Generated {len(addresses_df)} addresses")
addresses_df.head()

# COMMAND ----------

# DBTITLE 1,Generate Mobile Plans and Services
# Generate 5 mobile plans
plans = [
    {'plan_id': 'PLAN001', 'plan_name': 'Basic', 'plan_type': 'PREPAID', 'monthly_charge': 299.00},
    {'plan_id': 'PLAN002', 'plan_name': 'Standard', 'plan_type': 'POSTPAID', 'monthly_charge': 499.00},
    {'plan_id': 'PLAN003', 'plan_name': 'Premium', 'plan_type': 'POSTPAID', 'monthly_charge': 799.00},
    {'plan_id': 'PLAN004', 'plan_name': 'Unlimited', 'plan_type': 'POSTPAID', 'monthly_charge': 1199.00},
    {'plan_id': 'PLAN005', 'plan_name': 'Family Pack', 'plan_type': 'POSTPAID', 'monthly_charge': 1999.00}
]

for plan in plans:
    plan['plan_status'] = 'ACTIVE'
    plan['created_at'] = datetime.now() - timedelta(days=365)
    plan['updated_at'] = plan['created_at']

plans_df = pd.DataFrame(plans)
print(f"Generated {len(plans_df)} mobile plans")

# Generate service types
services = [
    {'service_id': 'SRV001', 'service_name': 'Local Calls', 'service_category': 'VOICE'},
    {'service_id': 'SRV002', 'service_name': 'STD Calls', 'service_category': 'VOICE'},
    {'service_id': 'SRV003', 'service_name': 'ISD Calls', 'service_category': 'VOICE'},
    {'service_id': 'SRV004', 'service_name': 'SMS', 'service_category': 'SMS'},
    {'service_id': 'SRV005', 'service_name': 'MMS', 'service_category': 'SMS'},
    {'service_id': 'SRV006', 'service_name': '4G Data', 'service_category': 'DATA'},
    {'service_id': 'SRV007', 'service_name': '5G Data', 'service_category': 'DATA'},
    {'service_id': 'SRV008', 'service_name': 'Roaming', 'service_category': 'VALUE_ADDED'},
    {'service_id': 'SRV009', 'service_name': 'Caller Tune', 'service_category': 'VALUE_ADDED'},
    {'service_id': 'SRV010', 'service_name': 'Voicemail', 'service_category': 'VALUE_ADDED'}
]

for service in services:
    service['description'] = f"{service['service_name']} service"
    service['created_at'] = datetime.now() - timedelta(days=365)

services_df = pd.DataFrame(services)
print(f"Generated {len(services_df)} service types")

plans_df.head()

# COMMAND ----------

# DBTITLE 1,Generate Plan Services Mapping
# Map services to plans
plan_services = []
ps_id = 1

plan_service_mappings = {
    'PLAN001': [('SRV001', 'UNLIMITED', 0), ('SRV004', '100 SMS', 0.10), ('SRV006', '2GB', 10)],
    'PLAN002': [('SRV001', 'UNLIMITED', 0), ('SRV002', '300 Min', 1.0), ('SRV004', 'UNLIMITED', 0), ('SRV006', '10GB', 5)],
    'PLAN003': [('SRV001', 'UNLIMITED', 0), ('SRV002', 'UNLIMITED', 0), ('SRV004', 'UNLIMITED', 0), ('SRV006', '50GB', 2), ('SRV007', '10GB', 5)],
    'PLAN004': [('SRV001', 'UNLIMITED', 0), ('SRV002', 'UNLIMITED', 0), ('SRV003', '100 Min', 5), ('SRV004', 'UNLIMITED', 0), ('SRV006', 'UNLIMITED', 0), ('SRV007', 'UNLIMITED', 0)],
    'PLAN005': [('SRV001', 'UNLIMITED', 0), ('SRV002', 'UNLIMITED', 0), ('SRV003', '200 Min', 3), ('SRV004', 'UNLIMITED', 0), ('SRV006', 'UNLIMITED', 0), ('SRV007', 'UNLIMITED', 0), ('SRV008', 'Yes', 0)]
}

for plan_id, services_list in plan_service_mappings.items():
    for service_id, limit, overage in services_list:
        plan_services.append({
            'plan_service_id': ps_id,
            'plan_id': plan_id,
            'service_id': service_id,
            'service_limit': limit,
            'overage_charge': overage,
            'created_at': datetime.now() - timedelta(days=365)
        })
        ps_id += 1

plan_services_df = pd.DataFrame(plan_services)
print(f"Generated {len(plan_services_df)} plan-service mappings")
plan_services_df.head()

# COMMAND ----------

# DBTITLE 1,Generate Subscriptions
# Generate subscriptions (1-2 per customer)
subscriptions = []
used_phone_numbers = set()

for _, customer in customers_df.iterrows():
    num_subscriptions = random.choices([1, 2], weights=[75, 25])[0]
    
    for j in range(num_subscriptions):
        sub_id = f"SUB{len(subscriptions) + 1:06d}"
        
        # Generate unique phone number
        while True:
            phone_number = f"+1{random.randint(2000000000, 9999999999)}"
            if phone_number not in used_phone_numbers:
                used_phone_numbers.add(phone_number)
                break
        
        plan_id = random.choice(plans_df['plan_id'].tolist())
        activation_date = customer['registration_date'] + timedelta(days=random.randint(0, 30))
        subscription_status = random.choices(
            ['ACTIVE', 'SUSPENDED', 'CANCELLED'], 
            weights=[85, 5, 10]
        )[0]
        
        deactivation_date = None
        if subscription_status == 'CANCELLED':
            deactivation_date = activation_date + timedelta(days=random.randint(30, 700))
        
        subscriptions.append({
            'subscription_id': sub_id,
            'customer_id': customer['customer_id'],
            'plan_id': plan_id,
            'phone_number': phone_number,
            'subscription_status': subscription_status,
            'activation_date': activation_date,
            'deactivation_date': deactivation_date,
            'created_at': activation_date,
            'updated_at': activation_date
        })

subscriptions_df = pd.DataFrame(subscriptions)
print(f"Generated {len(subscriptions_df)} subscriptions")
subscriptions_df.head()

# COMMAND ----------

# DBTITLE 1,Cell — customer contacts
# Generate customer contacts
contacts = []
contact_id = 1

for _, customer in customers_df.iterrows():

    # Primary phone
    contacts.append({
        'contact_id': contact_id,
        'customer_id': customer['customer_id'],
        'contact_type': 'PHONE',
        'contact_value': f"+1{random.randint(2000000000, 9999999999)}",
        'is_primary': True,
        'created_at': customer['created_at']
    })
    contact_id += 1

    # Primary email
    contacts.append({
        'contact_id': contact_id,
        'customer_id': customer['customer_id'],
        'contact_type': 'EMAIL',
        'contact_value': customer['email'],
        'is_primary': True,
        'created_at': customer['created_at']
    })
    contact_id += 1

customer_contacts_df = pd.DataFrame(contacts)

print(f"Generated {len(customer_contacts_df)} customer contacts")
customer_contacts_df.head()

# COMMAND ----------

# DBTITLE 1,Cell — subscription services
# Generate subscription services based on each subscription's plan
subscription_services = []
subscription_service_id = 1

for _, sub in subscriptions_df.iterrows():

    plan_services_for_plan = plan_services_df[
        plan_services_df['plan_id'] == sub['plan_id']
    ]

    for _, ps in plan_services_for_plan.iterrows():

        subscription_services.append({
            'subscription_service_id': subscription_service_id,
            'subscription_id': sub['subscription_id'],
            'service_id': ps['service_id'],
            'service_status': 'ACTIVE',
            'activation_date': sub['activation_date'],
            'deactivation_date': sub['deactivation_date'],
            'created_at': sub['activation_date']
        })

        subscription_service_id += 1

subscription_services_df = pd.DataFrame(subscription_services)

print(f"Generated {len(subscription_services_df)} subscription services")
subscription_services_df.head()

# COMMAND ----------

# DBTITLE 1,Generate Call Records
# Generate call records for active subscriptions
active_subs = subscriptions_df[subscriptions_df['subscription_status'] == 'ACTIVE']
num_call_records = 50000

call_records = []
for i in range(num_call_records):
    sub = active_subs.sample(1).iloc[0]
    
    call_id = f"CALL{i+1:08d}"
    call_type = random.choices(['LOCAL', 'STD', 'ISD', 'ROAMING'], weights=[70, 20, 5, 5])[0]
    call_direction = random.choice(['INCOMING', 'OUTGOING'])
    destination_number = f"+1{random.randint(2000000000, 9999999999)}"
    
    # Random timestamp within last 90 days
    call_start_time = datetime.now() - timedelta(
        days=random.randint(0, 90),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59)
    )
    
    # Call duration (0-3600 seconds)
    duration_seconds = random.randint(10, 3600)
    call_end_time = call_start_time + timedelta(seconds=duration_seconds)
    
    # Calculate charges based on call type
    charge_rates = {'LOCAL': 0, 'STD': 1.0, 'ISD': 5.0, 'ROAMING': 3.0}
    call_charges = round((duration_seconds / 60) * charge_rates[call_type], 4) if call_direction == 'OUTGOING' else 0
    
    call_records.append({
        'call_id': call_id,
        'subscription_id': sub['subscription_id'],
        'call_type': call_type,
        'call_direction': call_direction,
        'destination_number': destination_number,
        'call_start_time': call_start_time,
        'call_end_time': call_end_time,
        'call_duration_seconds': duration_seconds,
        'call_charges': call_charges,
        'created_at': call_end_time
    })

call_records_df = pd.DataFrame(call_records)
print(f"Generated {len(call_records_df)} call records")
print(f"Total call minutes: {call_records_df['call_duration_seconds'].sum() / 60:.2f}")
call_records_df.head()

# COMMAND ----------

# DBTITLE 1,Generate SMS Records
# Generate SMS records
num_sms_records = 100000

sms_records = []
for i in range(num_sms_records):
    sub = active_subs.sample(1).iloc[0]
    
    sms_id = f"SMS{i+1:08d}"
    sms_type = random.choices(['STANDARD', 'PROMOTIONAL', 'INTERNATIONAL'], weights=[85, 10, 5])[0]
    sms_direction = random.choice(['INCOMING', 'OUTGOING'])
    destination_number = f"+1{random.randint(2000000000, 9999999999)}"
    
    sms_timestamp = datetime.now() - timedelta(
        days=random.randint(0, 90),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )
    
    sms_count = 1
    
    # Calculate charges
    charge_rates = {'STANDARD': 0, 'PROMOTIONAL': 0, 'INTERNATIONAL': 2.0}
    sms_charges = charge_rates[sms_type] if sms_direction == 'OUTGOING' else 0
    
    sms_records.append({
        'sms_id': sms_id,
        'subscription_id': sub['subscription_id'],
        'sms_type': sms_type,
        'sms_direction': sms_direction,
        'destination_number': destination_number,
        'sms_timestamp': sms_timestamp,
        'sms_count': sms_count,
        'sms_charges': sms_charges,
        'created_at': sms_timestamp
    })

sms_records_df = pd.DataFrame(sms_records)
print(f"Generated {len(sms_records_df)} SMS records")
print(f"Total SMS count: {sms_records_df['sms_count'].sum()}")
sms_records_df.head()

# COMMAND ----------

# DBTITLE 1,Generate Data Usage Records
# Generate data usage records
num_data_records = 75000

data_usage_records = []
for i in range(num_data_records):
    sub = active_subs.sample(1).iloc[0]
    
    usage_id = f"DATA{i+1:08d}"
    usage_date = (datetime.now() - timedelta(days=random.randint(0, 90))).date()
    
    usage_start_time = datetime.combine(usage_date, datetime.min.time()) + timedelta(
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )
    
    # Session duration (5 mins to 4 hours)
    session_duration_mins = random.randint(5, 240)
    usage_end_time = usage_start_time + timedelta(minutes=session_duration_mins)
    
    # Data consumed (MB) - varies by session length
    data_consumed_mb = round(random.uniform(10, 500) * (session_duration_mins / 60), 4)
    
    network_type = random.choices(['2G', '3G', '4G', '5G'], weights=[5, 10, 60, 25])[0]
    
    # Calculate charges (if exceeding plan limits)
    data_charges = round(random.uniform(0, 50), 4) if random.random() > 0.8 else 0
    
    data_usage_records.append({
        'usage_id': usage_id,
        'subscription_id': sub['subscription_id'],
        'usage_date': usage_date,
        'usage_start_time': usage_start_time,
        'usage_end_time': usage_end_time,
        'data_consumed_mb': data_consumed_mb,
        'data_charges': data_charges,
        'network_type': network_type,
        'created_at': usage_end_time
    })

data_usage_df = pd.DataFrame(data_usage_records)
print(f"Generated {len(data_usage_df)} data usage records")
print(f"Total data consumed: {data_usage_df['data_consumed_mb'].sum() / 1024:.2f} GB")
data_usage_df.head()

# COMMAND ----------

# DBTITLE 1,Generate Bills
# Generate bills for subscriptions
bills = []
bill_items = []

for _, sub in subscriptions_df[subscriptions_df['subscription_status'].isin(['ACTIVE', 'SUSPENDED'])].iterrows():
    # Generate 3-6 monthly bills per subscription
    num_bills = random.randint(3, 6)
    
    for month in range(num_bills):
        bill_id = f"BILL{len(bills) + 1:08d}"
        
        billing_period_end = datetime.now().date() - timedelta(days=30 * month)
        billing_period_start = billing_period_end - timedelta(days=30)
        bill_date = billing_period_end + timedelta(days=1)
        due_date = bill_date + timedelta(days=15)
        
        # Get plan monthly charge
        plan_charge = plans_df[plans_df['plan_id'] == sub['plan_id']]['monthly_charge'].values[0]
        
        # Calculate usage charges
        call_charges = round(random.uniform(0, 100), 2)
        sms_charges = round(random.uniform(0, 20), 2)
        data_charges = round(random.uniform(0, 50), 2)
        
        total_amount = plan_charge + call_charges + sms_charges + data_charges
        tax_amount = round(total_amount * 0.18, 2)  # 18% tax
        discount_amount = round(random.uniform(0, 50), 2) if random.random() > 0.8 else 0
        net_amount = round(total_amount + tax_amount - discount_amount, 2)
        
        bill_status = random.choices(
            ['PAID', 'UNPAID', 'PARTIAL', 'OVERDUE'],
            weights=[70, 15, 10, 5]
        )[0]
        
        bills.append({
            'bill_id': bill_id,
            'customer_id': sub['customer_id'],
            'subscription_id': sub['subscription_id'],
            'bill_date': bill_date,
            'billing_period_start': billing_period_start,
            'billing_period_end': billing_period_end,
            'total_amount': total_amount,
            'tax_amount': tax_amount,
            'discount_amount': discount_amount,
            'net_amount': net_amount,
            'due_date': due_date,
            'bill_status': bill_status,
            'created_at': datetime.combine(bill_date, datetime.min.time())
        })
        
        # Generate bill items
        item_id = len(bill_items) + 1
        bill_items.append({
            'bill_item_id': item_id,
            'bill_id': bill_id,
            'item_type': 'MONTHLY_CHARGE',
            'description': 'Monthly plan charge',
            'quantity': 1,
            'unit_price': plan_charge,
            'amount': plan_charge,
            'created_at': datetime.combine(bill_date, datetime.min.time())
        })
        
        if call_charges > 0:
            item_id += 1
            bill_items.append({
                'bill_item_id': item_id,
                'bill_id': bill_id,
                'item_type': 'CALL_CHARGES',
                'description': 'Call usage charges',
                'quantity': round(random.uniform(50, 500), 2),
                'unit_price': round(call_charges / random.uniform(50, 500), 4),
                'amount': call_charges,
                'created_at': datetime.combine(bill_date, datetime.min.time())
            })
        
        if data_charges > 0:
            item_id += 1
            bill_items.append({
                'bill_item_id': item_id,
                'bill_id': bill_id,
                'item_type': 'DATA_CHARGES',
                'description': 'Data overage charges',
                'quantity': round(random.uniform(1, 10), 2),
                'unit_price': round(data_charges / random.uniform(1, 10), 4),
                'amount': data_charges,
                'created_at': datetime.combine(bill_date, datetime.min.time())
            })

bills_df = pd.DataFrame(bills)
bill_items_df = pd.DataFrame(bill_items)

print(f"Generated {len(bills_df)} bills")
print(f"Total billing amount: ${bills_df['net_amount'].sum():,.2f}")
print(f"Generated {len(bill_items_df)} bill items")
bills_df.head()

# COMMAND ----------

# DBTITLE 1,Generate Payments
# Generate payments for bills
payments = []

for _, bill in bills_df[bills_df['bill_status'].isin(['PAID', 'PARTIAL'])].iterrows():
    payment_id = f"PAY{len(payments) + 1:08d}"
    
    payment_date = bill['bill_date'] + timedelta(days=random.randint(1, 20))
    
    if bill['bill_status'] == 'PAID':
        payment_amount = bill['net_amount']
    else:  # PARTIAL
        payment_amount = round(bill['net_amount'] * random.uniform(0.3, 0.9), 2)
    
    payment_method = random.choices(
        ['CREDIT_CARD', 'DEBIT_CARD', 'NET_BANKING', 'UPI', 'WALLET', 'CASH'],
        weights=[30, 25, 20, 15, 8, 2]
    )[0]
    
    payment_status = random.choices(['SUCCESS', 'FAILED', 'PENDING'], weights=[92, 5, 3])[0]
    
    if payment_status == 'SUCCESS':
        transaction_reference = f"TXN{str(uuid.uuid4())[:8].upper()}"
    else:
        transaction_reference = None
    
    payments.append({
        'payment_id': payment_id,
        'bill_id': bill['bill_id'],
        'customer_id': bill['customer_id'],
        'payment_date': payment_date,
        'payment_amount': payment_amount,
        'payment_method': payment_method,
        'payment_status': payment_status,
        'transaction_reference': transaction_reference,
        'created_at': payment_date
    })

payments_df = pd.DataFrame(payments)
print(f"Generated {len(payments_df)} payments")
print(f"Total amount collected: ${payments_df[payments_df['payment_status']=='SUCCESS']['payment_amount'].sum():,.2f}")
payments_df.head()

# COMMAND ----------

# DBTITLE 1,Generate Complaint Categories and Complaints
# Generate complaint categories
complaint_categories = [
    {'category_id': 'CAT001', 'category_name': 'Network Issue', 'description': 'Poor network coverage or connectivity issues'},
    {'category_id': 'CAT002', 'category_name': 'Billing Issue', 'description': 'Incorrect billing or charges'},
    {'category_id': 'CAT003', 'category_name': 'Service Quality', 'description': 'Call drops, poor voice quality'},
    {'category_id': 'CAT004', 'category_name': 'Data Speed', 'description': 'Slow internet speed'},
    {'category_id': 'CAT005', 'category_name': 'Customer Service', 'description': 'Poor customer support'},
    {'category_id': 'CAT006', 'category_name': 'Plan Change', 'description': 'Issues with plan upgrade/downgrade'},
    {'category_id': 'CAT007', 'category_name': 'Device Issue', 'description': 'SIM card or device related issues'}
]

for cat in complaint_categories:
    cat['created_at'] = datetime.now() - timedelta(days=365)

complaint_categories_df = pd.DataFrame(complaint_categories)
print(f"Generated {len(complaint_categories_df)} complaint categories")

# Generate complaints
complaints = []
for i in range(500):
    customer = customers_df.sample(1).iloc[0]
    
    # Get customer's subscriptions
    cust_subs = subscriptions_df[subscriptions_df['customer_id'] == customer['customer_id']]
    sub = cust_subs.sample(1).iloc[0] if len(cust_subs) > 0 else None
    
    complaint_id = f"COMP{i+1:06d}"
    category = complaint_categories_df.sample(1).iloc[0]
    
    complaint_date = datetime.now() - timedelta(days=random.randint(0, 180))
    
    complaint_status = random.choices(
        ['OPEN', 'IN_PROGRESS', 'RESOLVED', 'CLOSED', 'ESCALATED'],
        weights=[10, 15, 50, 20, 5]
    )[0]
    
    priority = random.choices(['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'], weights=[20, 50, 25, 5])[0]
    
    resolution_date = None
    resolution_notes = None
    
    if complaint_status in ['RESOLVED', 'CLOSED']:
        resolution_date = complaint_date + timedelta(days=random.randint(1, 15))
        resolution_notes = f"Issue resolved for {category['category_name']}"
    
    complaints.append({
        'complaint_id': complaint_id,
        'customer_id': customer['customer_id'],
        'subscription_id': sub['subscription_id'] if sub is not None else None,
        'category_id': category['category_id'],
        'complaint_date': complaint_date,
        'complaint_description': f"{category['category_name']}: {fake.sentence()}",
        'complaint_status': complaint_status,
        'priority': priority,
        'resolution_date': resolution_date,
        'resolution_notes': resolution_notes,
        'created_at': complaint_date,
        'updated_at': resolution_date if resolution_date else complaint_date
    })

complaints_df = pd.DataFrame(complaints)
print(f"Generated {len(complaints_df)} complaints")
complaints_df.head()

# COMMAND ----------

# DBTITLE 1,Generate Service Areas
# Generate service areas
service_areas = []
for i in range(50):
    area_id = f"AREA{i+1:03d}"
    city = fake.city()
    state = fake.state()
    region = random.choice(['North', 'South', 'East', 'West', 'Central'])
    network_coverage = random.choices(['3G', '4G', '5G'], weights=[10, 60, 30])[0]
    
    service_areas.append({
        'area_id': area_id,
        'area_name': f"{city} Zone {i+1}",
        'city': city,
        'state': state,
        'region': region,
        'network_coverage': network_coverage,
        'created_at': datetime.now() - timedelta(days=365)
    })

service_areas_df = pd.DataFrame(service_areas)
print(f"Generated {len(service_areas_df)} service areas")
service_areas_df.head()

# COMMAND ----------

# DBTITLE 1,Save All Data to CSV Files
# Create output directory
import os
output_dir = "/Workspace/Users/niranjanebi706@gmail.com/telecom_project/sample_data"
os.makedirs(output_dir, exist_ok=True)

# Save all dataframes to CSV
dataframes = {
    'customers': customers_df,
    'customer_addresses': addresses_df,
    'mobile_plans': plans_df,
    'service_types': services_df,
    'plan_services': plan_services_df,
    'subscriptions': subscriptions_df,
    'call_records': call_records_df,
    'sms_records': sms_records_df,
    'data_usage': data_usage_df,
    'bills': bills_df,
    'bill_items': bill_items_df,
    'payments': payments_df,
    'complaint_categories': complaint_categories_df,
    'complaints': complaints_df,
    'service_areas': service_areas_df
}

for table_name, df in dataframes.items():
    file_path = f"{output_dir}/{table_name}.csv"
    df.to_csv(file_path, index=False)
    print(f"Saved {table_name}: {len(df)} records to {file_path}")

print(f"\n✅ All sample data generated successfully!")
print(f"📁 Files saved to: {output_dir}")

# COMMAND ----------

# DBTITLE 1,Data Generation Summary
# Summary statistics
print("=" * 80)
print("TELECOM SAMPLE DATA GENERATION SUMMARY")
print("=" * 80)

for table_name, df in dataframes.items():
    print(f"{table_name.ljust(30)}: {len(df):>10,} records")

print("=" * 80)
print("\nKEY METRICS:")
print(f"Total Customers: {len(customers_df):,}")
print(f"Active Subscriptions: {len(subscriptions_df[subscriptions_df['subscription_status']=='ACTIVE']):,}")
print(f"Total Call Minutes: {call_records_df['call_duration_seconds'].sum() / 60:,.2f}")
print(f"Total SMS: {sms_records_df['sms_count'].sum():,}")
print(f"Total Data (GB): {data_usage_df['data_consumed_mb'].sum() / 1024:,.2f}")
print(f"Total Revenue: ${bills_df['net_amount'].sum():,.2f}")
print(f"Payments Collected: ${payments_df[payments_df['payment_status']=='SUCCESS']['payment_amount'].sum():,.2f}")
print(f"Open Complaints: {len(complaints_df[complaints_df['complaint_status'].isin(['OPEN', 'IN_PROGRESS'])])}")
print("=" * 80)

# COMMAND ----------

# DBTITLE 1,validation cell
# Validate generated datasets
print("=" * 70)
print("DATASET VALIDATION")
print("=" * 70)

dataframes = {
    'customers': customers_df,
    'customer_addresses': addresses_df,
    'customer_contacts': customer_contacts_df,
    'mobile_plans': plans_df,
    'service_types': services_df,
    'plan_services': plan_services_df,
    'subscriptions': subscriptions_df,
    'subscription_services': subscription_services_df,
    'call_records': call_records_df,
    'sms_records': sms_records_df,
    'data_usage': data_usage_df,
    'bills': bills_df,
    'bill_items': bill_items_df,
    'payments': payments_df,
    'complaint_categories': complaint_categories_df,
    'complaints': complaints_df,
    'service_areas': service_areas_df
}

for name, df in dataframes.items():
    print(f"{name:<30} {len(df):>10,}")

print("=" * 70)

# COMMAND ----------

# ============================================================
# RELATIONAL INTEGRITY VALIDATION
# ============================================================

print("=" * 80)
print("RELATIONAL INTEGRITY VALIDATION")
print("=" * 80)

errors = []

# 1. Customer addresses -> customers
invalid_addresses = addresses_df[
    ~addresses_df['customer_id'].isin(customers_df['customer_id'])
]

print(f"Invalid customer addresses : {len(invalid_addresses):,}")

if len(invalid_addresses) > 0:
    errors.append("customer_addresses -> customers")

# 2. Customer contacts -> customers
invalid_contacts = customer_contacts_df[
    ~customer_contacts_df['customer_id'].isin(customers_df['customer_id'])
]

print(f"Invalid customer contacts  : {len(invalid_contacts):,}")

if len(invalid_contacts) > 0:
    errors.append("customer_contacts -> customers")

# 3. Plan services -> plans
invalid_plan_services = plan_services_df[
    ~plan_services_df['plan_id'].isin(plans_df['plan_id'])
]

print(f"Invalid plan services      : {len(invalid_plan_services):,}")

if len(invalid_plan_services) > 0:
    errors.append("plan_services -> mobile_plans")

# 4. Plan services -> service types
invalid_service_refs = plan_services_df[
    ~plan_services_df['service_id'].isin(services_df['service_id'])
]

print(f"Invalid service references : {len(invalid_service_refs):,}")

if len(invalid_service_refs) > 0:
    errors.append("plan_services -> service_types")

# 5. Subscriptions -> customers
invalid_sub_customers = subscriptions_df[
    ~subscriptions_df['customer_id'].isin(customers_df['customer_id'])
]

print(f"Invalid subscription customers : {len(invalid_sub_customers):,}")

if len(invalid_sub_customers) > 0:
    errors.append("subscriptions -> customers")

# 6. Subscriptions -> plans
invalid_sub_plans = subscriptions_df[
    ~subscriptions_df['plan_id'].isin(plans_df['plan_id'])
]

print(f"Invalid subscription plans : {len(invalid_sub_plans):,}")

if len(invalid_sub_plans) > 0:
    errors.append("subscriptions -> mobile_plans")

# 7. Subscription services -> subscriptions
invalid_sub_service_subs = subscription_services_df[
    ~subscription_services_df['subscription_id'].isin(
        subscriptions_df['subscription_id']
    )
]

print(f"Invalid subscription-service subscriptions : {len(invalid_sub_service_subs):,}")

if len(invalid_sub_service_subs) > 0:
    errors.append("subscription_services -> subscriptions")

# 8. Subscription services -> service types
invalid_sub_service_types = subscription_services_df[
    ~subscription_services_df['service_id'].isin(services_df['service_id'])
]

print(f"Invalid subscription-service services : {len(invalid_sub_service_types):,}")

if len(invalid_sub_service_types) > 0:
    errors.append("subscription_services -> service_types")

# 9. Calls -> subscriptions
invalid_calls = call_records_df[
    ~call_records_df['subscription_id'].isin(
        subscriptions_df['subscription_id']
    )
]

print(f"Invalid call subscriptions : {len(invalid_calls):,}")

if len(invalid_calls) > 0:
    errors.append("call_records -> subscriptions")

# 10. SMS -> subscriptions
invalid_sms = sms_records_df[
    ~sms_records_df['subscription_id'].isin(
        subscriptions_df['subscription_id']
    )
]

print(f"Invalid SMS subscriptions : {len(invalid_sms):,}")

if len(invalid_sms) > 0:
    errors.append("sms_records -> subscriptions")

# 11. Data -> subscriptions
invalid_data = data_usage_df[
    ~data_usage_df['subscription_id'].isin(
        subscriptions_df['subscription_id']
    )
]

print(f"Invalid data subscriptions : {len(invalid_data):,}")

if len(invalid_data) > 0:
    errors.append("data_usage -> subscriptions")

# 12. Bills -> customers
invalid_bill_customers = bills_df[
    ~bills_df['customer_id'].isin(customers_df['customer_id'])
]

print(f"Invalid bill customers : {len(invalid_bill_customers):,}")

if len(invalid_bill_customers) > 0:
    errors.append("bills -> customers")

# 13. Bills -> subscriptions
invalid_bill_subs = bills_df[
    ~bills_df['subscription_id'].isin(
        subscriptions_df['subscription_id']
    )
]

print(f"Invalid bill subscriptions : {len(invalid_bill_subs):,}")

if len(invalid_bill_subs) > 0:
    errors.append("bills -> subscriptions")

# 14. Bill items -> bills
invalid_bill_items = bill_items_df[
    ~bill_items_df['bill_id'].isin(bills_df['bill_id'])
]

print(f"Invalid bill items : {len(invalid_bill_items):,}")

if len(invalid_bill_items) > 0:
    errors.append("bill_items -> bills")

# 15. Payments -> bills
invalid_payments = payments_df[
    ~payments_df['bill_id'].isin(bills_df['bill_id'])
]

print(f"Invalid payment bills : {len(invalid_payments):,}")

if len(invalid_payments) > 0:
    errors.append("payments -> bills")

# 16. Payments -> customers
invalid_payment_customers = payments_df[
    ~payments_df['customer_id'].isin(customers_df['customer_id'])
]

print(f"Invalid payment customers : {len(invalid_payment_customers):,}")

if len(invalid_payment_customers) > 0:
    errors.append("payments -> customers")

# 17. Complaints -> customers
invalid_complaint_customers = complaints_df[
    ~complaints_df['customer_id'].isin(customers_df['customer_id'])
]

print(f"Invalid complaint customers : {len(invalid_complaint_customers):,}")

if len(invalid_complaint_customers) > 0:
    errors.append("complaints -> customers")

# 18. Complaints -> categories
invalid_complaint_categories = complaints_df[
    ~complaints_df['category_id'].isin(
        complaint_categories_df['category_id']
    )
]

print(f"Invalid complaint categories : {len(invalid_complaint_categories):,}")

if len(invalid_complaint_categories) > 0:
    errors.append("complaints -> complaint_categories")

print("=" * 80)

if len(errors) == 0:
    print("✅ ALL REFERENTIAL INTEGRITY CHECKS PASSED")
else:
    print("❌ REFERENTIAL INTEGRITY ERRORS FOUND:")
    for error in errors:
        print(" -", error)

# COMMAND ----------

# ============================================================
# PRIMARY KEY + BUSINESS RULE VALIDATION
# ============================================================

print("=" * 80)
print("PRIMARY KEY AND BUSINESS RULE VALIDATION")
print("=" * 80)

checks = {
    "customers.customer_id": customers_df['customer_id'].duplicated().sum(),
    "subscriptions.subscription_id": subscriptions_df['subscription_id'].duplicated().sum(),
    "subscriptions.phone_number": subscriptions_df['phone_number'].duplicated().sum(),
    "call_records.call_id": call_records_df['call_id'].duplicated().sum(),
    "sms_records.sms_id": sms_records_df['sms_id'].duplicated().sum(),
    "data_usage.usage_id": data_usage_df['usage_id'].duplicated().sum(),
    "bills.bill_id": bills_df['bill_id'].duplicated().sum(),
    "payments.payment_id": payments_df['payment_id'].duplicated().sum(),
    "complaints.complaint_id": complaints_df['complaint_id'].duplicated().sum()
}

for name, count in checks.items():
    print(f"{name:<40}: {count}")

print("\nBusiness Rules:")

print(
    "Negative call duration:",
    (call_records_df['call_duration_seconds'] < 0).sum()
)

print(
    "Negative SMS count:",
    (sms_records_df['sms_count'] <= 0).sum()
)

print(
    "Negative data usage:",
    (data_usage_df['data_consumed_mb'] < 0).sum()
)

print(
    "Invalid call timestamps:",
    (call_records_df['call_end_time'] < call_records_df['call_start_time']).sum()
)

print(
    "Invalid data timestamps:",
    (data_usage_df['usage_end_time'] < data_usage_df['usage_start_time']).sum()
)

print(
    "Invalid subscription dates:",
    (
        subscriptions_df['deactivation_date'].notna() &
        (
            subscriptions_df['deactivation_date'] <
            subscriptions_df['activation_date']
        )
    ).sum()
)

print("=" * 80)

# COMMAND ----------

# ============================================================
# FINAL DATA EXPORT
# ============================================================

dataframes = {
    'customers': customers_df,
    'customer_addresses': addresses_df,
    'customer_contacts': customer_contacts_df,
    'mobile_plans': plans_df,
    'service_types': services_df,
    'plan_services': plan_services_df,
    'subscriptions': subscriptions_df,
    'subscription_services': subscription_services_df,
    'call_records': call_records_df,
    'sms_records': sms_records_df,
    'data_usage': data_usage_df,
    'bills': bills_df,
    'bill_items': bill_items_df,
    'payments': payments_df,
    'complaint_categories': complaint_categories_df,
    'complaints': complaints_df,
    'service_areas': service_areas_df
}

output_dir = "/Workspace/Users/niranjanebi706@gmail.com/telecom_project/sample_data"

import os
os.makedirs(output_dir, exist_ok=True)

for table_name, df in dataframes.items():
    file_path = f"{output_dir}/{table_name}.csv"
    df.to_csv(file_path, index=False)
    print(f"✅ {table_name:<30} {len(df):>8,} records")

print("\n" + "=" * 70)
print(f"TOTAL TABLES: {len(dataframes)}")
print(f"OUTPUT DIRECTORY: {output_dir}")
print("=" * 70)