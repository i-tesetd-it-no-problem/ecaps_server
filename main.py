from fastapi import FastAPI
import uvicorn
import ssl
import os

app = FastAPI()


@app.get("/test")
async def test_endpoint():
    return {"message": "Mutual TLS connection successful"}


if __name__ == "__main__":
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 构建绝对路径
    cert_file = os.path.join(script_dir, "ssl_cfg", "server.crt")
    key_file = os.path.join(script_dir, "ssl_cfg", "server.key")
    ca_file = os.path.join(script_dir, "ssl_cfg", "ca.pem")

    # 打印路径以进行调试
    print("Certificate file path:", cert_file)
    print("Key file path:", key_file)
    print("CA file path:", ca_file)

    # 检查文件是否存在
    for file_path in [cert_file, key_file, ca_file]:
        if not os.path.isfile(file_path):
            print(f"Error: 文件未找到 - {file_path}")
            exit(1)

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=cert_file, keyfile=key_file)
    ssl_context.load_verify_locations(cafile=ca_file)  # 验证客户端证书
    ssl_context.verify_mode = ssl.CERT_REQUIRED  # 要求客户端提供证书

    # 启动FastAPI应用并启用SSL
    uvicorn.run(app, host="0.0.0.0", port=8000, ssl_context=ssl_context)
