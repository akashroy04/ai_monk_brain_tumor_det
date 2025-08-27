FROM python:3.11-slim


RUN apt-get update && apt-get install -y gcc build-essential libpoppler-cpp-dev pkg-config \
    cmake libsm6 libxext6 libfontconfig1 libxrender1 libxrender-dev libzbar-dev imagemagick \
    pdftohtml libxml2-dev libxslt1-dev ghostscript curl  unzip vim psmisc git parallel libzbar0


WORKDIR /target

COPY requirements.txt .
RUN pip --no-cache-dir install -r requirements.txt

EXPOSE 5501
EXPOSE 9085

COPY . .


RUN pip install uvicorn

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*


RUN pip install python-multipart


ENTRYPOINT ["/target/docker-entrypoint.sh"]
