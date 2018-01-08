import requests
from bs4 import BeautifulSoup

def get_all_weather_conditions():
  url = "https://www.weatherbit.io/api/codes"
  response = requests.get(url)
  html = response.content

  soup = BeautifulSoup(html)
  table = soup.find('tbody')
  list_of_rows = []
  for row in table.findAll('tr'):
    list_of_cells = []
    for cell in row.findAll('td'):
      text = cell.text.replace('&nbsp;', '')
      list_of_cells.append(text)
    list_of_rows.append(list_of_cells[1])
  return list_of_rows

# print(get_all_weather_conditions())
