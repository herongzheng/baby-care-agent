# Start from a minimal base image
FROM ubuntu:22.04

# Install curl (needed to download Toolbox)
RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy your tools.yaml config into the container
COPY tools.yaml /app/tools.yaml

# Download Toolbox binary
RUN curl -O https://storage.googleapis.com/genai-toolbox/v0.20.0/linux/amd64/toolbox \
    && chmod +x toolbox

# Run Toolbox with your config
ENTRYPOINT ["./toolbox", "--tools-file", "tools.yaml", "--address=0.0.0.0","--port=5000"]