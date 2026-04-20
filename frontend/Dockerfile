# Stage 1: Build Stage
FROM node:20-slim AS build-stage

WORKDIR /app

# Install dependencies first (for better layer caching)
COPY package*.json ./
RUN npm install

# Build the project
COPY . .
RUN npm run build

# Stage 2: Production Stage (Nginx)
FROM nginx:stable-alpine AS production-stage

# Copy the build artifacts from stage 1
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copy custom Nginx configuration for Vue SPA routing
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
