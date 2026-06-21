FROM python:3.11.15-slim-bookworm
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python3" , "app.py" ]
