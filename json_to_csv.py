# Código para transformar JSON a CSV
# Código para transformar un JSON de entradas en CSV

import json

import pandas as pd

def json_to_csv(json_file, csv_file):

    """

    Convierte un archivo JSON a CSV.



    :param json_file: Ruta al archivo JSON de entrada.

    :param csv_file: Ruta al archivo CSV de salida.

    """

    with open(json_file, 'r', encoding='UTF-8') as f:

        data = json.load(f)



    new_dict = {"uri": [],"author":[],"created": [],"text":[]}

    for entrada in data:
      for key, value in entrada.items():
        if type(value) is str:

            # Eliminamos saltos y espacios en blanco

            value = value.strip().replace('\n', ' ').replace('\r', '')

        new_dict[key].append(value)

    df = pd.DataFrame(new_dict)

    df.to_csv(csv_file, index=False, encoding='UTF-8-sig')





if __name__ == "__main__":

    json_to_csv("yolandadiaz_bsky_social_posts.json", "salidayolanda.csv")