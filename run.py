import uvicorn
import os

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8002,
        ssl_keyfile=".cert/key.pem",
        ssl_certfile=".cert/cert.pem",
        reload=True
    )