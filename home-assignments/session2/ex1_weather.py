import requests
import sys

def temp_converter(temp_kelvin, i_convention):
    if i_convention.upper() == "C":
        result = int(temp_kelvin - 273.15)
        o_convention = "celsius"
        return result
    elif i_convention.upper() == "F":
        result = int(round((temp_kelvin - 273.15) * 1.8))
        o_convention = "fahrenheit"
        return result
    else:
        raise ValueError("Please input proper convention C or F.")
        quit()


def temp_convention(i_convention):
    if i_convention.upper() == "C":
        o_convention = "celsius"
        return o_convention
    elif i_convention.upper() == "F":
        o_convention = "fahrenheit"
        return o_convention
    else:
        raise ValueError("Please input proper convention C or F.")
        quit()


def forecast(city, plus_days, i_convention, json_data):
    if plus_days >= 5:
        raise ValueError("The forecast for the next days can be in range on 1-4")
        quit()

    if plus_days >= 1:
        start_day = 1

    current_day = 0
    start_day = 0
    current_inc = 0
    full_day_temp = []

    for day in range(start_day, plus_days + 1):
        while json_data['list'][current_day]['dt_txt'][: -9] == json_data['list'][current_inc]['dt_txt'][: -9]:
            current_inc += 1
            temp_kelvin = json_data['list'][current_inc]['main']['temp']
            full_day_temp.append(temp_kelvin)
        weather = json_data['list'][current_inc]['weather'][0]['description']
        temp_min = min(full_day_temp)
        temp_min = temp_converter(temp_min, i_convention)
        temp_max = max(full_day_temp)
        temp_max = temp_converter(temp_max, i_convention)
        convention = temp_convention(i_convention)
        date = json_data['list'][current_day]['dt_txt'][:-9]
        current_day = len(full_day_temp)
        current_inc = current_day
        if day == 0:
            print(
                f'The weather today in {city} is {weather} with temperatures trailing from {temp_min}-{temp_max} {convention}.')
        elif day > 0 and day < 5:
            print(f'{date} {weather} with temperatures trailing from {temp_min}-{temp_max} {convention}.')

if __name__ == "__main__":



    city = input('wellcome to forecast station!! input city name: ')
    plus_days = int(input('you can get the forecast for today(0) and for next 4 days, please input 0-4: '))
    i_convention = input('type f to persent in fahrenheit or c to persent in celsius: ')

    api_address = 'http://api.openweathermap.org/data/2.5/forecast?appid=70e488eb4c2c4de0ccadc1095cec8b9c&q='
    url = api_address + city
    json_data = requests.get(url).json()

    forecast(city, plus_days, i_convention, json_data)
