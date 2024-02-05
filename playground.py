from bs4 import BeautifulSoup


with open("index.html") as file:
    html = file.read()

soup = BeautifulSoup(html, "html.parser")

# 1.extracting title
title_soup = soup.select_one(".sc-irLvIq")
TITLE = title_soup and title_soup.text.strip() or ""
print(f"Title: {TITLE}")

# 2.extracting overview

description_soup = soup.select_one("#abstract .sc-eEPhau")
OVERVIEW = ""
if description_soup:
    paragraphs = description_soup.find_all("p")
    OVERVIEW = " \n".join(f"{p.text.strip()} \n" for p in paragraphs)

# print(f"OVERVIEW:\n {OVERVIEW}")

# 3.extracting description

description_soup = soup.select_one("#description ")
DESCRIPTION = ""
if description_soup:
    paragraphs = description_soup.select("p, h2")
    DESCRIPTION = " \n".join(
        f"{p.text.strip()} \n" for p in paragraphs)

print(f"DESCRIPTION:\n {DESCRIPTION}")

# 4.extracting evaluation

evaluation_soup = soup.select_one("#evaluation")
EVALUATION = ""
if evaluation_soup:
    paragraphs = evaluation_soup.select("p, h2 , .uc-code-block code")
    EVALUATION = " \n".join(
        f"{p.text.strip()}" for p in paragraphs)
print(f"EVALUATION:\n {EVALUATION}")
