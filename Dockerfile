FROM python:3.10

WORKDIR /code

COPY . /code

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 7860

CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]