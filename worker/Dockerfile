#python debian. do not use alpine
FROM python:latest

#set working dir
WORKDIR /app

#copy local files to container
COPY . /app

#dependencies
RUN pip install -r requirements.txt


#starting command
CMD ["ipython"]