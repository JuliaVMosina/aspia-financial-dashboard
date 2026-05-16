# Aspia-inspired: Finance & HR Outsourcing Executive Dashboard

> *Inspired by Aspia Group's reporting needs — not an official Aspia product. All data is synthetic.*

A corporate-simulation Power BI dashboard modeled after the reporting needs of a Nordic finance and payroll outsourcing company.
Synthetic data proportioned from Aspia Group's publicly available business profile.

---

## Business Question

**How is our finance outsourcing business growing — and where are the risks?**

A multi-region outsourcing firm serving 400+ clients across Accounting, Payroll, HR Services, and Tax & Legal generates complex operational and financial data.
This dashboard answers the questions a Head of BI or Regional Director would bring to a monthly review:

- Which service lines are driving revenue growth?
- Are we retaining clients — and where is churn emerging?
- How utilized is our workforce across roles and regions?
- What does MoM and YoY revenue performance look like?

---

## Dashboard Pages

| Page | Focus |
|---|---|
| **Overview** | Global KPIs: total revenue, active clients, retention rate, NPS score |
| **Financial Performance** | Revenue by service line, MoM % growth, YoY comparison, regional mix matrix |
| **Client Portfolio** | Client base trend, new vs churned, industry and size breakdown |
| **Operational Efficiency** | Employee utilization by role, contracts by service line, avg services per client |

---

## Key Metrics

| Metric | Value |
|---|---|
| Clients | ~400 (demo scale) |
| Observation period | 2022–2024 (3 years) |
| Retention rate | ~97% |
| Avg employee utilization | ~87% |
| Active contracts | ~982 |
| Service lines | Accounting · Payroll · HR Services · Tax & Legal |

---

## Data Architecture

```
data/
├── monthly_revenue.csv   ← revenue by month · region · service line
├── monthly_kpis.csv      ← retention % · NPS · new/churned clients · avg services
├── clients.csv           ← client master: industry · size · status · region
├── contracts.csv         ← contract-level: service line · monthly value · status
└── employees.csv         ← role · utilization % · clients managed · years experience
```

---

## Key DAX Measures

```dax
-- Month-over-month revenue growth using date arithmetic
Revenue MoM % =
VAR CurrentDate = SELECTEDVALUE(monthly_revenue[month])
VAR CurYear     = YEAR(CurrentDate)
VAR CurMonth    = MONTH(CurrentDate)
VAR PrevDate    = DATE(IF(CurMonth=1, CurYear-1, CurYear), IF(CurMonth=1, 12, CurMonth-1), 1)
VAR PriorRev    = CALCULATE(SUM(monthly_revenue[revenue_eur]), monthly_revenue[month] = PrevDate)
RETURN DIVIDE(SUM(monthly_revenue[revenue_eur]) - PriorRev, PriorRev) * 100

-- Year-over-year comparison
Revenue YoY % =
VAR RevCurrent = CALCULATE(SUM(monthly_revenue[revenue_eur]), monthly_revenue[year] = 2024)
VAR RevPrior   = CALCULATE(SUM(monthly_revenue[revenue_eur]), monthly_revenue[year] = 2023)
RETURN DIVIDE(RevCurrent - RevPrior, RevPrior) * 100
```

---

## Stack

| Tool | Purpose |
|---|---|
| Power BI Desktop | Dashboard development, DAX measures, data modeling |
| DAX | Time intelligence, KPI calculations, business logic |
| Power Query | Data transformation and loading |
| Star schema | Data model design |

---

## Design Style

Inspired by Aspia's corporate visual language:
- Primary: Aspia orange `#F4511E`
- Accent: Aspia pink-red `#F0314A`
- Secondary: `#FF8C42` · `#8B3FC8`
- Dark navy: `#1B2B40`
- Clean KPI cards, minimal gridlines

---

## Screenshots

| Page | Preview |
|---|---|
| Overview | *(screenshot)* |
| Financial Performance | *(screenshot)* |
| Client Portfolio | *(screenshot)* |
| Operational Efficiency | *(screenshot)* |

---

## About

**Julia Mosina** — BI & Data Analyst  
[LinkedIn](https://www.linkedin.com/in/julia-mosina) · Espoo, Finland · Open to opportunities in Finland and EU

*This is a portfolio project demonstrating Power BI and data modeling skills.
All data is synthetic and generated specifically for this dashboard.*
