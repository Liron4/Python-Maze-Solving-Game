import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game.game_controller import GameController
from config import get_config, list_configurations


def main():
    """Main function to start the maze application"""
    # Check for configuration argument
    config_name = None
    if len(sys.argv) > 1:
        if sys.argv[1] == "--list":
            list_configurations()
            return
        config_name = sys.argv[1]
    
    # Get configuration
    config = get_config(config_name)
    print(f"Using configuration: {config['description']}")
    print(f"Resolution: {config['window_size'][0]}x{config['window_size'][1]}")
    print(f"Maze size: {config['rows']}x{config['cols']} cells")
    print()
    
    # Create and run the game controller with configuration
    game_controller = GameController(
        rows=config['rows'], 
        cols=config['cols'], 
        window_size=config['window_size'],
        animation_speed=config['animation_speed'],
        ui_font_size=config['ui_font_size'],
        animate=True
    )
    game_controller.run()


if __name__ == "__main__":
    main()