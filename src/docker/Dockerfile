FROM python:slim

WORKDIR /usr/src/app

# install requirements
RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy over rest of project.
COPY . /usr/src/app/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/docker/entrypoint.sh"]