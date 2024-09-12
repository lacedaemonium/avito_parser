FROM ubuntu:22.04

WORKDIR /app

COPY . .

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y build-essential libdbus-glib-1-dev libgirepository1.0-dev
RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libatk-bridge2.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget libcairo2-dev libgirepository1.0-dev
RUN apt install -y python3-pip
RUN pip3 install -r requirements.txt

CMD [ "python3", "engine.py" ]


