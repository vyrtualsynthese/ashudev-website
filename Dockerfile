#### Builder Stage ####
<<<<<<< HEAD
FROM node:14.19.1-alpine3.14 AS builder
=======
FROM node:16-alpine AS builder
>>>>>>> bca5fda4 (:green_heart: fix: Bumped node version)

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
