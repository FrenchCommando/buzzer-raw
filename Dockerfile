FROM python:3.7-buster
COPY requirements.txt /
RUN apt-get update
Run apt-get upgrade -y
RUN apt-get install -y pkg-config \
  python-pexpect\
  libusb-dev \
  libdbus-1-dev\
  libglib2.0-dev\
  libudev-dev \
  libical-dev \
  libreadline-dev

RUN pip install --upgrade pip
RUN pip install --root-user-action=ignore -r requirements.txt
RUN pip install --root-user-action=ignore gunicorn
RUN pip install --root-user-action=ignore bluepy
RUN pip install --root-user-action=ignore pybluez
COPY . /
RUN mkdir /buzzerlog
CMD [ "python", "-u", "page.py" ]
