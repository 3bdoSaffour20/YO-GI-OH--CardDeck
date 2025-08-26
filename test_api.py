import requests
from PIL import Image, ImageTk
import io
import sys

def test_api_connection():
    print("Testing YGOPRODeck API connection...")
    try:
        print("Making request to: https://db.ygoprodeck.com/api/v7/cardinfo.php")
        response = requests.get("https://db.ygoprodeck.com/api/v7/cardinfo.php", timeout=10)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ API connection successful!")
            data = response.json()
            print(f"✓ Found {len(data['data'])} cards in the database")
            
            # Test fetching a specific card
            test_card = "Dark Magician"
            found = False
            for card in data['data']:
                if card['name'].lower() == test_card.lower():
                    print(f"✓ Found test card: {card['name']}")
                    print(f"  Type: {card['type']}")
                    print(f"  ATK: {card.get('atk', 'N/A')}")
                    print(f"  DEF: {card.get('def', 'N/A')}")
                    found = True
                    break
            
            if not found:
                print("✗ Test card not found")
                # Show first few cards for debugging
                print("First 5 cards available:")
                for i, card in enumerate(data['data'][:5]):
                    print(f"  {i+1}. {card['name']}")
                
        else:
            print(f"✗ API Error: {response.status_code}")
            print(f"Response text: {response.text[:200]}...")
            
    except requests.exceptions.Timeout:
        print("✗ API request timed out")
    except requests.exceptions.ConnectionError:
        print("✗ Connection error - check internet connection")
    except Exception as e:
        print(f"✗ Connection failed: {str(e)}")
        import traceback
        traceback.print_exc()

def test_image_loading():
    print("\nTesting image loading...")
    try:
        # Test loading an image
        image_url = "https://images.ygoprodeck.com/images/cards/46986414.jpg"  # Dark Magician
        print(f"Loading image from: {image_url}")
        response = requests.get(image_url, timeout=10)
        print(f"Image response status: {response.status_code}")
        
        if response.status_code == 200:
            image_data = response.content
            image = Image.open(io.BytesIO(image_data))
            print(f"✓ Image loaded successfully: {image.size}")
            print(f"✓ Image format: {image.format}")
        else:
            print(f"✗ Image loading failed: {response.status_code}")
            
    except Exception as e:
        print(f"✗ Image loading error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=" * 50)
    print("YU-GI-OH! DECK BUILDER - COMPREHENSIVE TEST")
    print("=" * 50)
    
    test_api_connection()
    test_image_loading()
    
    print("\n" + "=" * 50)
    print("TEST COMPLETED")
    print("=" * 50)
