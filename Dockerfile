FROM python:3.9-slim
WORKDIR /app
COPY rclone_initializer.py .
RUN pip install requests
CMD python ./rclone_initializer.py && tail -f /dev/null