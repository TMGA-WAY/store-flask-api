FROM python:3.10
EXPOSE 4500
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host","0.0.0.0", "--port","4500"]