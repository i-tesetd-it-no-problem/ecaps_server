from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field, ValidationError
from typing import Optional
import ssl
import os
from uvicorn.config import Config
from uvicorn.server import Server
import logging
from datetime import datetime

app = FastAPI()  # 创建 FastAPI 应用实例

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sensor_api")


# 电压电流传感器
class Lmv358Sensor(BaseModel):
    current: float = Field(..., ge=0, description="电流测量值")
    voltage: float = Field(..., ge=0, description="电压测量值")


# 环境光/接近/红外传感器
class Ap3216cSensor(BaseModel):
    illuminance: float = Field(..., description="光照强度")
    proximity: float = Field(..., description="接近度")
    infrared: float = Field(..., description="红外强度")


# 温湿度传感器
class Si7006Sensor(BaseModel):
    temperature: float = Field(..., description="温度值")
    humidity: float = Field(..., description="湿度值")


# 人体红外传感器
class Rda226Sensor(BaseModel):
    detected: bool = Field(..., description="检测到人体")


# 光闸/火焰传感器
class Itr9608Sensor(BaseModel):
    light_detected: bool = Field(..., description="光电开关检测状态")
    flame_detected: bool = Field(..., description="火焰检测状态")


# 心率/血氧传感器
class Max30102Sensor(BaseModel):
    heart_rate: float = Field(..., description="心率")
    blood_oxygen: float = Field(..., description="血氧水平")


# 所有传感器数据
class SensorData(BaseModel):
    timestamp: float = Field(..., description="Unix 时间戳")
    lmv358: Lmv358Sensor
    ap3216c: Ap3216cSensor
    si7006: Si7006Sensor
    rda226: Rda226Sensor
    itr9608: Itr9608Sensor
    max30102: Max30102Sensor


# 定义 POST 请求的数据模型（可选，如果需要额外字段）
class SubmitSensorRequest(BaseModel):
    data: SensorData


@app.get("/test")
async def test_endpoint():
    logger.info("Test endpoint accessed")
    return {"message": "Mutual TLS connection successful"}


@app.post("/submit_sensor_data")
async def submit_sensor_data(sensor_data: SensorData, request: Request):
    try:
        # 打印接收到的POST请求数据
        logger.info(f"Received POST data: {sensor_data.json()}")

        # 验证时间戳
        data_time = datetime.fromtimestamp(sensor_data.timestamp)
        logger.info(f"Data timestamp: {data_time.isoformat()}")

        # 这里可以添加更多的处理逻辑，例如存储数据到数据库

        # 返回成功响应
        return {"msg": "Sensor data received successfully"}
    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail="Invalid request data")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))

    cert_file = os.path.join(script_dir, "ssl_cfg", "server.crt")  # 服务器证书文件路径
    key_file = os.path.join(script_dir, "ssl_cfg", "server.key")  # 服务器私钥文件路径
    ca_file = os.path.join(script_dir, "ssl_cfg", "ca.pem")  # CA 证书文件路径

    # 检查证书文件是否存在
    for file_path in [cert_file, key_file, ca_file]:  # 遍历所有证书文件路径
        if not os.path.isfile(file_path):
            logger.error(f"Error: 文件未找到 - {file_path}")
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
    logger.info("Starting Uvicorn server with mutual TLS")
    server.run()
