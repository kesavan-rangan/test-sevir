ARG FUNCTION_DIR="/app"
ARG MODEL_DIR="t5-small"

# Creating a base image to install all the App dependencies
FROM python:slim-buster as build-image
RUN apt-get update && apt-get install -y g++ make cmake unzip libcurl4-openssl-dev
ARG FUNCTION_DIR
RUN mkdir -p ${FUNCTION_DIR}
COPY app/* ${FUNCTION_DIR}
COPY requirements.txt ${FUNCTION_DIR}
RUN pip install --target ${FUNCTION_DIR} -r ${FUNCTION_DIR}/requirements.txt
RUN pip install --target ${FUNCTION_DIR} awslambdaric

# Using the above image that has the installed libraries to be used in AWS Lambda's container image 
FROM python:slim-buster
ARG FUNCTION_DIR
ARG MODEL_DIR
WORKDIR ${FUNCTION_DIR}
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}
RUN mkdir -p ${MODEL_DIR} && mv config.json ${MODEL_DIR}
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "main.handler" ]
