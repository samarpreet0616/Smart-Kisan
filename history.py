import json

def load_history():

    try:

        with open("history.json","r") as file:

            data = json.load(file)

            return data


    except FileNotFoundError:


        return []



def save_city(city):

      old_history = load_history()

      if city in old_history:

          old_history.remove(city)
          old_history.insert(0,city)


      else:

          old_history.insert(0,city)

      old_history = old_history[:5]

      with open("history.json","w")as file:

          json.dump(old_history,file)







