FROM python

RUN apt update

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

WORKDIR /home

ENTRYPOINT [ "python3" ]

CMD [ "stock_shelves.py" ]