FROM python:3.7

RUN pip3 install pika==1.1.0
RUN pip3 install pyzmq==19.0.1
RUN pip3 install julia

WORKDIR /app
COPY . .

# for ZeroMQ server
#EXPOSE 5555

CMD julia install.jl
CMD python3 hello-world/python/pyjulia_test.py
CMD python3 hello-world/python/hello.py
CMD python3 hello-world/python/sort.py
