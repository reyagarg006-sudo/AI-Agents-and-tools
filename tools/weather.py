from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")

def _has_country_specified(location):
    """Check if location already includes country (comma-separated format)"""
    return "," in location.strip()

def _ask_for_country(city):
    """Ask user to specify country for ambiguous city names"""
    print(f"\n⚠️  '{city}' exists in multiple countries. Please specify the country.")
    country = input(f"Enter country for {city}: ").strip()
    if not country:
        return None
    return f"{city}, {country}"

# This function can be called directly for testing the weather tool independently
def get_weather(city):
    """
    Fetch weather for a city.
    If city doesn't include country, ask user to specify.
    
    Args:
        city: City name or "City, Country" format
    """
    city = city.strip()
    user_country = None
    
    # If city doesn't have country info, ask for it
    if not _has_country_specified(city):
        location = _ask_for_country(city)
        if not location:
            return "Error: Country not specified. Cannot fetch weather."
        # Extract country for validation
        user_country = location.split(",")[1].strip()
    else:
        location = city
        user_country = location.split(",")[1].strip()
    
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={location}"
    response = requests.get(url)
    data = response.json()
    # print(data)  # Debug: Print API response
    if "error" in data:
        error_message = data.get("error", {}).get("message", "Location not found")
        return f"Error: {error_message}"

    # Validate that API returned location from the specified country
    returned_country = data["location"]["country"].strip().lower()
    specified_country = user_country.lower()
    
    # Check if returned country matches specified country
    if returned_country != specified_country:
        print(f"\n⚠️  Did not find '{city.split(',')[0]}' in {user_country}.")
        print(f"     Found location: {data['location']['name']}, {data['location']['country']}")
        confirm = input(f"Is this correct? (yes/no): ").strip().lower()
        if confirm not in ["yes", "y"]:
            return f"Cancelled. Please verify the city spelling and try again."

    temp = data["current"]["temp_c"]
    condition = data["current"]["condition"]["text"]
    location_name = data["location"]["name"]
    country = data["location"]["country"]

    return f"It is {temp}°C in {location_name}, {country} with {condition}."

# dynamic input
if __name__ == "__main__":
    city = input("Enter city: ")
    print(get_weather(city))