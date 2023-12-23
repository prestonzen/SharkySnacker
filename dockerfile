# Use Alpine as the base image
FROM python:3.10.11-alpine

# Set the working directory in the container to /app
WORKDIR /app

# Install dependencies required for Pygame and Xvfb
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev \
    && apk add --no-cache sdl2 sdl2_ttf sdl2_image sdl2_mixer sdl2_gfx \
    && apk add --no-cache xvfb

# Copy the game files to the container
COPY . /app

# Install Python dependencies
RUN pip install pygame

# Set the display environment variable
ENV DISPLAY=:99

# Use Xvfb to create a virtual display
CMD Xvfb :99 -screen 0 1024x768x16 & \
    sleep 1 && \
    python ./game.py
