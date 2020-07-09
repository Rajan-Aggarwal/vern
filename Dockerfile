
FROM python:3.7

ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install -r requirements.txt

EXPOSE 3000

ENTRYPOINT ["python3", "SlotValidationService/manage.py", "runserver", "0.0.0.0:8000"]
