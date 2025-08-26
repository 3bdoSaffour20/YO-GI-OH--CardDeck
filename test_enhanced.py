import tkinter as tk
from yugioh_deck_builder_enhanced import YugiohDeckBuilder

def test_application():
    """Test the enhanced Yu-Gi-Oh! deck builder application"""
    print("Testing Yu-Gi-Oh! Deck Builder - Enhanced Edition")
    print("=" * 50)
    
    # Test 1: Check if application initializes
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the window for testing
        app = YugiohDeckBuilder(root)
        print("✓ Application initialized successfully")
    except Exception as e:
        print(f"✗ Application initialization failed: {e}")
        return False
    
    # Test 2: Check theme setup
    try:
        themes = app.themes
        if "light" in themes and "dark" in themes:
            print("✓ Theme system working correctly")
        else:
            print("✗ Theme system not working")
            return False
    except Exception as e:
        print(f"✗ Theme test failed: {e}")
        return False
    
    # Test 3: Check initial cards loading
    try:
        if len(app.all_cards) > 0:
            print(f"✓ Loaded {len(app.all_cards)} initial cards")
        else:
            print("✗ No cards loaded")
            return False
    except Exception as e:
        print(f"✗ Card loading test failed: {e}")
        return False
    
    # Test 4: Test deck management functions
    try:
        initial_deck_count = len(app.current_deck)
        app.new_deck()
        if len(app.current_deck) == 0:
            print("✓ New deck function working")
        else:
            print("✗ New deck function not working")
            return False
    except Exception as e:
        print(f"✗ Deck management test failed: {e}")
        return False
    
    print("=" * 50)
    print("All basic tests passed!")
    print("The enhanced application should be ready to use.")
    print("\nTo run the full application:")
    print("python yugioh_deck_builder_enhanced.py")
    
    root.destroy()
    return True

if __name__ == "__main__":
    test_application()
