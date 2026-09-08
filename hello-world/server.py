from fastapi import FastAPI 


app = FastAPI()

@app.api_route("/{path:path}", methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'])
def get_root(path: str):
    return "Hello World"
