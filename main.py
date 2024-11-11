from fastapi import FastAPI
import uvicorn
import ssl

app = FastAPI()


@app.get("/test")
async def test_endpoint():
    return {"message": "Mutual TLS connection successful"}


if __name__ == "__main__":
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile="ssl_cfg/server.crt", keyfile="ssl_cfg/server.key")
    ssl_context.load_verify_locations(cafile="ca.pem")  # 验证客户端证书
    ssl_context.verify_mode = ssl.CERT_REQUIRED  # 要求客户端提供证书

    uvicorn.run(app, host="0.0.0.0", port=8000, ssl_context=ssl_context)
