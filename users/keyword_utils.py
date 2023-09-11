SUFFIXES = {
    'ի': 'ու',
    'ուն': 'ան',
}

MAX_LETTERS_TO_TRIM = 2
MIN_LETTERS_TO_KEEP = 5


def get_similar_keywords(original_keyword):
    original_keyword = original_keyword.strip()
    similars = []
    for suffix, replacement in SUFFIXES.items():
        if original_keyword.endswith(suffix):
            similars.append(original_keyword[:-(len(suffix))] + replacement)
    if len(original_keyword) > MIN_LETTERS_TO_KEEP:
        available_letters_to_trim = len(original_keyword) - MIN_LETTERS_TO_KEEP
        for i in range(-min(MAX_LETTERS_TO_TRIM, available_letters_to_trim), 0):
            similars.append(original_keyword[:i])
    if ' ' in original_keyword:
        parts = original_keyword.split(' ')
        # Take only last 2 parts
        parts = parts[-2:]
        similars.append(f'{parts[0][0]}.{parts[1]}')
        similars.append(f'{parts[0][0]} {parts[1]}')
    # Ensure there are no duplicates
    return list(set(similars))
