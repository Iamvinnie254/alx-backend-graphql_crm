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
