from fastapi import FastAPI
import ssl
import os
from uvicorn.config import Config
from uvicorn.server import Server

app = FastAPI()  # 创建 FastAPI 应用实例


@app.get("/test")
async def test_endpoint():
    return {"message": "Mutual TLS connection successful"}


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))

    cert_file = os.path.join(script_dir, "ssl_cfg", "server.crt")  # 服务器证书文件路径
    key_file = os.path.join(script_dir, "ssl_cfg", "server.key")  # 服务器私钥文件路径
    ca_file = os.path.join(script_dir, "ssl_cfg", "ca.pem")  # CA 证书文件路径

    # 检查证书文件是否存在
    for file_path in [cert_file, key_file, ca_file]:  # 遍历所有证书文件路径
        if not os.path.isfile(file_path):
            print(f"Error: 文件未找到 - {file_path}")
            exit(1)

    # 创建 Uvicorn 对象
    config = Config(
        app=app,  # 指定 FastAPI 应用实例
        host="0.0.0.0",
        port=8001,
        ssl_certfile=cert_file,  # 服务器证书
        ssl_keyfile=key_file,  # 服务器私钥
        ssl_ca_certs=ca_file,  # 验证客户端证书的 CA 证书
        ssl_cert_reqs=ssl.CERT_REQUIRED,  # 双向 TLS 认证
    )

    server = Server(config)
    server.run()
