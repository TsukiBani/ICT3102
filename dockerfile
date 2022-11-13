# # from alpine:latest
# # FROM ubuntu:latest
# FROM python:3.9.7-alpine

# WORKDIR /code
# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0

# RUN apk add --no-cache gcc musl-dev linux-headers
# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt

# EXPOSE 5000

# COPY . .

# # ENTRYPOINT  ["python"]

# # CMD ["flask", "--app", "main", "run"]
# CMD [ "flask", "run" ]

# Use an official Python runtime as an image
FROM python:3.6

# The EXPOSE instruction indicates the ports on which a container
EXPOSE 5000
EXPOSE 3306

# Sets the working directory for following COPY and CMD instructions
# Notice we haven’t created a directory by this name - this instruction
# creates a directory with this name if it doesn’t exist
WORKDIR /app

COPY requirements.txt requirements.txt
# COPY init.sql docker-entrypoint-initdb.d/init.sql
ADD ./db/init.sql /docker-entrypoint-initdb.d

RUN python -m pip install --upgrade pip
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org --no-cache-dir -r requirements.txt

# Run app.py when the container launches
COPY . .
CMD python app.py