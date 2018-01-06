import pandas as pd 


def readCSV(csv_name):
  statesAndCities = []
  df = pd.read_csv(csv_name)
  cities = df.city
  state = df.state_id
  for i in range(0, len(cities)):
    temp = cities[i] + ", " + state[i]
    statesAndCities.append(temp)
  
  return statesAndCities

# print(readCSV("uscitiesv1.3.csv"))
