# Sharky Snacker

Sharky Snacker is an engaging arcade-style game where players help Sharky, the friendly shark, dodge the cunning Slavic Witch and munch on delicious pelmeni. Proudly designed by the imaginative team at Kaizen Gaming, our indie studio.

## Gameplay

![Sharky Snacker Gameplay](demos/alphaShowcase.gif)

Navigate through the treacherous waters, outswim the Slavic Witch, and collect as many pelmeni as you can. Each level increases in difficulty, challenging your reflexes and strategy.

### Controls

- Use the arrow keys or `W`, `A`, `S`, `D` to move Sharky around.
- Dodge the Slavic Witch while collecting pelmeni and hearts.
- Press `Space` to play again upon game over.

### Features

- Responsive controls for fluid navigation.
- Progressive difficulty with each level for engaging gameplay.
- Retro-inspired graphics paired with charming sound effects.
- An energetic soundtrack that keeps you in the zone.

## Installation and Prerequisites

To play Sharky Snacker, you'll need Python and Pygame installed on your system.

```sh
pip install pygame
```

### Running with Python

After installing the prerequisites, follow these steps:

1. Clone this repository or download the ZIP file.
2. Navigate to the game's directory.
3. Run the game with:

```sh
python sharky_snacker.py
```

### Running with Docker

Alternatively, you can run Sharky Snacker using Docker.

#### Building the Docker Image

To build the Docker image:

```sh
docker build -t sharky_snacker .
```

#### Running the Docker Container

To run the game in a Docker container:

```sh
docker run -it --rm sharky_snacker
```

#### Running from Docker Hub

You can also run Sharky Snacker directly from Docker Hub:

```sh
docker run -it --rm prestonzen/sharky-snacker
```

## Credits

Sharky Snacker is crafted with ❤️ by Kaizen Gaming. A huge shoutout to our dedicated team members for bringing this game to life.

![Kaizen Gaming Logo](assets/KaizenGaming2-750x750p.png)

### License

Sharky Snacker is shared under the DBAD (Don't Be a Dick) License. Feel free to use and share this game, but always give credit where it's due.