FROM python:3.10.12
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "--server.port", "80", "main.py"]
EXPOSE 80
