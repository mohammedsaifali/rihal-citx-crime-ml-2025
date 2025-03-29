# Use the full Python 3.9 image (more complete than slim)
FROM python:3.9

# Set environment variables for consistent locale (can help prevent encoding issues)
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/requirements.txt

# Update package lists and install build-essential (for compiling any dependencies)
RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# Use python -m pip instead of pip directly to install dependencies
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project files into the container
COPY . /app

# Expose the port used by Streamlit
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
