import os
from dotenv import load_dotenv

from client import Client


load_dotenv("stack.env")

API_TOKEN = os.environ.get("API_TOKEN")
FASTAPI_URL = os.environ.get("FASTAPI_URL")


def main():
    client = Client(FASTAPI_URL, API_TOKEN)
    working = client.check_mongo_health()
    print("MongoDB health:", working)


if __name__ == "__main__":
    main()
