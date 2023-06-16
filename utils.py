MONTHS = {
    "հունվար": 1, "հունվարի": 1, "փետրվար": 2, "փետրվարի": 2, "մարտ": 3, "մարտի": 3,
    "ապրիլ": 4, "ապրիլի": 4, "մայիս": 5, "մայիսի": 5, "հունիս": 6, "հունիսի": 6,
    "հուլիս": 7, "հուլիսի": 7, "օգոստոս": 8, "օգոստոսի": 8, "սեպտեմբեր": 9, "սեպտեմբերի": 9,
    "հոկտեմբեր": 10, "հոկտեմբերի": 10, "նոյեմբեր": 11, "նոյեմբերի": 11, "դեկտեմբեր": 12, "դեկտեմբերի": 12,
}


def find_keyword(keywords, text):
    l_text = text.lower()
    for k in keywords:
        index = l_text.find(k.lower())
        if index >= 0:
            return index, k
    return -1, None


def extract_texts(container):
    all_texts = container.findAll(text=True)

    content = []
    for text in all_texts:
        stripped = text.strip()
        if stripped:
            content.append(stripped)

    return ' '.join(content)
