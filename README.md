# Car and Snake Game 🚗 🐍

A Python-based game where cars, snakes, and humans interact in a dynamic environment. Built using Pygame.

## 🎮 Game Overview

In this game, you control one car while other cars move autonomously. Snakes chase humans, and cars can collide with snakes to score points. The game features:

- Multiple autonomous cars with random movement patterns
- Snakes that actively chase the nearest human
- Humans that move randomly and avoid boundaries
- Score tracking for both car and snake collisions
- Player-controlled car with keyboard input

## 🔧 Prerequisites

- Python 3.x
- Pygame library

## 🛠️ Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd carandsnake
```

2. Install the required dependencies:
```bash
pip install pygame
```

## 🎯 How to Play

1. Run the game:
```bash
python main.py
```

2. Controls:
- Arrow keys: Move the selected car
- TAB: Switch between cars
- S: Stop the game
- Close window to exit

## 🎨 Game Elements

- 🚗 Cars: Move randomly, one can be player-controlled
- 🐍 Snakes: Chase the nearest human
- 👤 Humans: Move randomly within the game boundaries
- Scoring: Cars get points for hitting snakes, snakes get points for catching humans

## 📁 Project Structure

```
carandsnake/
├── main.py         # Main game loop and initialization
├── car.py          # Car class definition
├── snake.py        # Snake class definition
├── human.py        # Human class definition
├── car.png         # Car sprite image
├── snake.png       # Snake sprite image
├── human.png       # Human sprite image
├── gamelogo.png    # Game window icon
└── README.md       # Project documentation
```

## 🤝 Contributing

Feel free to fork the project and submit pull requests for any improvements.

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🎥 Preview

[Add screenshots or GIF of your game here]

## 🔧 Known Issues

- None currently reported. Please create an issue if you find any bugs.

## 🙏 Acknowledgments

- Pygame community for the excellent gaming framework
- [Add any other acknowledgments]