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
    working = client.check_db_health()
    print("MongoDB health:", working)

    # Create collection
    client.create_collection(COLLECTION_NAME)

    # Get list of collections
    cols = client.get_collections()
    print("Collections:", cols)

    # Add Bikes
    for bike in bikes:
        client.create_document(COLLECTION_NAME, bike.model_dump(mode="json"), doc_id=bike.id)

    # List Bikes
    documents = client.get_documents(COLLECTION_NAME)
    ids = [doc["id"] for doc in documents]
    print("List of bikes:", ids)

    # Get specific Bike
    json_bike = client.get_document(COLLECTION_NAME, "4")
    bike = Bike.model_validate_json(json_bike)
    bike.print()

    # Delete bike
    client.delete_document(COLLECTION_NAME, "4")
    client.delete_document(COLLECTION_NAME, "5")

    # List Bikes
    documents = client.get_documents(COLLECTION_NAME)
    ids = [doc["id"] for doc in documents]
    print("List of bikes:", ids)

    # Update bike
    bike = bikes[3]
    bike.label = "New label"
    client.update_document(COLLECTION_NAME, bike.id, bike.model_dump(mode="json"))

    # Get specific Bike
    bike_number = 3
    json_bike = client.get_document(COLLECTION_NAME, str(bike_number))
    bike = Bike.model_validate_json(json_bike)
    bike.print()


    # # delete collection
    # client.delete_collection(COLLECTION_NAME)
    # client.delete_collection("NEW")

    # list collections
    cols = client.get_collections()
    print("Collections:", cols)


if __name__ == "__main__":
    main()