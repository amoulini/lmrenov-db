import os
import json
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Dict, Any, Optional

import pymysql

# --------------------------
# MariaDB connection
# --------------------------
MYSQL_HOST = os.environ.get("MYSQL_HOST")
MYSQL_PORT = int(os.environ.get("MYSQL_PORT"))
MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE")

API_TOKEN = os.environ.get("API_TOKEN")


def get_connection():
    return pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )


# --------------------------
# FastAPI app
# --------------------------
app = FastAPI(
    title="MariaDB API Gateway with Token Auth"
)

# --------------------------
# Models
# --------------------------
class DocumentModel(BaseModel):
    id: str
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
    return {"message": "FastAPI MariaDB Gateway is running!"}


@app.get("/health-db", dependencies=[Depends(verify_token)], tags=["Health"])
def health_check():
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")

        return {"status": "ok", "database": "reachable"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        conn.close()


# --------------------------
# Collection endpoints
# --------------------------
@app.get("/collections", dependencies=[Depends(verify_token)])
def get_collections():
    """
    Returns the list of all collection names in the database.
    """
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = [list(row.values())[0] for row in cursor.fetchall()]

        return {"collections": tables}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        conn.close()


@app.post("/collections/{collection_name}", dependencies=[Depends(verify_token)])
def create_collection(collection_name: str):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(f"""
                CREATE TABLE `{collection_name}` (
                    id VARCHAR(36) PRIMARY KEY,
                    data JSON
                )
            """)
        return {"message": f"Collection '{collection_name}' created"}

    except pymysql.err.OperationalError as e:
        # 1050 = Table already exists  
        if e.args[0] == 1050:
            raise HTTPException(status_code=410, detail=f"Collection '{collection_name}' already exists")
        else:
            raise HTTPException(status_code=500, detail=f"MySQL operational error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        conn.close()


@app.delete("/collections/{collection_name}", dependencies=[Depends(verify_token)])
def delete_collection(collection_name: str):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(f"DROP TABLE `{collection_name}`")

        return {"message": f"Collection '{collection_name}' deleted"}

    except pymysql.err.OperationalError as e:
        # 1146 = Table doesn't exist
        if e.args[0] == 1146:
            raise HTTPException(status_code=404, detail=f"Collection '{collection_name}' not found")
        else:
            raise HTTPException(status_code=405, detail=f"MySQL operational error: {str(e)}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        conn.close()



# --------------------------
# Get all documents from a collection
# --------------------------
@app.get("/collections/{collection_name}/documents", dependencies=[Depends(verify_token)])
def get_all_documents(collection_name: str):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM `{collection_name}`")
            rows = cursor.fetchall()

        return {"documents": rows}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        conn.close()


# --------------------------
# Document endpoints
# --------------------------
@app.post("/collections/{collection_name}/documents", dependencies=[Depends(verify_token)])
def create_document(collection_name: str, doc: DocumentModel):
    doc_id = doc.id

    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO `{collection_name}` (id, data) VALUES (%s, %s)",
                (doc_id, json.dumps(doc.data))
            )
        conn.commit()

        return {"inserted_id": doc_id}

    except pymysql.err.IntegrityError as e:
        error_code = e.args[0]
        if error_code == 1062:
            raise HTTPException(status_code=409, detail=f"Document with id '{doc_id}' already exists")
        else:
            raise HTTPException(status_code=400, detail=f"Database integrity error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        conn.close()


@app.put("/collections/{collection_name}/documents/{doc_id}", dependencies=[Depends(verify_token)])
def update_document(collection_name: str, doc_id: str, doc: DocumentModel):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            result = cursor.execute(
                f"UPDATE `{collection_name}` SET data=%s WHERE id=%s",
                (json.dumps(doc.data), doc_id)
            )

        if result == 0:
            raise HTTPException(status_code=404, detail="Document not found")
        return {"modified_count": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        conn.close()


@app.delete("/collections/{collection_name}/documents/{doc_id}", dependencies=[Depends(verify_token)])
def delete_document(collection_name: str, doc_id: str):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            result = cursor.execute(
                f"DELETE FROM `{collection_name}` WHERE id=%s",
                (doc_id,)
            )

        if result == 0:
            raise HTTPException(status_code=404, detail="Document not found")
        return {"deleted_count": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        conn.close()


@app.get("/collections/{collection_name}/documents/{doc_id}", dependencies=[Depends(verify_token)])
def get_document(collection_name: str, doc_id: str):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                f"SELECT data FROM `{collection_name}` WHERE id=%s",
                (doc_id,)
            )
            row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Document not found")
        return row

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        conn.close()
