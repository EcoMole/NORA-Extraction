import typing

class DataStore():
    def __init__(self):
        self.categories_2015_2283 = {
        "modified molecular structure": "Modified molecular structure",
        "produced from microorganisms, fungi or algae": "Microorganisms, fungi or algae",
        "from plants or their parts": "Plants",
        "from plants and their parts": "Plants",
        "new production process": "Production process",
        "ood resulting from a production process not used" : "Production process",
        "from animals or their parts": "Animals",
        "vitamins and minerals from": "Vitamins and minerals",
        "vitamins, minerals": "Vitamins and minerals",
        "of mineral origin": "Mineral origin",
        "cell or tissue culture derived": "Cell and tissue",
        "cell culture or tissue": "Cell and tissue",
        "food consisting of engineered nanomaterial": "Nanomaterials",
        "exclusive use in food supplement prior": "Food supplement prior",
        "vitamins, minerals and other substances": "Vitamins and minerals",
        }   

        self.categories_97_618 = { # The reasoning behind class and category is that we dont want to capture the sole number
        "class 1.1": "1.1 (Chemicals)", # also sometimes mentioned as sub-class
        "class 1.2": "1.2 (Chemicals)",
        "class 2.1": "2.1 (Complex NF)",
        "class 2.2": "2.2 (Complex NF)",
        "class 3.1": "3.1 (Plants)", 
        "class 3.2": "3.2 (Plants)",
        "class 4.1": "4.1 (Animals)",
        "class 4.2": "4.2 (Animals)",
        "class 5.1": "5.1 (Microogranisms)",
        "class 5.2": "5.2 (Microorganisms)",
        "class 6": "6 (Production process)",
        "category 1.1": "1.1 (Chemicals)", # also sometimes mentioned as sub-category
        "category 1.2": "1.2 (Chemicals)",
        "category 2.1": "2.1 (Complex NF)",
        "category 2.2": "2.2 (Complex NF)",
        "category 3.1": "3.1 (Plants)",  
        "category 3.2": "3.2 (Plants)",
        "category 4.1": "4.1 (Animals)",
        "category 4.2": "4.2 (Animals)",
        "category 5.1": "5.1 (Microogranisms)",
        "category 5.2": "5.2 (Microorganisms)",
        "category 6": "6 (Production process)",
        }

        self.categories_258_97 = {
        "category a": "a (from GMO)",
        "category b": "b (non GMO)",
        "category c": "c (Molecular structure)",
        "category d": "d (Microogranisms)",
        "category e": "e (Plants)",
        "category f": "f (Production process)",
        }

        self.SO_names = {
        ("Reinhard", "Ackerl"),
        ("Ana Luisa", "Afonso"),
        ("Océane", "Albert"),
        ("Mathias Rudolf", "Amundsen"),
        ("Michele", "Ardizzone"),
        ("Domenico", "Azzollini"),
        ("Elisa", "Beneventi"),
        ("Victor", "Bunea"),
        ("Paolo", "Colombo"),
        ("Ionut", "Craciun"),
        ("Giacomo", "de sanctis"),
        ("Agnès", "de sesmaisons"),
        ("Aikaterini", "Doulgeridou"),
        ("Céline", "Dumas"),
        ("Lucia", "Fabiani"),
        ("Antonio", "Fernandez"),
        ("Antonio", "Dumont"),
        ("Lucien", "Ferreira"),
        ("Lucien", "Da Costa"),
        ("Thibault", "Fiolet"),
        ("Esther", "Garcia"),
        ("Esther", "Ruiz"),
        ("Wolfgang", "Gelbmann"),
        ("Andrea", "Gennaro"),
        ("Andrea", "Germini"),
        ("Maria", "Glymenaki"),
        ("Tilemachos", "Goumperis"),
        ("Paschalina", "Grammatikou"),
        ("Leng", "Heng"),
        ("Sara", "Jacchia"),
        ("Dafni", "Kagkli"),
        ("Nena", "Karavasiloglou"),
        ("Georges", "Kass"),
        ("Eirini", "Kouloura"),
        ("Marcello", "Laganaro"),
        ("Paolo", "Lenzi"),
        ("Aleksandra", "Lewandowska"),
        ("Maura", "Magani"),
        ("Ana", "Martin Camargo"),
        ("Leonard", "Matijevic"),
        ("Vania", "Mendes"),
        ("Alejandra", "Muñoz Gonzalez"),
        ("Franco", "Neri"),
        ("Estefania", "Noriega"),
        ("Estefania", "Fernandez"),
        ("Irene", "Nuin"),
        ("Nikoletta", "Papadopoulou"),
        ("Pietro", "Piffanelli"),
        ("Gabriela", "Precup"),
        ("Tommaso", "Raffaello"),
        ("Fernando", "Rivero Pino"),
        ("Pablo", "Rodriguez"),
        ("Pablo", "Fernandez"),
        ("Ruth", "Roldan Torres"),
        ("Annamaria", "Rossi"),
        ("Reinhilde", "Schoonjans"),
        ("Qingqing", "Sun"),
        ("Francesco", "Suriano"),
        ("Roman", "Svejstil"),
        ("Ariane", "Titz"),
        ("Emanuela", "Turla"),
        ("Silvia", "Valtueña Martinez"),
        ("Ermolaos", "Ververis"),
        ("Panagiota", "Zakidou"),
        }

    def get_categories(self, directive: str) -> typing.Dict[str, str]:
        if directive == "2015/2283":
            return self.categories_2015_2283
        elif directive == "97/618":
            return self.categories_97_618
        elif directive == "258/97":
            return self.categories_258_97
        else:
            return None
        
    def get_officers(self) -> typing.Set[str]:
        return self.SO_names
