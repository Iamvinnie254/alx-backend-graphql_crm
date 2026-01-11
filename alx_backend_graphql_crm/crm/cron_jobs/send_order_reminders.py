#!/usr/bin/env python3

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from datetime import datetime
import sys

# GraphQL endpoint
GRAPHQL_URL = "http://localhost:8000/graphql"

# Log file
LOG_FILE = "/tmp/order_reminders_log.txt"

# GraphQL transport
transport = RequestsHTTPTransport(
    url=GRAPHQL_URL,
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# GraphQL query
query = gql("""
query RecentOrders {
  orders(lastDays: 7) {
    id
    customer {
      email
    }
  }
}
""")

try:
    result = client.execute(query)
    orders = result.get("orders", [])

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a") as log_file:
        for order in orders:
            log_file.write(
                f"{timestamp} - Order ID: {order['id']}, Customer Email: {order['customer']['email']}\n"
            )

    print("Order reminders processed!")

except Exception as e:
    print(f"Error processing order reminders: {e}", file=sys.stderr)
