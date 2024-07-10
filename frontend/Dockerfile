FROM node:14


WORKDIR /frontend


COPY package*.json ./


RUN npm install


COPY . .


RUN npm run build


CMD ["npm", "run", "serve"]
