#### Builder Stage ####
FROM node:17-alpine AS builder

WORKDIR /home/node/app
ENV NODE_ENV development

RUN apk add --update-cache \
    alpine-sdk  \
    autoconf \
    automake \
    build-base \
    file \
    git \
    libtool \
    libpng \
    libpng-dev \
    libwebp \
    libwebp-dev \
    libjpeg-turbo \
    libjpeg-turbo-dev \
    musl \
    nasm \
    zlib \
    zlib-dev \
  && rm -rf /var/cache/apk/*

#### Dev Stage ####
FROM builder AS dev

COPY package*.json ./
RUN npm i --ignore-scripts
COPY . .

CMD ["npm", "start"]
