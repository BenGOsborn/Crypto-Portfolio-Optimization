FROM python:3.8-slim-buster
WORKDIR /app
RUN pip install pipenv
COPY main.py arranger.py Pipfile* ./
RUN pipenv install --deploy --ignore-pipfile

CMD ["pipenv", "run", "python", "main.py"]