from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import ssl
import os
from uvicorn.config import Config
from uvicorn.server import Server

app = FastAPI()  # 创建 FastAPI 应用实例


# 定义 POST 请求的数据模型
class SubmitRequest(BaseModel):
    param1: str
    param2: str


@app.get("/test")
async def test_endpoint():
    return {"message": "Mutual TLS connection successful"}


@app.post("/submit")
async def submit_endpoint(data: SubmitRequest, request: Request):
    # 打印接收到的POST请求数据
    print("Received POST data:", await request.json())

    # 检查数据并返回结果
    if not data.param1 or not data.param2:
        raise HTTPException(status_code=400, detail="Invalid request data")

    # 返回数据
    return {"message": "POST request received successfully", "data": data.dict()}


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

    # 创建 Uvicorn 配置对象
    config = Config(
        app=app,  # 指定 FastAPI 应用实例
        host="0.0.0.0",
        port=8001,
        ssl_certfile=cert_file,  # 服务器证书
        ssl_keyfile=key_file,  # 服务器私钥
        ssl_ca_certs=ca_file,  # 验证客户端证书的 CA 证书
        ssl_cert_reqs=ssl.CERT_REQUIRED,  # 双向 TLS 认证
    )

    # 创建并运行 Uvicorn 服务器
    server = Server(config)
    server.run()
