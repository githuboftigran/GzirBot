SUFFIXES = {
    'ի': 'ու',
    'ուն': 'ան',
}

MAX_LETTERS_TO_TRIM = 2
MIN_LETTERS_TO_KEEP = 5


def get_similar_keywords(original_keyword):
    similars = []
    for suffix, replacement in SUFFIXES.items():
        if original_keyword.endswith(suffix):
            similars.append(original_keyword[:-(len(suffix))] + replacement)
    if len(original_keyword) > MIN_LETTERS_TO_KEEP:
        available_letters_to_trim = len(original_keyword) - MIN_LETTERS_TO_KEEP
        for i in range(-min(MAX_LETTERS_TO_TRIM, available_letters_to_trim), 0):
            similars.append(original_keyword[:i])
    # Ensure there are no duplicates
    return list(set(similars))