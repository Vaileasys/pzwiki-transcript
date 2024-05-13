# dictionary to map cat/icon
CAT_REPLACEMENTS = {
    "Television": "tv",
    "Radio": "radio",
    "Amateur": "radio",
    "Military": "radio",
}

def replace_cat(cat):
    return CAT_REPLACEMENTS.get(cat, cat)