from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/crm_heartbeat_log.txt"
GRAPHQL_URL = "http://localhost:8000/graphql"

def log_crm_heartbeat():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive"

    # Optional GraphQL hello query
    try:
        transport = RequestsHTTPTransport(
            url=GRAPHQL_URL,
            verify=True,
            retries=2,
        )
        client = Client(
            transport=transport,
            fetch_schema_from_transport=False
        )

        query = gql("""
        query {
            hello
        }
        """)

        client.execute(query)
    except Exception:
        # Fail silently – heartbeat should still be logged
        pass

    with open(LOG_FILE, "a") as file:
        file.write(message + "\n")


GRAPHQL_URL = "http://localhost:8000/graphql"
LOG_FILE = "/tmp/low_stock_updates_log.txt"


def update_low_stock():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    transport = RequestsHTTPTransport(
        url=GRAPHQL_URL,
        verify=True,
        retries=3,
    )

    client = Client(
        transport=transport,
        fetch_schema_from_transport=False
    )

    mutation = gql("""
    mutation {
      updateLowStockProducts {
        success
        products {
          name
          stock
        }
      }
    }
    """)

    try:
        result = client.execute(mutation)
        products = result["updateLowStockProducts"]["products"]

        with open(LOG_FILE, "a") as log_file:
            for product in products:
                log_file.write(
                    f"{timestamp} - Product: {product['name']}, New Stock: {product['stock']}\n"
                )

    except Exception as e:
        with open(LOG_FILE, "a") as log_file:
            log_file.write(f"{timestamp} - Error updating stock: {e}\n")