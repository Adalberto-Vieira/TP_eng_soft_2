FROM python:3.9-alpine

COPY ./requirements.txt /taskList/requirements.txt

WORKDIR /taskList

RUN pip install -r requirements.txt

COPY ./taskList /taskList

ENV FLASK_APP=app.py

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]