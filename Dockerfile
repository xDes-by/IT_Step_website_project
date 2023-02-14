FROM python:3.9.12
WORKDIR /project
COPY ./requirements.txt project/requirements.txt
RUN pip install -r project/requirements.txt
COPY . /project
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 

