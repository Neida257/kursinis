# Užduočių valdymo sistema

## 1. Įvadas

Šio kursinio darbo tikslas – sukurti objektinio programavimo principais paremtą Python programą. Pasirinkta tema – **užduočių valdymo sistema**, skirta užduotims kurti, peržiūrėti, redaguoti, šalinti, filtruoti, rūšiuoti ir saugoti faile.

Programa veikia terminale. Vartotojas gali pasirinkti veiksmus iš meniu, įvesti užduoties informaciją ir išsaugoti duomenis `tasks.json` faile.

### Kaip paleisti programą

1. Atsisiųskite arba nuklonuokite projektą iš GitHub.
2. Įsitikinkite, kad kompiuteryje įdiegtas Python 3.
3. Terminale atidarykite projekto aplanką.
4. Paleiskite programą:

```bash
python main.py
```

### Kaip naudotis programa

Paleidus programą pateikiamas meniu:

- pridėti naują užduotį;
- peržiūrėti visas užduotis;
- peržiūrėti vienos užduoties informaciją;
- pažymėti užduotį kaip atliktą;
- ištrinti užduotį;
- redaguoti užduotį;
- filtruoti pagal būseną arba prioritetą;
- ieškoti užduoties;
- rodyti vėluojančias užduotis;
- rūšiuoti pagal terminą arba prioritetą;
- išsaugoti duomenis ir išeiti.

---

## 2. Programos funkcionalumas

Programa įgyvendina šias pagrindines funkcijas:

| Funkcija | Aprašymas |
|---|---|
| Užduoties pridėjimas | Vartotojas įveda užduoties tipą, pavadinimą, aprašymą, prioritetą, terminą ir būseną. |
| Užduočių peržiūra | Programa parodo visas sukurtas užduotis. |
| Vienos užduoties informacija | Galima peržiūrėti konkrečios užduoties detales pagal ID. |
| Užduoties redagavimas | Leidžiama pakeisti pavadinimą, aprašymą, prioritetą ir terminą. |
| Užduoties ištrynimas | Užduotis pašalinama iš sąrašo. |
| Užduoties pažymėjimas kaip atliktos | Užduoties būsena pakeičiama į `Atlikta`. |
| Filtravimas | Užduotys filtruojamos pagal būseną arba prioritetą. |
| Paieška | Užduoties ieškoma pagal pavadinimą arba aprašymą. |
| Vėluojančios užduotys | Programa parodo užduotis, kurių terminas jau praėjo. |
| Rūšiavimas | Užduotys rūšiuojamos pagal terminą arba prioritetą. |
| Duomenų saugojimas | Užduotys išsaugomos `tasks.json` faile. |

---

## 3. Objektinio programavimo principai

### 3.1. Abstrakcija

Abstrakcija leidžia apibrėžti bendrą struktūrą, kurią turi įgyvendinti paveldinčios klasės. Programoje naudojama abstrakti klasė `BaseTask`, kuri turi du abstrakčius metodus:

```python
class BaseTask(ABC):
    @abstractmethod
    def to_dict(self):
        pass

    @abstractmethod
    def get_task_type(self):
        pass
```

Ši klasė nurodo, kad visos užduotys privalo turėti metodą duomenims paversti į žodyną ir metodą užduoties tipui gauti.

### 3.2. Paveldėjimas

Paveldėjimas leidžia vienai klasei perimti kitos klasės savybes ir metodus. Programoje klasė `Task` paveldi `BaseTask`, o `RegularTask` ir `UrgentTask` paveldi `Task`:

```python
class Task(BaseTask):
    ...

class RegularTask(Task):
    ...

class UrgentTask(Task):
    ...
```

Tokiu būdu paprastos ir skubios užduotys turi bendrą struktūrą, bet gali skirtingai apibrėžti savo tipą.

### 3.3. Polimorfizmas

Polimorfizmas leidžia skirtingoms klasėms turėti tą patį metodą, bet jį įgyvendinti skirtingai. Programoje metodas `get_task_type()` naudojamas tiek `RegularTask`, tiek `UrgentTask` klasėse:

```python
class RegularTask(Task):
    def get_task_type(self):
        return "Paprasta užduotis"

class UrgentTask(Task):
    def get_task_type(self):
        return "Skubi užduotis"
```

Kai programa spausdina užduotis, ji gali naudoti tą patį metodą, tačiau rezultatas priklauso nuo konkretaus objekto tipo.

### 3.4. Inkapsuliacija

Inkapsuliacija leidžia apsaugoti objekto duomenis ir kontroliuoti jų keitimą. Programoje naudojami privatūs atributai `_title`, `_priority`, `_status` ir `property` metodai:

```python
@property
def priority(self):
    return self._priority

@priority.setter
def priority(self, value):
    if value in ["žemas", "vidutinis", "aukštas"]:
        self._priority = value
```

Tai leidžia užtikrinti, kad prioritetas būtų pakeistas tik į leidžiamą reikšmę.

---

## 4. Dizaino šablonas

Programoje naudojamas **Factory Method** dizaino šablonas. Jis leidžia kurti skirtingų tipų užduotis per vieną bendrą metodą.

```python
class TaskFactory:
    @staticmethod
    def create_task(task_type, task_id, title, description, priority, deadline, status):
        if task_type == "skubi":
            return UrgentTask(task_id, title, description, priority, deadline, status)
        return RegularTask(task_id, title, description, priority, deadline, status)
```

Šis šablonas tinka programai, nes užduotys gali būti skirtingų tipų. Jeigu ateityje reikėtų pridėti naują užduoties tipą, pakaktų papildyti `TaskFactory` klasę, nekeičiant visos programos struktūros.

---

## 5. Kompozicija ir agregacija

Programoje naudojama agregacija: `TaskManager` klasė saugo daug `Task` objektų sąraše:

```python
class TaskManager:
    def __init__(self):
        self.tasks = []
```

`TaskManager` nėra pati užduotis, bet ji valdo užduočių kolekciją. Tai leidžia atskirti užduoties duomenis nuo veiksmų, atliekamų su užduočių sąrašu.

---

## 6. Skaitymas iš failo ir rašymas į failą

Programa naudoja JSON failą `tasks.json` duomenims saugoti.

### Rašymas į failą

```python
def save_to_file(self, filename="tasks.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            [task.to_dict() for task in self.tasks],
            file,
            ensure_ascii=False,
            indent=4
        )
```

### Skaitymas iš failo

```python
def load_from_file(self, filename="tasks.json"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        ...
    except FileNotFoundError:
        self.tasks = []
```

Tai leidžia išsaugoti programos būseną ir ją atkurti kitą kartą paleidus programą.

---

## 7. Testavimas

Pagrindinis funkcionalumas testuojamas naudojant `unittest` modulį. Testams skirtas failas:

```text
test_task_manager.py
```

Testais galima patikrinti, ar užduotys sukuriamos teisingai, ar veikia užduočių pridėjimas, paieška, būsenos keitimas, trynimas ir failų saugojimas.

Testų paleidimas:

```bash
python -m unittest test_task_manager.py
```

---

## 8. Projekto failai

```text
kursinis/
├── main.py
├── test_task_manager.py
├── tasks.json
└── README.md
```

| Failas | Paskirtis |
|---|---|
| `main.py` | Pagrindinis programos kodas. |
| `test_task_manager.py` | Vienetinių testų failas. |
| `tasks.json` | Užduočių duomenų saugojimo failas. |
| `README.md` | Kursinio darbo aprašas Markdown formatu. |

---

## 9. Rezultatai

- Sukurta terminale veikianti užduočių valdymo sistema.
- Programa leidžia pridėti, redaguoti, šalinti, filtruoti, ieškoti ir rūšiuoti užduotis.
- Įgyvendinti keturi objektinio programavimo principai: abstrakcija, paveldėjimas, polimorfizmas ir inkapsuliacija.
- Pritaikytas Factory Method dizaino šablonas.
- Duomenys išsaugomi ir nuskaitomi iš JSON failo.

---

## 10. Išvados

Šio kursinio darbo metu buvo sukurta užduočių valdymo sistema, kuri praktiškai pritaiko objektinio programavimo principus. Programa turi aiškią klasių struktūrą, leidžia valdyti skirtingų tipų užduotis ir saugo duomenis faile. Darbo metu buvo pritaikytas Factory Method dizaino šablonas, kuris leidžia patogiai kurti skirtingų tipų užduotis.

Ateityje programą būtų galima išplėsti pridedant grafinę vartotojo sąsają, vartotojų prisijungimą, priminimus apie artėjančius terminus arba duomenų saugojimą duomenų bazėje.

---

## 11. Naudoti šaltiniai

- Python dokumentacija
- `unittest` dokumentacija
- Markdown sintaksės gairės
- PEP8 Python kodo stiliaus gairės
