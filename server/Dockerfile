FROM python:3-alpine
ADD temp_server.py /
RUN pip install pygal
RUN pip install bottle
RUN pip install sqlalchemy
RUN pip install prettytable
EXPOSE 8080
ENTRYPOINT [ "python"]
CMD ["./temp_server.py"]
