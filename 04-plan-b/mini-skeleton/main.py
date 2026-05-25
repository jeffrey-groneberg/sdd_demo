from fastapi import FastAPI

app = FastAPI(title="URL Shortener (skeleton)")


@app.get("/hello")
def hello():
    return {"message": "hello, world"}
