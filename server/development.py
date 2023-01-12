import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app:sio_app",
        port=8443,
        log_level="info",
        reload=True,
        use_colors=True,
        ssl_keyfile="../key.pem",
        ssl_certfile="../cert.pem"
    )
