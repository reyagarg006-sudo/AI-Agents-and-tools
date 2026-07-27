import requests

def convert_currency(amount, from_currency, to_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency.upper()}"
    
    response = requests.get(url)
    data = response.json()

    if "rates" not in data:
        return "Currency conversion failed"

    rate = data["rates"].get(to_currency.upper())

    if not rate:
        return "Invalid target currency"

    converted = amount * rate

    return f"{amount} {from_currency.upper()} = {converted:.2f} {to_currency.upper()}"