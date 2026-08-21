import requests
import sys

def get_bhubaneswar_weather():
    """
    Pre-MCP Weather Script:
    This script manually connects to the Open-Meteo API. 
    Notice how we have to hardcode the latitude, longitude, and JSON parsing logic.
    If the API changes, this script breaks. This illustrates why MCP is superior.
    """
    
    # Bhubaneswar coordinates
    lat = 20.2961
    lon = 85.8245
    
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    
    print("Fetching weather for Bhubaneswar using standard REST API...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        current = data.get("current_weather", {})
        temp = current.get("temperature", "Unknown")
        wind = current.get("windspeed", "Unknown")
        
        print(f"\nResult:")
        print(f"Temperature: {temp}°C")
        print(f"Wind Speed: {wind} km/h")
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    get_bhubaneswar_weather()
