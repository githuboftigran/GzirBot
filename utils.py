def is_keyword_in(keywords, text):
    for k in keywords:
        if k in text.lower():
            return True
    return False
