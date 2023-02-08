FROM --platform=linux/arm64/v8 python:3.9


# WORKDIR /src

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python", "./src/main.py" ]
