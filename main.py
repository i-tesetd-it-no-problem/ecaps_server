from fastapi import FastAPI
import ssl
import os
from uvicorn.config import Config
from uvicorn.server import Server

app = FastAPI()  # 创建 FastAPI 应用实例


@app.get("/test")  # 定义一个 GET 请求的路由，路径为 /test
async def test_endpoint():  # 定义异步函数处理 /test 路由的请求
    return {"message": "Mutual TLS connection successful"}  # 返回 JSON 响应，表示双向 TLS 连接成功


if __name__ == "__main__":  # 判断是否作为主程序运行
    script_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本的绝对目录路径

    # 构建服务器证书、私钥和 CA 证书的绝对路径
    cert_file = os.path.join(script_dir, "ssl_cfg", "server.crt")  # 服务器证书文件路径
    key_file = os.path.join(script_dir, "ssl_cfg", "server.key")  # 服务器私钥文件路径
    ca_file = os.path.join(script_dir, "ssl_cfg", "ca.pem")  # CA 证书文件路径

    # 打印证书文件路径，用于调试
    print("Certificate file path:", cert_file)  # 输出服务器证书路径
    print("Key file path:", key_file)  # 输出服务器私钥路径
    print("CA file path:", ca_file)  # 输出 CA 证书路径

    # 检查证书文件是否存在
    for file_path in [cert_file, key_file, ca_file]:  # 遍历所有证书文件路径
        if not os.path.isfile(file_path):  # 如果文件不存在
            print(f"Error: 文件未找到 - {file_path}")  # 打印错误信息，指出缺失的文件
            exit(1)  # 退出程序，返回错误状态码

    # 创建 Uvicorn 配置对象，包含 SSL 参数
    config = Config(
        app=app,  # 指定 FastAPI 应用实例
        host="0.0.0.0",  # 服务器监听的主机地址，0.0.0.0 表示监听所有可用接口
        port=8000,  # 服务器监听的端口号
        ssl_certfile=cert_file,  # 指定服务器证书文件
        ssl_keyfile=key_file,  # 指定服务器私钥文件
        ssl_ca_certs=ca_file,  # 指定用于验证客户端证书的 CA 证书文件
        ssl_cert_reqs=ssl.CERT_REQUIRED,  # 要求客户端提供有效的证书，实现双向 TLS 认证
    )

    # 创建并运行 Uvicorn 服务器
    server = Server(config)  # 使用配置对象创建 Uvicorn 服务器实例
    server.run()  # 启动服务器，开始监听请求
