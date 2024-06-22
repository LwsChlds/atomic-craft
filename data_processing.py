def get_compound_components(formula):
    """
    This is a mess, but it works for now
    CO2 -> {'C': 1, 'O': 2}
    [Cu(NH3)4]SO4 -> {'Cu': 1, 'N': 4, 'H': 12,'S': 1, 'O': 4}
    """
    results = {}
    idx = 0
    number = 1
    brackets = False
    square_bracket = False
    substring = ""
    skip = False
    for i, letter in enumerate(formula):
        if "·" in formula:
            continue
        if skip:
            skip = False
            continue
        if letter == '[':
            square_bracket = True
            if i != 0 and idx != i:
                if number != 1:
                    offset = 1
                    if formula[i - offset - 1].isnumeric():
                        offset += 1
                    results[formula[idx:i - offset]] = results.get(formula[idx:i - offset], 0) + number
                    number = 1
                else:
                    results[formula[idx:i]] = results.get(formula[idx:i], 0) + number
            continue
        if formula[i - 1] == ']':
            square_bracket = False
            sub_values = get_compound_components(substring)
            for key, value in sub_values.items():
                if formula[i].isnumeric():
                    results[key] = results.get(key, 0) + value * int(formula[i])
                else:
                    results[key] = results.get(key, 0) + value
            substring = ""
            idx = i
            continue
        if square_bracket:
            if letter != "]":
                substring += letter
            continue

        if letter == '(':
            brackets = True
            if i != 0 and idx != i:
                if number != 1:
                    offset = 1
                    if formula[i - offset - 1].isnumeric():
                        offset += 1
                    results[formula[idx:i - offset]] = results.get(formula[idx:i - offset], 0) + number
                    number = 1
                else:
                    results[formula[idx:i]] = results.get(formula[idx:i], 0) + number
            continue
        if formula[i - 1] == ')':
            brackets = False
            sub_values = get_compound_components(substring)
            for key, value in sub_values.items():
                if formula[i].isnumeric():
                    results[key] = results.get(key, 0) + value * int(formula[i])
                else:
                    results[key] = results.get(key, 0) + value
            substring = ""
            idx = i + 1
            continue
        if brackets:
            if letter != ")":
                substring += letter
            continue
        if letter.isupper() and i != 0 and idx != i:
            if number != 1:
                offset = 1
                if formula[i - offset - 1].isnumeric():
                    offset += 1
                results[formula[idx:i - offset]] = results.get(formula[idx:i - offset], 0) + number
                number = 1
            else:
                results[formula[idx:i]] = results.get(formula[idx:i], 0) + number
            idx = i
        if letter.isnumeric():
            if i < len(formula) - 1:
                if formula[i + 1].isnumeric():
                    number = int(letter + formula[i + 1])
                    skip = True
                else:
                    number = int(letter)
            else:
                number = int(letter)
        if i == len(formula) - 1 and formula[i - 1] != ")" and formula[i - 1] != "]":
            if number != 1:
                results[formula[idx:-1]] = results.get(formula[idx:-1], 0) + number
                number = 1
            else:
                results[formula[idx:]] = results.get(formula[idx:], 0) + number
    return results
