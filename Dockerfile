FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./backend /app

COPY requirements.txt 
RUN pip install -r requirements.txt

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "80"]