FROM python:3.10.2-alpine
# set work directory
WORKDIR /bundles_checker
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
    
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
# copy project
COPY . .
# run entrypoint.sh
ENTRYPOINT ["/bundles_checker/entrypoint.sh"]