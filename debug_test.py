import requests
import sys

def debug_test():
    print("Starting debug test...")
    
    # Test basic requests functionality
    try:
        print("Testing requests module...")
        response = requests.get("http://httpbin.org/get", timeout=5)
        print(f"HTTPBin test: {response.status_code}")
        
        # Test YGOPRODeck API
        print("Testing YGOPRODeck API...")
        ygo_response = requests.get("https://db.ygoprodeck.com/api/v7/cardinfo.php", timeout=10)
        print(f"YGOPRODeck status: {ygo_response.status_code}")
        
        if ygo_response.status_code == 200:
            data = ygo_response.json()
            print(f"Cards found: {len(data.get('data', []))}")
            
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = debug_test()
    print(f"Test completed: {'SUCCESS' if success else 'FAILED'}")
