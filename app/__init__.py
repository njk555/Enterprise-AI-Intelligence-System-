from fastapi import FastAPI

app = FastAPI(
    title="Enterprise AI Intelligence Engine",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "project": "Enterprise AI Intelligence Engine",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}