FROM python:3.10

RUN apt-get update && \
    apt-get install -y --no-install-recommends wget ca-certificates xz-utils && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir ffmpeg && \
    cd ffmpeg && \
    wget -q -O ffmpeg.tar.xz https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-$(dpkg --print-architecture)-static.tar.xz && \
    tar --strip-components 1 -xJf ffmpeg.tar.xz && \
    mv ffmpeg /usr/bin/ffmpeg && \
    chmod u+x /usr/bin/ffmpeg && \
    cd - && \
    rm -rf ffmpeg

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --system

COPY main.py .

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
