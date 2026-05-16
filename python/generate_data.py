"""
Aspia-inspired: Finance & Payroll Outsourcing Analytics — Finland
Synthetic data generator

Simulates a finance/payroll outsourcing company operating in Finland,
with ~500 SME clients across 6 regions and 4 service lines.

Tables generated:
  clients.csv         — 500 Finnish SME clients
  contracts.csv       — service contracts per client
  monthly_revenue.csv — revenue by service line, region, month (2022-2024)
  monthly_kpis.csv    — KPI summary per month
  employees.csv       — ~75 employees across Finland
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

# ── Constants ──────────────────────────────────────────────────────────────

N_CLIENTS = 500

INDUSTRIES = ['IT/Tech', 'Retail', 'Construction', 'Manufacturing',
              'Hospitality', 'Healthcare', 'Other']
INDUSTRY_WEIGHTS = [0.20, 0.20, 0.15, 0.15, 0.10, 0.10, 0.10]

SIZES = ['Micro', 'Small', 'Medium', 'Large']
SIZE_WEIGHTS = [0.40, 0.35, 0.20, 0.05]

REGIONS = ['Helsinki', 'Espoo/Vantaa', 'Tampere', 'Turku', 'Oulu', 'Other']
REGION_WEIGHTS = [0.35, 0.20, 0.15, 0.10, 0.08, 0.12]

SERVICE_LINES = ['Accounting', 'Payroll', 'HR Services', 'Tax & Legal']

# Service adoption rates per client
SERVICE_ADOPTION = {
    'Accounting':  0.92,
    'Payroll':     0.78,
    'HR Services': 0.32,
    'Tax & Legal': 0.42,
}

# Monthly contract value ranges (EUR) by company size
MONTHLY_VALUE = {
    'Micro':  {
        'Accounting':  (200,  600),
        'Payroll':     (150,  400),
        'HR Services': (200,  500),
        'Tax & Legal': (150,  400),
    },
    'Small':  {
        'Accounting':  (600,  2500),
        'Payroll':     (400,  1800),
        'HR Services': (500,  1800),
        'Tax & Legal': (400,  1500),
    },
    'Medium': {
        'Accounting':  (2500, 9000),
        'Payroll':     (1800, 7000),
        'HR Services': (1500, 6000),
        'Tax & Legal': (1200, 5000),
    },
    'Large':  {
        'Accounting':  (9000,  28000),
        'Payroll':     (7000,  22000),
        'HR Services': (6000,  18000),
        'Tax & Legal': (5000,  15000),
    },
}

# Finnish synthetic company name components
PREFIXES = ['Fin', 'Nord', 'Hel', 'Tam', 'Arc', 'Scan', 'Kal',
            'Savo', 'Pohja', 'Lapin', 'Pro', 'Uni', 'Baltic', 'Länsi']
INDUSTRY_SUFFIXES = {
    'IT/Tech':        ['Tech', 'Soft', 'Digital', 'Systems', 'Solutions', 'Data'],
    'Retail':         ['Retail', 'Trade', 'Market', 'Commerce', 'Store'],
    'Construction':   ['Build', 'Rakennus', 'Infra', 'Civil', 'Construct'],
    'Manufacturing':  ['Manufacturing', 'Industry', 'Tuotanto', 'Works'],
    'Hospitality':    ['Hotel', 'Bistro', 'Ravintola', 'Catering'],
    'Healthcare':     ['Care', 'Health', 'Medical', 'Clinic'],
    'Other':          ['Services', 'Group', 'Partners', 'Consulting'],
}


def random_date(start: datetime, end: datetime) -> datetime:
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))


def company_name(industry: str, idx: int) -> str:
    prefix = random.choice(PREFIXES)
    suffix = random.choice(INDUSTRY_SUFFIXES[industry])
    return f"{prefix}{suffix} Oy"


# ── 1. Clients ─────────────────────────────────────────────────────────────

print("Generating clients...")
clients = []
for i in range(N_CLIENTS):
    industry = np.random.choice(INDUSTRIES, p=INDUSTRY_WEIGHTS)
    size     = np.random.choice(SIZES,      p=SIZE_WEIGHTS)
    region   = np.random.choice(REGIONS,    p=REGION_WEIGHTS)
    acquired = random_date(datetime(2018, 1, 1), datetime(2023, 6, 30))

    # ~22% total churn over the observation window
    is_churned = random.random() < 0.22
    churn_date = None
    if is_churned and acquired < datetime(2023, 1, 1):
        churn_date = random_date(
            max(acquired + timedelta(days=180), datetime(2022, 1, 1)),
            datetime(2024, 12, 31),
        )
        status = 'Churned'
    else:
        status = 'Active'

    clients.append({
        'client_id':    f'C{i+1:04d}',
        'company_name': company_name(industry, i),
        'industry':     industry,
        'size':         size,
        'region':       region,
        'acquired_date': acquired.strftime('%Y-%m-%d'),
        'status':       status,
        'churn_date':   churn_date.strftime('%Y-%m-%d') if churn_date else None,
    })

clients_df = pd.DataFrame(clients)
print(f"  {len(clients_df)} clients")


# ── 2. Contracts ───────────────────────────────────────────────────────────

print("Generating contracts...")
contracts = []
contract_id = 1
for _, client in clients_df.iterrows():
    acquired   = datetime.strptime(client['acquired_date'], '%Y-%m-%d')
    churn_date = (datetime.strptime(client['churn_date'], '%Y-%m-%d')
                  if (client['churn_date'] and isinstance(client['churn_date'], str)) else None)

    for service in SERVICE_LINES:
        if random.random() < SERVICE_ADOPTION[service]:
            lo, hi = MONTHLY_VALUE[client['size']][service]
            monthly_val = round(random.uniform(lo, hi), -1)  # round to 10 EUR
            end_date = churn_date if churn_date else None
            status   = 'Active' if not churn_date else 'Cancelled'

            contracts.append({
                'contract_id':      f'CON{contract_id:05d}',
                'client_id':        client['client_id'],
                'service_line':     service,
                'start_date':       acquired.strftime('%Y-%m-%d'),
                'end_date':         end_date.strftime('%Y-%m-%d') if end_date else None,
                'monthly_value_eur': monthly_val,
                'status':           status,
            })
            contract_id += 1

contracts_df = pd.DataFrame(contracts)
print(f"  {len(contracts_df)} contracts")


# ── 3. Monthly Revenue ─────────────────────────────────────────────────────

print("Generating monthly revenue...")
months = pd.date_range(start='2022-01-01', end='2024-12-01', freq='MS')
monthly_revenue = []

for month in months:
    # Active contracts this month
    active = contracts_df[
        (pd.to_datetime(contracts_df['start_date']) <= month) &
        (
            contracts_df['end_date'].isna() |
            (pd.to_datetime(contracts_df['end_date'].fillna('2099-01-01')) >= month)
        )
    ]
    active_with_region = active.merge(
        clients_df[['client_id', 'region']], on='client_id'
    )

    for service in SERVICE_LINES:
        for region in REGIONS:
            subset = active_with_region[
                (active_with_region['service_line'] == service) &
                (active_with_region['region'] == region)
            ]
            if len(subset) == 0:
                continue

            base = subset['monthly_value_eur'].sum()
            m    = month.month

            # Finnish business seasonality
            if   service == 'Payroll'     and m == 12:           season = 1.18  # holiday bonuses
            elif service == 'Payroll'     and m == 6:            season = 1.10  # summer holidays
            elif service == 'Tax & Legal' and m in (1, 2, 3, 4): season = 1.22  # tax filing season
            elif service == 'Accounting'  and m in (1, 3, 6, 9, 12): season = 1.08  # quarterly close
            else:                                                 season = 1.00

            # YoY growth ~6% annually
            year_growth = 1 + 0.06 * (month.year - 2022)
            noise       = np.random.uniform(0.97, 1.03)
            revenue     = round(base * season * year_growth * noise, 0)

            monthly_revenue.append({
                'month':            month.strftime('%Y-%m'),
                'year':             month.year,
                'month_num':        m,
                'service_line':     service,
                'region':           region,
                'revenue_eur':      revenue,
                'active_contracts': len(subset),
            })

monthly_revenue_df = pd.DataFrame(monthly_revenue)
print(f"  {len(monthly_revenue_df)} monthly revenue rows")


# ── 4. Monthly KPIs ────────────────────────────────────────────────────────

print("Generating monthly KPIs...")
monthly_kpis = []
clients_df['acquired_dt'] = pd.to_datetime(clients_df['acquired_date'])
clients_df['churn_dt']    = pd.to_datetime(clients_df['churn_date'])

for i, month in enumerate(months):
    # Active clients: acquired before month-end, not yet churned
    active_mask = (
        (clients_df['acquired_dt'] <= month) &
        (clients_df['churn_dt'].isna() | (clients_df['churn_dt'] > month))
    )
    n_active = active_mask.sum()

    # New clients this month
    n_new = (
        (clients_df['acquired_dt'].dt.year  == month.year) &
        (clients_df['acquired_dt'].dt.month == month.month)
    ).sum()

    # Churned this month
    n_churned = (
        clients_df['churn_dt'].notna() &
        (clients_df['churn_dt'].dt.year  == month.year) &
        (clients_df['churn_dt'].dt.month == month.month)
    ).sum()

    # Retention: annualised, capped to realistic range
    retention = round(100 - (n_churned / max(n_active, 1) * 100 * 12), 1)
    retention = float(np.clip(retention, 87.0, 97.0))

    # NPS: steady improvement 35 → 47 with noise
    nps = 35 + (i / len(months)) * 12 + np.random.normal(0, 1.5)
    nps = int(np.clip(round(nps), 30, 52))

    # Revenue per client
    month_str = month.strftime('%Y-%m')
    month_rev = monthly_revenue_df[
        monthly_revenue_df['month'] == month_str
    ]['revenue_eur'].sum()
    rev_per_client = round(month_rev / max(n_active, 1), 0)

    # Avg contracts per active client
    active_contracts = contracts_df[
        (pd.to_datetime(contracts_df['start_date']) <= month) &
        (
            contracts_df['end_date'].isna() |
            (pd.to_datetime(contracts_df['end_date'].fillna('2099-01-01')) >= month)
        )
    ]
    avg_services = round(len(active_contracts) / max(n_active, 1), 2)

    monthly_kpis.append({
        'month':                  month_str,
        'year':                   month.year,
        'month_num':              month.month,
        'active_clients':         int(n_active),
        'new_clients':            int(n_new),
        'churned_clients':        int(n_churned),
        'retention_rate_pct':     retention,
        'nps_score':              nps,
        'revenue_per_client_eur': int(rev_per_client),
        'avg_services_per_client': avg_services,
    })

monthly_kpis_df = pd.DataFrame(monthly_kpis)
print(f"  {len(monthly_kpis_df)} KPI rows")


# ── 5. Employees ───────────────────────────────────────────────────────────

print("Generating employees...")
ROLES         = ['Senior Accountant', 'Accountant', 'Payroll Specialist',
                 'HR Consultant', 'Tax Advisor']
ROLE_WEIGHTS  = [0.20, 0.40, 0.20, 0.10, 0.10]
CLIENTS_RANGE = {
    'Senior Accountant':  (25, 50),
    'Accountant':         (15, 35),
    'Payroll Specialist': (20, 45),
    'HR Consultant':      (10, 25),
    'Tax Advisor':        (15, 35),
}

employees = []
for i in range(75):
    role   = np.random.choice(ROLES, p=ROLE_WEIGHTS)
    region = np.random.choice(REGIONS, p=REGION_WEIGHTS)
    lo, hi = CLIENTS_RANGE[role]
    employees.append({
        'employee_id':     f'E{i+1:03d}',
        'role':            role,
        'region':          region,
        'clients_managed': random.randint(lo, hi),
        'years_experience': random.randint(1, 20),
        'utilization_pct': round(random.uniform(72, 98), 1),
    })

employees_df = pd.DataFrame(employees)
print(f"  {len(employees_df)} employees")


# ── Save ───────────────────────────────────────────────────────────────────

out = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
os.makedirs(out, exist_ok=True)

clients_df.drop(columns=['acquired_dt', 'churn_dt']).to_csv(
    os.path.join(out, 'clients.csv'), index=False)
contracts_df.to_csv(       os.path.join(out, 'contracts.csv'),       index=False)
monthly_revenue_df.to_csv( os.path.join(out, 'monthly_revenue.csv'), index=False)
monthly_kpis_df.to_csv(    os.path.join(out, 'monthly_kpis.csv'),    index=False)
employees_df.to_csv(       os.path.join(out, 'employees.csv'),        index=False)

print("\nDone!")
print(f"   clients.csv         -> {len(clients_df)} rows")
print(f"   contracts.csv       -> {len(contracts_df)} rows")
print(f"   monthly_revenue.csv -> {len(monthly_revenue_df)} rows")
print(f"   monthly_kpis.csv    -> {len(monthly_kpis_df)} rows")
print(f"   employees.csv       -> {len(employees_df)} rows")
