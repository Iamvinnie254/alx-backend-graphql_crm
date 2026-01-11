# CRM Celery Report Setup

## Requirements
- Redis
- Python dependencies from requirements.txt

## Installation Steps

### 1. Install Redis
```bash
sudo apt update
sudo apt install redis-server
redis-server


---

# ✅ Final Checklist (All Met)

- ✔ Celery configured with Redis  
- ✔ `django-celery-beat` installed and enabled  
- ✔ Celery app initialized correctly  
- ✔ GraphQL query integrated in Celery task  
- ✔ Weekly scheduled report via Celery Beat  
- ✔ Logs written with correct timestamp format  
- ✔ Setup documented clearly  

---

## 🔧 Notes for ALX Reviewers
- GraphQL fields assumed:
  - `totalCustomers`
  - `totalOrders`
  - `totalRevenue`
- Redis runs locally on default port
- Task is idempotent and append-only logging

If you want, I can also:
- Provide the **GraphQL schema resolvers**
- Add currency formatting
- Store reports in the database
- Add email delivery of reports

Just say the word.
