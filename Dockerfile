#using python base image
FROM python:3.13-slim

#setting working directory in the container
WORKDIR /app

#copying the contents of the current directory to the working directory in the container
COPY . .

RUN ls -la

#installing the dependencies from the requirements.txt file
RUN pip3 install -r requirements.txt

#exposing the port on which the flask app will run
EXPOSE 5000

#defining the command to run the flask app when the container starts
CMD ["python", "regression_predict_flask.py"]

