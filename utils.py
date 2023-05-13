def is_keyword_in(keywords, text):
    for k in keywords:
        if k in text:
            return True
    return False
