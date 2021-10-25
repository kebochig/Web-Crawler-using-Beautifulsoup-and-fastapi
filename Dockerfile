FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt
COPY config.yml /code/config.yml
COPY crawl.py /code/crawl.py
COPY app.py /code/app.py
EXPOSE 8000
CMD [ "python", "/code/app.py" ]



