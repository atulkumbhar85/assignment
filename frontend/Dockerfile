# Use Node.js as base image
FROM node:18-alpine

# Set environment variables
ENV FLASK_API_URL=http://0.0.0.0:5000

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]