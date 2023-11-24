# Use an official Python runtime as a parent image
FROM python:3.11.3

# Set the working directory in the container
WORKDIR /app

COPY . .


RUN pip install flask flask_cors pandas nltk scikit-learn pymongo kafka-python openai jwt

# Expose ports
EXPOSE 8001

CMD ["python3", "app.py"]
