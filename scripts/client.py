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
    
    def check_mongo_health(self) -> bool:
        health_url = f"{self.url}/health-db"
        response = requests.get(health_url, headers=self.headers)

        if response.status_code == 200:
            return True
        else:
            print(f"MongoDB health check failed: {response.status_code} - {response.text}")
            return False

    def create_collection(self, collection_name: str):
        collections = self.get_collections()
        if collection_name in collections:
            print(f"The collection '{collection_name}' already exists. Skip creation.")
        
        else:
            create_url = f"{self.url}/collections/{collection_name}"
            response = requests.post(create_url, headers=self.headers)

            if response.status_code == 200 or response.status_code == 201:
                print(f"Collection '{collection_name}' created successfully")
            elif response.status_code == 400:
                print(f"Collection '{collection_name}' already exists")
            else:
                print(f"Failed to create collection: {response.status_code} - {response.text}")


    def get_collections(self) -> list[str]:
        list_url = f"{self.url}/collections"
        collections = []
        response = requests.get(list_url, headers=self.headers)

        if response.status_code == 200:
            collections = response.json().get("collections", [])
        else:
            print(f"Failed to fetch collections: {response.status_code} - {response.text}")

        return collections

    def get_document(self, collection_name: str, doc_id: str) -> dict:
        get_url = f"{self.url}/collections/{collection_name}/documents/{doc_id}"
        response = requests.get(get_url, headers=self.headers)

        if response.status_code == 200:
            return response.json().get("document", {})
        else:
            print(f"Failed to fetch document: {response.status_code} - {response.text}")
            return {}

    def create_document(self, collection_name: str, data: dict) -> str:
        create_url = f"{self.url}/collections/{collection_name}/documents"
        response = requests.post(create_url, headers=self.headers, json={"data": data})

        if response.status_code == 200:
            return response.json().get("inserted_id", "")
        else:
            print(f"Failed to create document: {response.status_code} - {response.text}")
            return ""
    
    def get_documents(self, collection_name: str) -> list[dict]:
        get_url = f"{self.url}/collections/{collection_name}/documents"
        response = requests.get(get_url, headers=self.headers)

        if response.status_code == 200:
            return response.json().get("documents", [])
        else:
            print(f"Failed to fetch documents: {response.status_code} - {response.text}")
            return []

        