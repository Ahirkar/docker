FROM node:alpine

WORKDIR /app1

COPY package*.json ./

COPY build /app1/build

COPY public /app1/public

COPY src /app1/src

COPY server.js /app1/server.js

RUN npm install --force

#RUN npm install react-scripts --save-dev --force

EXPOSE 3000

CMD [ "npm", "run" , "start" ]



