from django.conf import settings
import csv


# Read in the local CEDAR_dictionary to get captions and help-text.
cedar_forest_dict_path = settings.BASE_DIR / 'CEDAR_forest_dictionary.csv'

# Initialize lists for field names, help texts, and captions
field_names = []
field_helpt = []
field_captions = []

# Read the CSV file using the csv.reader function
with open(cedar_forest_dict_path, 'r', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        field_names.append(row['field'])
        field_helpt.append(row['description'])
        field_captions.append(row['caption'])

# Make dictionaries indexed by field names.
dict_help = dict(zip(field_names, field_helpt))
dict_capt = dict(zip(field_names, field_captions))

# Clean the data dict
for key in dict_help:
    if isinstance(dict_help[key], float):
        dict_help[key] = ''
    else:
        dict_help[key] = dict_help[key].replace('\xa0',' ')

# Clean the data dict
for key in dict_capt:
    if isinstance(dict_capt[key], float):
        dict_capt[key] = ''
    else:
        dict_capt[key] = dict_capt[key].replace('\xa0',' ')


def get_help_text(field_name, dict = dict_help):
    return(dict.get(field_name, "Missing Help Text"))
