FROM python:3-alpine
 
# Create app directory
WORKDIR /app
 
# Install app dependencies
RUN pip3 install Flask azure-storage-blob
 
# Bundle app source
COPY . .

EXPOSE 5000

# Start app
CMD python3 app.py
