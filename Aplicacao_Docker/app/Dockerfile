FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y python3 python3-pip\
	python3-numpy python3-scipy python3-matplotlib\
	libopencv-dev python3-opencv &&\
	rm -rf /var/lib/apt/lists/*

RUN mkdir src

WORKDIR /src
RUN pip3 install flask numpy scipy matplotlib opencv-python imutils
COPY ./src /src
EXPOSE 5000
CMD python3 server.py