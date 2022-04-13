ARG FUNCTION_DIR="/app"
FROM python:buster as build-image
RUN apt-get update && \
    apt-get install -y \
    g++ \
    make \
    cmake \
    unzip \
    libcurl4-openssl-dev
ARG FUNCTION_DIR
RUN mkdir -p ${FUNCTION_DIR}
COPY app/* ${FUNCTION_DIR}
COPY requirements.txt ${FUNCTION_DIR}
RUN pip install --target ${FUNCTION_DIR} -r requirements.txt
RUN pip install \
        --target ${FUNCTION_DIR} \
        awslambdaric

FROM python:buster
ARG FUNCTION_DIR
WORKDIR ${FUNCTION_DIR}
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "app.handler" ]
