# Environment setup
FROM python:3.8-slim-buster
WORKDIR /app
RUN pip install pipenv

# Install requirements
COPY Pipfile* ./
RUN pipenv install --system --deploy --ignore-pipfile

# Copy over files
COPY main.py arranger.py ./

# Start container
CMD ["python", "main.py"]