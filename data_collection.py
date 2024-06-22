import requests
from bs4 import BeautifulSoup


def process_name(name):
    if "(" in name:
        split = name.split("(")
        name = split[0].strip()
    return name


def get_compounds():
    compounds = {}
    html_doc = requests.get("https://en.wikipedia.org/wiki/List_of_inorganic_compounds").text
    soup = BeautifulSoup(html_doc, 'html.parser')
    main = soup.find("div", class_="mw-content-ltr mw-parser-output")
    new = main.find_all('li')
    for row in new:
        if " - " in row.text:
            split = row.text.split(" - ")
            name = process_name(split[0])
            equation = split[1]
            if len(name) < 30 and len(equation) < 20:
                compounds[name] = equation
            continue
        if " – " in row.text:
            split = row.text.split(" – ")
            name = process_name(split[0])
            equation = split[1]
            if len(name) < 30 and len(equation) < 20:
                compounds[name] = equation
            continue
        span = row.find('span')
        title = row.find('a').get("title")
        if span is None or title is None:
            continue
        if row.find("span").get("typeof") is not None:
            continue
        name = process_name(title)
        equation = span.text.strip()
        if len(name) < 30 and len(equation) < 20:
            compounds[name] = equation
    return compounds


def get_elements():
    elements = {}
    html_doc = requests.get("https://en.wikipedia.org/wiki/List_of_chemical_elements").text
    soup = BeautifulSoup(html_doc, 'html.parser')
    main = soup.find("table", class_="wikitable")
    new = main.find_all('tr')
    for row in new:
        column = row.find_all('td')
        if len(column) != 16:
            continue
        symbol = column[1].get_text().strip()
        name = column[2].get_text().strip()
        elements[symbol] = name
    return elements
