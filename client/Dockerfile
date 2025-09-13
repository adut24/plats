# ----------------------------
# Stage 1: Build Angular app
# ----------------------------
FROM node:22.18.0-alpine AS build

WORKDIR /app

RUN npm install -g npm@11.5.2 \
    && npm install -g @angular/cli@20.1.6

# Copy dependency files first (better layer caching)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the app
COPY . .

# Build Angular app in production mode
RUN ng build --configuration production

# ----------------------------
# Stage 2: Nginx for serving
# ----------------------------
FROM nginx:stable-alpine

# Remove default Nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy Angular build output from Stage 1
COPY --from=build /app/dist/plats/browser/ /usr/share/nginx/html/

COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose HTTP port
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
