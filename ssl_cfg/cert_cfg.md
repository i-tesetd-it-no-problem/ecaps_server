# 服务端配置证书

## 使用自签名证书

### 1. 创建根证书颁发机构（CA）
```shell
cd ssl_cfg

# 生成 CA 私钥
openssl genrsa -out ca.key 4096

# 生成 CA 自签名根证书
openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 -out ca.pem

# 生成服务器私钥
openssl genrsa -out server.key 2048
```

### 2. 使用CA签发服务器证书
```shell
# 生成服务器证书签名请求 (CSR)
openssl req -new -key server.key -out server.csr

# 使用CA签署服务器证书
openssl x509 -req -in server.csr -CA ca.pem -CAkey ca.key -CAcreateserial -out server.crt -days 365 -sha256
```
- 生成的`server.crt`是服务器证书, `server.key`是服务器私钥

### 3. 使用CA签发客户端（开发板）证书
```shell
# 生成客户端私钥
openssl genrsa -out client.key 2048

# 生成客户端证书签名请求 (CSR)
openssl req -new -key client.key -out client.csr

# 使用CA签署客户端证书
openssl x509 -req -in client.csr -CA ca.pem -CAkey ca.key -CAcreateserial -out client.crt -days 365 -sha256
```
- 生成的`client.cr`t是客户端证书, `client.key`是客户端私钥