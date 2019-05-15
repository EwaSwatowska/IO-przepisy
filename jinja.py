import tempfile
import webbrowser
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('./templates'),
    autoescape=select_autoescape(['html'])
)

env.globals['project_path'] = Path(__file__).parent.absolute()

strona="przepis"

lista = ["jabłko", "cebula", "kurczak"]

template = env.get_template(strona + ".html")

title2 = "Nazwa przepisu"

text1 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore " \
        "magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea " \
        "commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat " \
        "nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit " \
        "anim id est laborum. "

src = "kitek.jpg"

class przepis:
    def __init__(self, link, nazwa):
        self.link=link
        self.nazwa=nazwa

p1=przepis("#","Jabłko pieczone")

przepisy = [p1]

skladniki =    [{"ilosc":"1", "reszta":"marchewka"},
                {"ilosc":"2", "reszta":"pomidor"},
                {"ilosc":"3", "reszta":"ziemniak"}]

result = template.render(title="Znajdź przepis", lista=lista, text1=text1, text2=text1.upper(), title2=title2, src=src, przepisy=przepisy, skladniki=skladniki, strona=strona).encode("utf-8")

tmp = tempfile.NamedTemporaryFile(delete=False)
path = tmp.name + '.html'
f = open(path, 'wb')
f.write(result)
f.close()

webbrowser.open(path)
