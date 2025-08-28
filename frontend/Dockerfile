FROM node:20-alpine AS deps
WORKDIR /ui
COPY package.json package-lock.json* ./
RUN npm install

FROM node:20-alpine AS dev
WORKDIR /ui

COPY --from=deps /ui/node_modules ./node_modules

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
