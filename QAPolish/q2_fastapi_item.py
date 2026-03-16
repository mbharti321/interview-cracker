from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI

'''
Using FastAPI and Pydantic, define a Pydantic model ItemResponse with an item_id (integer), name (string), and an optional query_param (string). 
Then, create a FastAPI GET endpoint /items/{item_id} that takes an item_id (integer path parameter) and an optional q (string query parameter),
returning a JSON response based on the ItemResponse model with a hardcoded item name 'Example Item'.
'''

class ItemResponse(BaseModel):
    item_id: int
    name: str
    query_param: Optional[str] = None


app = FastAPI()


@app.get('/items/{item_id}', response_model=ItemResponse)
def get_item(item_id: int, q: Optional[str] = None):
    """Return a hardcoded item response using the ItemResponse model."""
    return ItemResponse(item_id=item_id, name='Example Item', query_param=q)


if __name__ == '__main__':
    # Example: run with `uvicorn q2_fastapi_item:app --reload --port 8000`
    pass
