import os
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from bson import ObjectId
from typing import Dict, Any, Optional

from .db_connection import db

API_TOKEN = os.environ.get("API_TOKEN")


# --------------------------
# FastAPI app
# --------------------------
app = FastAPI(title="MongoDB API Gateway with Token Auth")

# --------------------------
# Models
# --------------------------
class DocumentModel(BaseModel):
    data: Dict[str, Any]

# --------------------------
# Authentication dependency
# --------------------------
def verify_token(authorization: Optional[str] = Header(None)):
    """
    Verifies the Bearer token passed in Authorization header.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token scheme")
    token = authorization.split(" ")[1]
    if token != API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid API token")
    return True

# --------------------------
# Health check
# --------------------------
@app.get("/", tags=["Health"])
def read_root():
    return {"message": "FastAPI MongoDB Gateway is running!"}


@app.get("/health-db", dependencies=[Depends(verify_token)], tags=["Health"])
def health_check():
    try:
        # The ping command is cheap and does not require auth on most setups
        db.command("ping")
        return {"status": "ok", "database": "reachable"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database unreachable: {str(e)}"
        )



# --------------------------
# Collection endpoints
# --------------------------
@app.get("/collections", dependencies=[Depends(verify_token)], tags=["Collections"])
def get_collections():
    """
    Returns the list of all collection names in the database.
    """
    try:
        collections = db.list_collection_names()
        return {"collections": collections}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list collections: {str(e)}")

@app.post("/collections/{collection_name}", dependencies=[Depends(verify_token)])
def create_collection(collection_name: str):
    if collection_name in db.list_collection_names():
        raise HTTPException(status_code=400, detail="Collection already exists")
    db.create_collection(collection_name)
    return {"message": f"Collection '{collection_name}' created."}

@app.delete("/collections/{collection_name}", dependencies=[Depends(verify_token)])
def delete_collection(collection_name: str):
    if collection_name not in db.list_collection_names():
        raise HTTPException(status_code=404, detail="Collection not found")
    db.drop_collection(collection_name)
    return {"message": f"Collection '{collection_name}' deleted."}



# --------------------------
# Get all documents from a collection
# --------------------------
@app.get("/collections/{collection_name}/documents", dependencies=[Depends(verify_token)])
def get_all_documents(collection_name: str):
    if collection_name not in db.list_collection_names():
        raise HTTPException(status_code=404, detail="Collection not found")
    documents = list(db[collection_name].find())
    # Convert ObjectId to string for JSON serialization
    for doc in documents:
        doc["_id"] = str(doc["_id"])
    return {"documents": documents}


# --------------------------
# Document endpoints
# --------------------------

@app.post("/collections/{collection_name}/documents", dependencies=[Depends(verify_token)])
def create_document(collection_name: str, doc: DocumentModel):
    if collection_name not in db.list_collection_names():
        raise HTTPException(status_code=404, detail="Collection not found")
    result = db[collection_name].insert_one(doc.data)
    return {"inserted_id": str(result.inserted_id)}


@app.put("/collections/{collection_name}/documents/{doc_id}", dependencies=[Depends(verify_token)])
def update_document(collection_name: str, doc_id: str, doc: DocumentModel):
    if collection_name not in db.list_collection_names():
        raise HTTPException(status_code=404, detail="Collection not found")
    result = db[collection_name].update_one({"_id": ObjectId(doc_id)}, {"$set": doc.data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"modified_count": result.modified_count}


@app.delete("/collections/{collection_name}/documents/{doc_id}", dependencies=[Depends(verify_token)])
def delete_document(collection_name: str, doc_id: str):
    if collection_name not in db.list_collection_names():
        raise HTTPException(status_code=404, detail="Collection not found")
    result = db[collection_name].delete_one({"_id": ObjectId(doc_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"deleted_count": result.deleted_count}


@app.get("/collections/{collection_name}/documents/{doc_id}", dependencies=[Depends(verify_token)])
def get_document(collection_name: str, doc_id: str):
    if collection_name not in db.list_collection_names():
        raise HTTPException(status_code=404, detail="Collection not found")
    # try:
    #     obj_id = ObjectId(doc_id)
    # except Exception:
    #     raise HTTPException(status_code=400, detail="Invalid document ID format")
    doc = db[collection_name].find_one({"id": doc_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    doc["_id"] = str(doc["_id"])
    return {"document": doc}