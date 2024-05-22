# 使用Alpine作为基础镜像
FROM python:3.9-alpine

# 设置工作目录
WORKDIR /app

# 复制requirements.txt到工作目录
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 设置环境变量
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# 暴露端口
EXPOSE 5000

# 运行Flask应用
CMD ["flask", "--debug", "run"]