# Yu-Gi-Oh! Deck Builder - Enhanced Edition

A completely revamped graphical user interface for building and managing Yu-Gi-Oh! card decks, developed in Python using the tkinter library with modern styling and enhanced functionality.

## 🚀 Major Improvements

### Visual Enhancements
- **Modern Dark/Light Themes**: Professional color schemes with hover effects
- **Improved Layout**: Better spacing, borders, and visual hierarchy
- **Emoji Icons**: Visual indicators for better user experience
- **Status Bar**: Real-time status updates at the bottom
- **Centered Window**: Application opens centered on screen

### Functionality Upgrades
- **20+ Pre-loaded Cards**: Expanded initial card collection including:
  - Dark Magician, Blue-Eyes White Dragon, Red-Eyes Black Dragon
  - Exodia, Dark Magician Girl, Kuriboh, Time Wizard
  - And many more popular cards!
- **Better Search**: Real-time filtering and improved search results
- **Deck Management**: Enhanced add/remove functionality with duplicate prevention
- **Import Feature**: Import cards from text files
- **Keyboard Shortcuts**: Ctrl+N (New), Ctrl+O (Open), Ctrl+S (Save), Ctrl+Q (Quit)

### Technical Improvements
- **Threaded Image Loading**: Prevents UI freezing when loading card images
- **Better Error Handling**: Comprehensive error messages and status updates
- **Theme Consistency**: All widgets properly themed in both light and dark modes
- **Performance**: Optimized card loading and filtering

## 🎨 Theme System

The application features two beautiful themes:

### Dark Theme (Default)
- Background: #2c3e50 (Dark blue-gray)
- Text: #ecf0f1 (Light gray)
- Accent Colors: Professional blues and reds

### Light Theme
- Background: #ecf0f1 (Light gray)
- Text: #2c3e50 (Dark blue-gray)
- Accent Colors: Bright blues and oranges

## 📋 Features

### Core Functionality
- **Card Search**: Real-time search with API integration
- **Deck Building**: Add/remove cards with visual feedback
- **Card Details**: High-quality images and comprehensive information
- **File Operations**: Save and load deck configurations
- **Theme Switching**: Toggle between light and dark modes

### Enhanced Features
- **Deck Counter**: Live count of cards in current deck
- **Import Cards**: Bulk import from text files
- **Keyboard Navigation**: Full keyboard support
- **Hover Effects**: Interactive button hover states
- **Status Updates**: Real-time operation feedback

## 🛠️ Installation

1. Ensure you have Python 3.6+ installed
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

Run the enhanced application:
```bash
python yugioh_deck_builder_enhanced.py
```

Or use the batch file (Windows):
```bash
run_enhanced.bat
```

### Keyboard Shortcuts
- `Ctrl+N` - New Deck
- `Ctrl+O` - Open Deck
- `Ctrl+S` - Save Deck
- `Ctrl+Q` - Quit Application
- `Enter` - Execute Search

### File Formats
- **Deck Files**: JSON format with card information
- **Import Files**: Text files with one card name per line

## 📁 Project Structure

```
YU-GI-OH! CardDeck/
├── yugioh_deck_builder_enhanced.py  # Main application
├── yugioh_deck_builder.py          # Original version
├── requirements.txt                # Dependencies
├── run_enhanced.bat               # Windows launcher
├── run.bat                        # Original launcher
├── README_ENHANCED.md             # This file
├── README.md                      # Original documentation
└── test_*.py                      # Test scripts
```

## 🔧 Technical Details

### Dependencies
- `requests` - API communication with YGOPRODeck
- `Pillow` - Image processing and display
- `tkinter` - GUI framework (built-in with Python)

### API Integration
The application uses the YGOPRODeck API:
- Endpoint: `https://db.ygoprodeck.com/api/v7/cardinfo.php`
- Fetches card data, images, and information
- Handles errors and timeouts gracefully

### Performance Features
- Background image loading prevents UI freezing
- Cached card data for better performance
- Efficient filtering and search algorithms

## 🎯 Usage Tips

1. **Search Efficiently**: Use real-time search for quick filtering
2. **Theme Preference**: Switch themes from the View menu
3. **Bulk Operations**: Use import/export for large decks
4. **Keyboard Shortcuts**: Learn the shortcuts for faster workflow
5. **Status Bar**: Watch the status bar for operation feedback

## 🐛 Troubleshooting

### Common Issues
- **API Connection**: Ensure internet connectivity for card data
- **Image Loading**: Some cards may not have available images
- **Large Decks**: Very large decks may take time to load

### Getting Help
If you encounter issues:
1. Check your internet connection
2. Verify all dependencies are installed
3. Check the status bar for error messages

## 📝 Version History

### v2.0 - Enhanced Edition
- Complete visual overhaul
- 20+ pre-loaded popular cards
- Theme system with light/dark modes
- Improved deck management
- Status bar and real-time feedback
- Keyboard shortcuts
- Import/export functionality

### v1.0 - Original
- Basic functionality
- Limited card selection
- Simple interface

## 👥 Contributing

Feel free to contribute by:
- Reporting bugs and issues
- Suggesting new features
- Improving documentation
- Adding new card sets

## 📄 License

This project is open source and available under the MIT License.

---

**Enjoy building your ultimate Yu-Gi-Oh! deck!** 🃏
