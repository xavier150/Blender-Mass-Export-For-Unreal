from typing import List, Tuple
from . import config

def get_export_list() -> List[Tuple[str, str]]:
    export_dict = config.get_export_items()

    print("Choisissez les dossiers à exporter :")
    choices_list = list(export_dict.keys())
    for i, choice_name in enumerate(choices_list, start=1):
        print(f"[{i}] {choice_name}")

    export_input = input("Saisissez le(s) numéro(s) correspondant(s) aux dossiers à exporter (séparez-les par des virgules) : ")

    export_list: List[Tuple[str, str]] = []
    choices = export_input.split(",")
    for choice in choices:
        try:
            index = int(choice.strip())
            if 1 <= index <= len(export_dict) + 1:
                key = choices_list[index - 1]
                export_list.extend(export_dict[key])
            else:
                print(f"Choix invalide : {choice}")
        except ValueError:
            print(f"Valeur invalide : {choice}")

    return export_list