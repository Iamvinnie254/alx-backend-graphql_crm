#!/bin/bash

# Absolute path to project root (adjust if necessary)
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

# Log file
LOG_FILE="/tmp/customer_cleanup_log.txt"

# Run Django cleanup command
DELETED_COUNT=$(python3 "$PROJECT_ROOT/manage.py" shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

cutoff_date = timezone.now() - timedelta(days=365)

qs = Customer.objects.exclude(orders__created_at__gte=cutoff_date).distinct()
count = qs.count()
qs.delete()
print(count)
")

# Log result with timestamp
echo \"$(date '+%Y-%m-%d %H:%M:%S') - Deleted customers: $DELETED_COUNT\" >> $LOG_FILE
