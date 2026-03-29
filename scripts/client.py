import requests


class Client():
    def __init__(self, url: str, api_key: str):
        self.url = url
        self.api_key = api_key

    @property
    def headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def check_db_health(self) -> bool:
        health_url = f"{self.url}/health-db"
        response = requests.get(health_url, headers=self.headers)

        if response.status_code == 200:
            return True
        else:
            print(f"DB health check failed: {response.status_code} - {response.text}")
            return False
        
    # -----------------------
    # Collection endpoints
    # -----------------------

    def create_collection(self, collection_name: str):
        create_url = f"{self.url}/collections/{collection_name}"
        response = requests.post(create_url, headers=self.headers)

        if response.status_code in (200, 201):
            print(f"Collection '{collection_name}' created successfully")
        elif response.status_code == 410:
            print(f"Collection '{collection_name}' already exists.")
        else:
            print(f"Failed to create collection: {response.status_code} - {response.text}")

    def delete_collection(self, collection_name: str):
        delete_url = f"{self.url}/collections/{collection_name}"
        response = requests.delete(delete_url, headers=self.headers)

        if response.status_code in (200, 201):
            print(f"Collection '{collection_name}' deleted successfully")
        elif response.status_code == 404:
            print(f"Collection '{collection_name}' not found.")
        else:
            print(f"Failed to delete collection: {response.status_code} - {response.text}")

    def get_collections(self) -> list[str]:
        list_url = f"{self.url}/collections"
        collections = []
        response = requests.get(list_url, headers=self.headers)

        if response.status_code == 200:
            collections = response.json().get("collections", [])
        else:
            print(f"Failed to fetch collections: {response.status_code} - {response.text}")

        return collections

    # --------------------
    # Document endpoints
    # --------------------

    def get_documents(self, collection_name: str) -> list[dict]:
        get_url = f"{self.url}/collections/{collection_name}/documents"
        response = requests.get(get_url, headers=self.headers)

        if response.status_code == 200:
            return response.json().get("documents", [])
        else:
            print(f"Failed to fetch documents: {response.status_code} - {response.text}")
            return []


    def create_document(self, collection_name: str, data: dict, doc_id: str = None) -> str:
        """
        Create a document in the specified collection.

        Args:
            collection_name (str): The collection/table name
            data (dict): The document data
            doc_id (str, optional): Optional document ID. If not provided, a UUID will be generated.

        Returns:
            str: Inserted document ID, or empty string on failure
        """
        # Generate an ID if not provided
        if doc_id is None:
            doc_id = str(uuid.uuid4())

        payload = {
            "id": doc_id,
            "data": data
        }

        create_url = f"{self.url}/collections/{collection_name}/documents"
        response = requests.post(create_url, headers=self.headers, json=payload)

        if response.status_code in (200, 201):
            print(f"Document with ID '{doc_id}' created successfully.")
            return response.json().get("inserted_id", doc_id)
        if response.status_code == 409:
            print(f"Document with ID '{doc_id}' already exists.")
            return ""
        else:
            print(f"Failed to create document: {response.status_code} - {response.text}")
            return ""

    def update_document(self, collection_name: str, doc_id: str, data: dict):
        url = f"{self.url}/collections/{collection_name}/documents/{doc_id}"
        payload = {
            "id": doc_id,
            "data": data
        }
        response = requests.put(url, headers=self.headers, json=payload)

        if response.status_code in (200, 201):
            print(f"Document with ID '{doc_id}' updated successfully")
        elif response.status_code == 404:
            print(f"Document with ID '{doc_id}' not found.")
        else:
            print(f"Failed to update document: {response.status_code} - {response.text}")


    def delete_document(self, collection_name: str, doc_id: str):
        delete_url = f"{self.url}/collections/{collection_name}/documents/{doc_id}"
        response = requests.delete(delete_url, headers=self.headers)

        if response.status_code == 200:
            print(f"Document with ID '{doc_id}' deleted successfully")
        elif response.status_code == 404:
            print(f"Document with ID '{doc_id}' not found.")
        else:
            print(f"Failed to delete document: {response.status_code} - {response.text}")


    def get_document(self, collection_name: str, doc_id: str) -> dict:
        get_url = f"{self.url}/collections/{collection_name}/documents/{doc_id}"
        response = requests.get(get_url, headers=self.headers)

        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            print(f"Failed to fetch document: {response.status_code} - {response.text}")
            return {}
