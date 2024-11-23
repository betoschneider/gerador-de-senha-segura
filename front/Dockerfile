FROM python:3.10.12
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8502
CMD ["streamlit", "run", "main.py", "--server.port=8502", "--server.address=0.0.0.0"]

