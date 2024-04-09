import requests
from restcountries import RestCountryApiV2 as rapi

import api_openai


# currency code in format: ISO 4217
def get_current_exchange_rate(currency_code):
    """Fetches the current exchange rate for a given currency code from table 'A'."""
    url = f"http://api.nbp.pl/api/exchangerates/rates/A/{currency_code}/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        rate = data['rates'][0]['mid']  # 'mid' rate is used for table 'A'

        print(f"Current exchange rate for {currency_code}: {rate}")

        return rate
    else:
        return "Error: Unable to fetch data or data not found."


def get_current_population(english_country_name) -> int:
    answer = rapi.get_countries_by_name(english_country_name, filters=["population"])

    print(f"Population [{english_country_name}]: {answer[0].population}")
    return answer[0].population


def answer_general_question(question):
    answer = api_openai.ask_gpt("Answer shortly. Skip additional comments.", question=question)

    print(f"{question}: {answer}")
    return answer
