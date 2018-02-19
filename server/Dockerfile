FROM python:3
# CANNOT use python:3-alpine or slim, due to dateparser dependence on gcc among other libraries -_-
ADD temp_server.py /
ADD database.py /
RUN pip install pygal
RUN pip install bottle
RUN pip install sqlalchemy
RUN pip install prettytable
RUN pip install dateparser
EXPOSE 8080
ENTRYPOINT [ "python"]
CMD ["./temp_server.py"]
