FROM docker.io/node:20-bookworm-slim

WORKDIR /app

COPY ./frontend/package*.json ./

RUN npm install

COPY ./frontend .

EXPOSE 3000
