import logging
from logging_config import setup_logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from urls import router as gps_router  
from logging_config import logger

# Create FastAPI instance
app = FastAPI(
    title="Gps Ping API",
    description="API for receiving GPS pings",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this according to your requirements
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root URL to verify service is running
@app.get("/")
async def read_root():
    logger.info("GPS Ping API is running")
    return {"message": "GPS Ping API is running"}

app.include_router(gps_router)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception for request {request.url}: {exc}", exc_info=True)
    return HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)