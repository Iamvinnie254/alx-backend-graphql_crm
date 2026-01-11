from celery import shared_task
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

GRAPHQL_URL = "http://localhost:8000/graphql"
LOG_FILE = "/tmp/crm_report_log.txt"


@shared_task
def generate_crm_report():
    transport = RequestsHTTPTransport(
        url=GRAPHQL_URL,
        verify=True,
        retries=3,
    )

    client = Client(
        transport=transport,
        fetch_schema_from_transport=False
    )

    query = gql("""
    query {
      totalCustomers
      totalOrders
      totalRevenue
    }
    """)

    try:
        result = client.execute(query)

        customers = result["totalCustomers"]
        orders = result["totalOrders"]
        revenue = result["totalRevenue"]

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(LOG_FILE, "a") as file:
            file.write(
                f"{timestamp} - Report: "
                f"{customers} customers, "
                f"{orders} orders, "
                f"{revenue} revenue\n"
            )

    except Exception as e:
        with open(LOG_FILE, "a") as file:
            file.write(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Report Error: {e}\n"
            )
