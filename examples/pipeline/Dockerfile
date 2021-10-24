FROM node:lts-alpine
LABEL maintainer="deva.kumar@sas.com"
RUN apk add --no-cache --upgrade bash
RUN apk add --no-cache --upgrade curl

WORKDIR /usr/src/app

ARG NODE_ENV
ENV NODE_ENV $NODE_ENV

COPY package.json /usr/src/app/
RUN npm install

COPY . /usr/src/app/

EXPOSE 80
CMD [ "npm", "start" ]
