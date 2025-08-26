# Yu-Gi-Oh! Deck Builder

A graphical user interface for building and managing Yu-Gi-Oh! card decks, developed in Python using the tkinter library.

## Features

- **Card Search**: Search for Yu-Gi-Oh! cards by name using the YGOPRODeck API
- **Deck Management**: Add, remove, and organize cards in your deck
- **Card Details**: View detailed information including images, stats, and descriptions
- **Theme Support**: Toggle between light and dark themes
- **File Operations**: Save and load deck configurations
- **User-Friendly Interface**: Intuitive layout with clear navigation

## Requirements

- Python 3.6+
- Required packages:
  - `requests` - For API communication
  - `Pillow` - For image handling

## Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python yugioh_deck_builder.py
```

### Main Interface

The application features three main sections:

1. **Left Panel**: Available cards list with search functionality
2. **Middle Panel**: Current deck list with management buttons
3. **Right Panel**: Card details display with image and statistics

### Menu Options

- **File Menu**:
  - New Deck: Start with a fresh deck
  - Open Deck: Load a previously saved deck
  - Save Deck: Save your current deck configuration
  - Exit: Close the application

- **View Menu**:
  - Light Theme: Switch to light color scheme
  - Dark Theme: Switch to dark color scheme

### How to Use

1. **Search for Cards**: Type a card name in the search bar and press Enter or click "Search"
2. **Add to Deck**: Select a card from the available list and click "Add to Deck"
3. **View Details**: Click on any card in either list to see its details
4. **Manage Deck**: Use the buttons to remove cards or clear the entire deck
5. **Save/Load**: Use the File menu to save your deck or load a previous one

## API Integration

The application uses the YGOPRODeck API (https://db.ygoprodeck.com/api/v7/cardinfo.php) to fetch:
- Card information (name, type, stats, description)
- Card images
- Card attributes and properties

## File Format

Decks are saved as JSON files with the following structure:
```json
[
  {
    "id": "46986414",
    "name": "Dark Magician",
    "type": "Normal Monster"
  },
  ...
]
```

## Troubleshooting

- **API Connection Issues**: Ensure you have an active internet connection
- **Image Loading**: Some cards may not have images available
- **Theme Switching**: The theme change applies to most widgets but may not affect all visual elements

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.
