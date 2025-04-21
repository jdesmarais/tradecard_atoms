from csv import DictReader
import os
from pathlib import Path

from alive_progress import alive_bar
from unidecode import unidecode

from generate_card import generate_tradecard_image

def str_round(str:str, nb:int):
    try :
        convert = f"{round(float(str.replace(',','.')),2)}"
    except:
        convert = str
    return convert

def generate_tradecard_image_from_csv(
    csv_filepath,
    background_img_filepath,
    atom_img_dirpath,
    picto_img_filepath,
    output_dirpath,
    show_result=False,
    save=True):

    # output dir
    if save:
        if os.path.exists(output_dirpath):
            if not os.path.isdir(output_dirpath):
                raise Exception(f"The output path {output_dirpath} exists but is not a directory, please fix it")
        else :
            os.mkdir(output_dirpath)

    # read CSV
    with open(csv_filepath, 'r') as csv_file:
        reader = DictReader(csv_file)

        # verify that the right colmns are found
        expected_columns = ["numero_atomique",
                            "symbole",
                            "nom",
                            "famille_d_element",
                            "masse_atomique",
                            "point_de_fusion_[°C]",
                            "point_d_ebullition_[°C]",
                            "date_de_decouverte",
                            "decouvert_par",
                            "description"]

        if not set(expected_columns).issubset(set(reader.fieldnames)):
            raise Exception(f"Missing columns in {csv_filepath} : we are expecting {expected_columns}, we have {reader.fieldnames}")
        
        picto_color_map = {
            "alcalin" : (255,18,85),
            "alcalino-terreux" : (250,117,0),
            "lanthanide" : (57,60,130),
            "actinide" : (71,90,255),
            "métal de transition" : (52,167,104),
            "métal de post-transition" : (102,59,59),
            "metalloïde" : (17,59,59),
            "autre non-métal" : (15,178,0),
            "non-métal" : (15,178,0),
            "halogène" : (216,171,33),
            "gaz noble" : (155,0,187),
            "non classé" : (104,105,113)
        }

        # loop over the CSV lines and generate one card per CSV line
        rows = list(reader)
        nb_rows = len(rows)

        exports = []

        with alive_bar(nb_rows) as bar:

            for row in rows:

                number = row["numero_atomique"]
                name = row["nom"]
                symbol = row["symbole"]
                subgroup = row["famille_d_element"]
                mass = str_round(row["masse_atomique"], 2)
                melt_temperature = str_round(row["point_de_fusion_[°C]"], 2)
                vapor_temperature = str_round(row["point_d_ebullition_[°C]"], 2)
                discovery_year = row["date_de_decouverte"]
                #discovered_by = row["decouvert_par"]
                description = row["description"]

                atom_img_filepath = atom_img_dirpath / Path(f"{unidecode(name)}.png")
                atom_title = f"{name.capitalize()} ({symbol})"
                atom_subgroup_title = f"{subgroup.capitalize()}"
                atom_kpis = [f"{number}", f"{mass} u", f"{melt_temperature} °C", f"{vapor_temperature} °C", f"{discovery_year}"]

                if subgroup not in picto_color_map:
                    print(f"-- Cannot find picto color for {name} : {subgroup} - Skipped")
                    continue

                picto_color = picto_color_map[subgroup]

                output_path = output_dirpath / Path(f"{unidecode(name)}.png")

                if not os.path.isfile(atom_img_filepath):
                    print(f"-- Cannot find image for {name} : {atom_img_filepath} - Skipped")
                    continue

                img = generate_tradecard_image(
                    background_img_filepath,
                    atom_img_filepath,
                    atom_title,
                    atom_subgroup_title,
                    picto_img_filepath,
                    picto_color,
                    atom_kpis,
                    description)

                if show_result:
                    img.show()

                if save:
                    img.save(output_path)
                    print(f"{name} : Card image saved to {output_path}")

                exports.append({"number": number, "atom": name, "symbol": symbol, "path": output_path})

                bar()

if __name__ == "__main__":
    csv_filepath = "assets/periodic_table_atoms.csv"
    background_img_filepath = "assets/background.png"
    atom_img_dirpath = "assets/img"
    picto_img_filepath = "assets/picto.png"
    output_dirpath="outputs"

    show_result = False
    save = True

    generate_tradecard_image_from_csv(
        csv_filepath,
        background_img_filepath,
        atom_img_dirpath,
        picto_img_filepath,
        output_dirpath,
        show_result=show_result,
        save=save)