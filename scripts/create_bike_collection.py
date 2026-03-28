import os
from dotenv import load_dotenv

from client import Client
from bikes_data import bikes, Bike


load_dotenv("stack.env")

API_TOKEN = os.environ.get("API_TOKEN")
FASTAPI_URL = os.environ.get("FASTAPI_URL")
COLLECTION_NAME = "Bikes"


def main():
    client = Client(FASTAPI_URL, API_TOKEN)

    # Check MongoDB health
    working = client.check_mongo_health()
    print("MongoDB health:", working)

    # Get list of collections
    cols = client.get_collections()
    print("Collections:", cols)

    # Create collection
    # client.create_collection(COLLECTION_NAME)

    # # Add Bikes
    # for bike in bikes:
    #     # print(bike.model_dump(mode="json"))
    #     if client.get_document(COLLECTION_NAME, bike.id) == {}:
    #         client.create_document(COLLECTION_NAME, bike.model_dump(mode="json"))
    #     else:
    #         print(f"Bike {bike.id} already exists")

    # List Bikes
    # documents = client.get_documents(COLLECTION_NAME)
    # ids = [doc["id"] for doc in documents]
    # print("List of bikes:", ids)

    # # Get specific Bike
    # json_bike = client.get_document(COLLECTION_NAME, "4")
    # bike = Bike.model_validate(json_bike)
    # print("Bike 4:", bike)


if __name__ == "__main__":
    main()