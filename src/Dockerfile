FROM python:3.8-slim-buster
WORKDIR /app
COPY main.py local.py Pip* ./
RUN pip3 install pipenv
RUN pipenv install

CMD pipenv run python main.py