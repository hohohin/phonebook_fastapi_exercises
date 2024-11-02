from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from Render!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}