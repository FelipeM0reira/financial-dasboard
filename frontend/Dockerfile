FROM node:18-alpine AS build

WORKDIR /app

COPY packge*.json ./

RUN npm install

COPY . .

RUN npm run build

# ESTÁGIO 2: Servir com Nginx
FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf

COPY --from=builder /app/build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]