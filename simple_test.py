import requests

# Simple test that writes to a file
with open('test_result.txt', 'w') as f:
    try:
        f.write("Testing requests module...\n")
        response = requests.get("http://httpbin.org/get", timeout=5)
        f.write(f"HTTPBin status: {response.status_code}\n")
        
        f.write("Testing YGOPRODeck API...\n")
        ygo_response = requests.get("https://db.ygoprodeck.com/api/v7/cardinfo.php", timeout=10)
        f.write(f"YGOPRODeck status: {ygo_response.status_code}\n")
        
        if ygo_response.status_code == 200:
            data = ygo_response.json()
            f.write(f"Cards found: {len(data.get('data', []))}\n")
            f.write("SUCCESS: API is working!\n")
        else:
            f.write(f"API Error: {ygo_response.text[:100]}\n")
            
    except Exception as e:
        f.write(f"ERROR: {str(e)}\n")
        import traceback
        traceback.print_exc(file=f)
