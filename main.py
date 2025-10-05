from fastapi import FastAPI
from app.routes import router

# Initialize FastAPI application
app = FastAPI(
    title="Homomorphic Encryption Demo",
    description="Educational project demonstrating Paillier homomorphic encryption",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include API routes
app.include_router(router, prefix="/api/v1")

@app.get("/", tags=["Root"])
async def root():
    """Welcome endpoint with usage instructions"""
    return {
        "message": "Welcome to Homomorphic Encryption Demo API",
        "documentation": "/docs",
        "demo_endpoint": "/api/v1/demo/full-workflow",
        "quick_start": {
            "1": "Visit /api/v1/demo/full-workflow to see a complete example",
            "2": "Use /api/v1/encrypt to encrypt numbers",
            "3": "Use /api/v1/compute to perform operations on encrypted data",
            "4": "Use /api/v1/decrypt to decrypt results"
        }
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)