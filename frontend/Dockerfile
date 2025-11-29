# Frontend Dockerfile
FROM node:18-alpine AS build
WORKDIR /app

COPY package.json package-lock.json* ./
COPY public ./public
COPY src ./src

RUN npm ci --silent
RUN npm run build

# Production image to serve the build
FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
