# Use the official NGINX image as the base image
#FROM nginx:latest

# Copy custom NGINX configuration files
#COPY nginx.conf /etc/nginx/nginx.conf
#COPY default.conf /etc/nginx/conf.d/default.conf

# Copy static website files to the web server root directory
#COPY index.html /usr/share/nginx/index.html

# Expose port 80 for HTTP traffic
#EXPOSE 80

# Start NGINX when the container starts
#CMD ["nginx", "-g", "daemon off;"]