import datetime

# This tells the program what date to use when figuring out an animal's birthday based on the season
SEASON_TO_MONTH_DAY = {
    "spring": (3, 21),
    "summer": (6, 21),
    "fall":   (9, 21),
    "autumn": (9, 21),
    "winter": (12, 21),
    "unknown": (1, 1)  # if we don't know the season, use January 1st
}

# These are short codes that stand for each animal type
SPECIES_PREFIX = {
    "hyena": "Hy",
    "lion": "Li",
    "tiger": "Ti",
    "bear": "Be"
}

HABITATS = {}

# Read names from the name list and save them for later use
names_queue = {}
names_queue["default"] = []
with open("animalNames.txt", "r") as f:
    for name in f:
        name = name.strip()
        names_queue["default"].append(name)  # use this list if we don't separate names by species

# Keep track of how many animals we've seen for each type
id_counters = {}

def gen_birth_date(season, age):
    today = datetime.date.today()
    year_of_birth = today.year - age
    if season.lower() in SEASON_TO_MONTH_DAY:
        month, day = SEASON_TO_MONTH_DAY[season.lower()]
    else:
        month, day = SEASON_TO_MONTH_DAY["unknown"]
    return datetime.date(year_of_birth, month, day).isoformat()

def gen_unique_id(species):
    if species not in id_counters:
        id_counters[species] = 1
    else:
        id_counters[species] += 1
    prefix = "XX"
    if species.lower() in SPECIES_PREFIX:
        prefix = SPECIES_PREFIX[species.lower()]
    return "{}{:02d}".format(prefix, id_counters[species])

def parse_animal_line(line):
    parts = line.strip().split(",")
    base_info = parts[0].split(" ")
    age = int(base_info[0])
    sex = base_info[3]
    species = base_info[4].lower()
    if "born in" in parts[0]:
        season = base_info[-1].lower()
    else:
        season = "unknown"
    color = parts[1].strip().replace("color", "").strip()
    weight = parts[2].strip()
    origin = parts[3].strip()
    return age, sex, species, season, color, weight, origin

zoo_output = []
with open("arrivingAnimals.txt", "r") as f:
    for line in f:
        age, sex, species, season, color, weight, origin = parse_animal_line(line)
        if len(names_queue["default"]) > 0:
            name = names_queue["default"].pop(0)
        else:
            name = "NoName"
        unique_id = gen_unique_id(species)
        birth_date = gen_birth_date(season, age)
        arrival_date = datetime.date.today().isoformat()

        record = "{}; {}; birth date: {}; {}; {}; {}; {}; arrived {}".format(
            unique_id, name, birth_date, color, sex, weight, origin, arrival_date)

        if species.capitalize() not in HABITATS:
            HABITATS[species.capitalize()] = []
        HABITATS[species.capitalize()].append(record)

# Write all animal information into a final file that shows where they live and their details
with open("zooPopulation.txt", "w") as out:
    for species in ["Hyena", "Lion", "Tiger", "Bear"]:
        out.write("{} Habitat:\n\n".format(species))
        if species in HABITATS:
            for animal in HABITATS[species]:
                out.write(animal + "\n")
        out.write("\n")

print("Zoo population report generated: zooPopulation.txt")
