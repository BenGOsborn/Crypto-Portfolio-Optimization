FROM python:3.8-slim-buster
WORKDIR /app
COPY main.py arranger.py Pip* ./
RUN pip3 install pipenv
RUN pipenv install

CMD pipenv run python main.py