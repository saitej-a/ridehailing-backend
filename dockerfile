
FROM python
WORKDIR "./app"
COPY . .
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD ["python3","manager.py","runserver","0.0.0.0:8000"]