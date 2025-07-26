# Use official Node.js image to build the app
FROM node:18 AS build

WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json* ./
RUN npm install

# Copy source code
COPY . .

# Build argument for API URL
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL

# Build the app
RUN npm run build

# Use lightweight web server to serve the build
FROM nginx:alpine

# Copy built assets from previous stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80 for web traffic
EXPOSE 80

# Start nginx server
CMD ["nginx", "-g", "daemon off;"]
