"""
Configuration settings for the Maze Generator & Solver.
Optimized for different screen resolutions and performance levels.
"""

# Resolution and Maze Size Configurations
CONFIGURATIONS = {
    "ultra_hd": {
        "window_size": (1920, 1080),
        "rows": 37, "cols": 67,    # Maximized cell size with zero margins
        "animation_speed": 50,     # Very fast for large mazes
        "ui_font_size": 50,        # Font size for algorithm info and timer
        "description": "Ultra HD - Maximum size maze fills entire screen"
    },
    
    "high_quality": {
        "window_size": (1600, 900),
        "rows": 33, "cols": 61,    # Maximized for large screens
        "animation_speed": 25,     # Fast animation
        "ui_font_size": 28,        # Font size for algorithm info and timer
        "description": "High Quality - Maximum screen utilization with overlay UI"
    },
    
    "standard": {
        "window_size": (1280, 720),
        "rows": 25, "cols": 45,    # Reduced for much larger cells (was 35×63)
        "animation_speed": 50,     # Standard speed
        "ui_font_size": 24,        # Font size for algorithm info and timer
        "description": "Standard HD - Maximum size maze with large cells"
    },
    
    "performance": {
        "window_size": (1024, 576),
        "rows": 19, "cols": 35,    # Reduced for larger cells (was 27×49)
        "animation_speed": 75,     # Slower for visibility
        "ui_font_size": 20,        # Font size for algorithm info and timer
        "description": "Performance - Large visible maze for older systems"
    }
}

# Default configuration (can be changed here)
DEFAULT_CONFIG = "high_quality"

def get_config(config_name=None):
    """Get configuration by name or return default"""
    if config_name is None:
        config_name = DEFAULT_CONFIG
    
    if config_name not in CONFIGURATIONS:
        print(f"Configuration '{config_name}' not found. Using default: {DEFAULT_CONFIG}")
        config_name = DEFAULT_CONFIG
    
    return CONFIGURATIONS[config_name]

def list_configurations():
    """List all available configurations"""
    print("Available configurations:")
    for name, config in CONFIGURATIONS.items():
        print(f"  {name}: {config['description']}")
        print(f"    Resolution: {config['window_size'][0]}x{config['window_size'][1]}")
        print(f"    Maze size: {config['rows']}x{config['cols']} cells")
        print()
