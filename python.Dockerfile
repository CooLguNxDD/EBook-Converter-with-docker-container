#FROM ubuntu:latest
#RUN apt-get clean && apt-get update && apt-get install -y locales
#RUN locale-gen en_US.UTF-8
#ENV LANG en_US.UTF-8
#ENV LANGUAGE en_US:en
#ENV LC_ALL en_US.UTF-8

FROM python:3.8

RUN pip3 install pika==1.1.0
RUN pip3 install pyzmq==19.0.1
RUN pip3 install beautifulsoup4
RUN pip3 install lxml
RUN pip3 install natsort

WORKDIR /app
ADD . /app

#ENV LANG en_US.UTF-8
#ENV LANGUAGE en_US:en
#ENV LC_ALL en_US.UTF-8
ENV PYTHONIOENCODING=utf-8
RUN pip3 install --no-cache-dir Cython==3.0a6
RUN python3 setup.py build_ext --inplace

# for ZeroMQ server
#EXPOSE 5555
#CMD python3 hello-world/python/sort.py
#CMD python3 hello-world/python/pyjulia_test.py
#ENTRYPOINT ["python"]
#CMD ["\main_docker_prefix.py"]
CMD TIMEOUT 3
CMD python3 setup.py build_ext --inplace
CMD python3 ebookSend.py
CMD python3 docker_prefix_content.py
CMD python3 main_docker_prefix.py

