FROM node:20-alpine AS dev
WORKDIR /frontend

COPY package.json package-lock.json* ./
RUN npm install

RUN npm install tailwindcss@3.4 postcss autoprefixer --save-dev && npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
