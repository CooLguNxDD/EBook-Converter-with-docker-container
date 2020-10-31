FROM python:3.8

#RUN pip3 install pika==1.1.0
#RUN pip3 install pyzmq==19.0.1
#RUN pip install julia
#full guide https://pyjulia.readthedocs.io/en/latest/installation.html#step-3-install-julia-packages-required-by-pyjulia
WORKDIR /app
COPY . .

# for ZeroMQ server
#EXPOSE 5555

CMD python3 hello-world/hello.py
CMD python3 hello-world/sort.py
CMD python3 hello-world/pyjulia_test.py
