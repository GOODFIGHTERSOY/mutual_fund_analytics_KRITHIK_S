import requests
import pandas as pd

amfi_code = "125497"

url = f"https://api.mfapi.in/mf/{amfi_code}"

response = requests.get(url)

data = response.json()

print("Scheme:", data["meta"]["scheme_name"])
print("Latest NAV:", data["data"][0]["nav"])
print("Date:", data["data"][0]["date"])