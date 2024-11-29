import requests
import json
import re


class LazyDecoder(json.JSONDecoder):
    def decode(self, s, **kwargs):
        regex_replacements = [
            (re.compile(r'([^\\])\\([^\\])'), r'\1\\\\\2'),
            (re.compile(r',(\s*])'), r'\1'),
        ]
        for regex, replacement in regex_replacements:
            s = regex.sub(replacement, s)
        return super().decode(s, **kwargs)


def clean_json(raw_json):
    """
    Cleans a JSON string by escaping problematic characters and removing invalid control characters.
    """
    # Remove invalid control characters (e.g., \n, \r) from the JSON
    raw_json = re.sub(r'[\x00-\x1F\x7F]', '', raw_json)

    # Fix invalid escape sequences and trailing commas
    regex_replacements = [
        (re.compile(r'([^\\])\\([^\\])'), r'\1\\\\\2'),  # Fix invalid escape sequences
        (re.compile(r',(\s*])'), r'\1'),                # Remove trailing commas
    ]
    for regex, replacement in regex_replacements:
        raw_json = regex.sub(replacement, raw_json)

    return raw_json



def fetch_and_clean_api_data(url):
    try:
        # Fetch the raw API response
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful

        # Clean the JSON to fix escape issues
        cleaned_json = clean_json(response.text)

        # Parse the cleaned JSON
        data = json.loads(cleaned_json)
        return data
    except requests.RequestException as e:
        print(f"HTTP Request failed: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decoding failed: {e}")
        print("Partial cleaned JSON output for debugging:")
        # print(cleaned_json[:500])  # Print the first 500 characters of cleaned JSON for inspection
    return None


# # API URL
# api_url = "https://api.tce.ce.gov.br/index.php/sim/1_0/notas_empenhos.json?codigo_municipio=012&codigo_orgao=06&data_referencia_empenho=202305"
#
# # Fetch, clean, and print the API data
# data = fetch_and_clean_api_data(api_url)
# if data:
#     print(json.dumps(data, indent=2, ensure_ascii=False))
# else:
#     print("Failed to retrieve or parse API data.")