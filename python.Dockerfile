FROM python:3.7

RUN pip3 install pika==1.1.0
RUN pip3 install pyzmq==19.0.1
RUN pip3 install julia
###full guide https://pyjulia.readthedocs.io/en/latest/installation.html#step-3-install-julia-packages-required-by-pyjulia
WORKDIR /app
COPY . .

# for ZeroMQ server
#EXPOSE 5555
CMD python3 hello-world/python/initial_pyjulia.py
CMD python3 hello-world/python/hello.py
CMD python3 hello-world/python/sort.py
CMD python3 hello-world/python/pyjulia_test.py
