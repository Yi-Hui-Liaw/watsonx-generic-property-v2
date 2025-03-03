FROM node:22

RUN mkdir node

COPY . /node

WORKDIR /node

RUN npm install 

EXPOSE 80

CMD ["npm", "run", "dev"]