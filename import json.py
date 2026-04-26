import json
from dataclasses import dataclass, asdict
from datetime import datetime


# =========================
# SPALVOS TERMINALUI
# =========================

class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    END = "\033[0m"


# =========================
# UŽDUOTIES KLASĖ
# =========================

@dataclass
class Task:
    task_id: int
    title: str
    description: str
    priority: str
    deadline: str
    status: str = "Neatlikta"

    def to_dict(self):
        return asdict(self)


# =========================
# UŽDUOČIŲ VALDYMO KLASĖ
# =========================

class TaskManager:
    def __init__(self):
        self.tasks = []

    def get_next_id(self):
        if not self.tasks:
            return 1
        return max(task.task_id for task in self.tasks) + 1

    def add_task(self, task):
        self.tasks.append(task)
        self.save_to_file()
        print_success("Užduotis sėkmingai pridėta.")

    def find_task_by_id(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def show_tasks(self):
        print_header("VISOS UŽDUOTYS")

        if not self.tasks:
            print_info("Užduočių nėra.")
            return

        for task in self.tasks:
            print_task(task)

    def show_task_details(self, task_id):
        task = self.find_task_by_id(task_id)

        if task:
            print_header("UŽDUOTIES INFORMACIJA")
            print_task(task, detailed=True)
        else:
            print_error("Užduotis su tokiu ID nerasta.")

    def mark_as_done(self, task_id):
        task = self.find_task_by_id(task_id)

        if task:
            task.status = "Atlikta"
            self.save_to_file()
            print_success("Užduotis pažymėta kaip atlikta.")
        else:
            print_error("Užduotis su tokiu ID nerasta.")

    def delete_task(self, task_id):
        task = self.find_task_by_id(task_id)

        if task:
            self.tasks.remove(task)
            self.save_to_file()
            print_success("Užduotis sėkmingai ištrinta.")
        else:
            print_error("Užduotis su tokiu ID nerasta.")

    def edit_task(self, task_id):
        task = self.find_task_by_id(task_id)

        if not task:
            print_error("Užduotis su tokiu ID nerasta.")
            return

        print_header("UŽDUOTIES REDAGAVIMAS")
        print_info("Palikite lauką tuščią, jei nenorite jo keisti.")

        new_title = input_colored("Naujas pavadinimas: ")
        new_description = input_colored("Naujas aprašymas: ")
        new_priority = input_colored("Naujas prioritetas (žemas / vidutinis / aukštas): ").lower()
        new_deadline = input_colored("Naujas terminas (YYYY-MM-DD): ")

        if new_title:
            task.title = new_title

        if new_description:
            task.description = new_description

        if new_priority:
            if new_priority in ["žemas", "vidutinis", "aukštas"]:
                task.priority = new_priority
            else:
                print_error("Prioritetas nepakeistas, nes įvesta neteisinga reikšmė.")

        if new_deadline:
            if is_valid_date(new_deadline):
                task.deadline = new_deadline
            else:
                print_error("Terminas nepakeistas, nes data įvesta neteisingu formatu.")

        self.save_to_file()
        print_success("Užduotis atnaujinta.")

    def filter_by_status(self, status):
        filtered_tasks = [
            task for task in self.tasks
            if task.status.lower() == status.lower()
        ]

        print_header(f"UŽDUOTYS PAGAL BŪSENĄ: {status}")
        self.show_filtered_tasks(filtered_tasks)

    def filter_by_priority(self, priority):
        filtered_tasks = [
            task for task in self.tasks
            if task.priority.lower() == priority.lower()
        ]

        print_header(f"UŽDUOTYS PAGAL PRIORITETĄ: {priority}")
        self.show_filtered_tasks(filtered_tasks)

    def search_tasks(self, keyword):
        found_tasks = [
            task for task in self.tasks
            if keyword.lower() in task.title.lower()
            or keyword.lower() in task.description.lower()
        ]

        print_header(f"PAIEŠKOS REZULTATAI: {keyword}")
        self.show_filtered_tasks(found_tasks)

    def show_overdue_tasks(self):
        today = datetime.today().date()

        overdue_tasks = [
            task for task in self.tasks
            if datetime.strptime(task.deadline, "%Y-%m-%d").date() < today
            and task.status != "Atlikta"
        ]

        print_header("VĖLUOJANČIOS UŽDUOTYS")
        self.show_filtered_tasks(overdue_tasks)

    def sort_by_deadline(self):
        sorted_tasks = sorted(
            self.tasks,
            key=lambda task: datetime.strptime(task.deadline, "%Y-%m-%d")
        )

        print_header("UŽDUOTYS SURŪŠIUOTOS PAGAL TERMINĄ")
        self.show_filtered_tasks(sorted_tasks)

    def sort_by_priority(self):
        priority_order = {
            "aukštas": 1,
            "vidutinis": 2,
            "žemas": 3
        }

        sorted_tasks = sorted(
            self.tasks,
            key=lambda task: priority_order.get(task.priority.lower(), 4)
        )

        print_header("UŽDUOTYS SURŪŠIUOTOS PAGAL PRIORITETĄ")
        self.show_filtered_tasks(sorted_tasks)

    def show_filtered_tasks(self, filtered_tasks):
        if not filtered_tasks:
            print_info("Užduočių pagal pasirinktą kriterijų nėra.")
            return

        for task in filtered_tasks:
            print_task(task)

    def save_to_file(self, filename="tasks.json"):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                [task.to_dict() for task in self.tasks],
                file,
                ensure_ascii=False,
                indent=4
            )

    def load_from_file(self, filename="tasks.json"):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)

                self.tasks = []

                for i, item in enumerate(data, start=1):
                    task = Task(
                        task_id=item.get("task_id", i),
                        title=item.get("title", "Be pavadinimo"),
                        description=item.get("description", "Nėra aprašymo"),
                        priority=item.get("priority", "žemas"),
                        deadline=item.get("deadline", "2026-01-01"),
                        status=item.get("status", "Neatlikta")
                    )

                    self.tasks.append(task)

        except FileNotFoundError:
            self.tasks = []

        except json.JSONDecodeError:
            self.tasks = []
            print_error("Nepavyko nuskaityti tasks.json failo. Failas gali būti sugadintas.")


# =========================
# IŠVEDIMO FUNKCIJOS
# =========================

def print_line():
    print(Colors.BLUE + "-" * 70 + Colors.END)


def print_header(title):
    print("\n" + Colors.HEADER + "=" * 70 + Colors.END)
    print(Colors.BOLD + Colors.CYAN + title.center(70) + Colors.END)
    print(Colors.HEADER + "=" * 70 + Colors.END)


def print_success(message):
    print(Colors.GREEN + f"\n✅ {message}" + Colors.END)


def print_error(message):
    print(Colors.RED + f"\n❌ {message}" + Colors.END)


def print_info(message):
    print(Colors.YELLOW + f"\nℹ️  {message}" + Colors.END)


def input_colored(message):
    return input(Colors.BOLD + Colors.CYAN + message + Colors.END).strip()


def color_priority(priority):
    if priority.lower() == "aukštas":
        return Colors.RED + priority + Colors.END
    elif priority.lower() == "vidutinis":
        return Colors.YELLOW + priority + Colors.END
    elif priority.lower() == "žemas":
        return Colors.GREEN + priority + Colors.END
    return priority


def color_status(status):
    if status.lower() == "atlikta":
        return Colors.GREEN + status + Colors.END
    elif status.lower() == "vykdoma":
        return Colors.YELLOW + status + Colors.END
    elif status.lower() == "neatlikta":
        return Colors.RED + status + Colors.END
    return status


def print_task(task, detailed=False):
    print_line()
    print(f"{Colors.BOLD}ID:{Colors.END}          {task.task_id}")
    print(f"{Colors.BOLD}Pavadinimas:{Colors.END} {task.title}")
    print(f"{Colors.BOLD}Prioritetas:{Colors.END} {color_priority(task.priority)}")
    print(f"{Colors.BOLD}Būsena:{Colors.END}      {color_status(task.status)}")
    print(f"{Colors.BOLD}Terminas:{Colors.END}    {task.deadline}")

    if detailed:
        print(f"{Colors.BOLD}Aprašymas:{Colors.END}   {task.description}")

    print_line()


# =========================
# ĮVEDIMO TIKRINIMO FUNKCIJOS
# =========================

def is_valid_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def choose_deadline():
    while True:
        deadline = input_colored("Terminas (YYYY-MM-DD): ")

        if is_valid_date(deadline):
            return deadline

        print_error("Datą įveskite formatu YYYY-MM-DD, pvz. 2026-05-10.")


def choose_priority():
    priorities = ["žemas", "vidutinis", "aukštas"]

    while True:
        priority = input_colored("Prioritetas (žemas / vidutinis / aukštas): ").lower()

        if priority in priorities:
            return priority

        print_error("Pasirinkite: žemas, vidutinis arba aukštas.")


def choose_status():
    statuses = {
        "neatlikta": "Neatlikta",
        "vykdoma": "Vykdoma",
        "atlikta": "Atlikta"
    }

    while True:
        status = input_colored("Būsena (neatlikta / vykdoma / atlikta): ").lower()

        if status in statuses:
            return statuses[status]

        print_error("Pasirinkite: neatlikta, vykdoma arba atlikta.")


def get_number(message):
    while True:
        try:
            return int(input_colored(message))
        except ValueError:
            print_error("Įveskite skaičių.")


# =========================
# MENIU
# =========================

def show_menu():
    print_header("UŽDUOČIŲ VALDYMO SISTEMA")

    print(Colors.BOLD + "Pasirinkite veiksmą:" + Colors.END)
    print()
    print(Colors.CYAN + "1. " + Colors.END + "Pridėti naują užduotį")
    print(Colors.CYAN + "2. " + Colors.END + "Peržiūrėti visas užduotis")
    print(Colors.CYAN + "3. " + Colors.END + "Peržiūrėti vienos užduoties informaciją")
    print(Colors.CYAN + "4. " + Colors.END + "Pažymėti užduotį kaip atliktą")
    print(Colors.CYAN + "5. " + Colors.END + "Ištrinti užduotį")
    print(Colors.CYAN + "6. " + Colors.END + "Redaguoti užduotį")
    print(Colors.CYAN + "7. " + Colors.END + "Filtruoti pagal būseną")
    print(Colors.CYAN + "8. " + Colors.END + "Filtruoti pagal prioritetą")
    print(Colors.CYAN + "9. " + Colors.END + "Ieškoti užduoties")
    print(Colors.CYAN + "10." + Colors.END + " Rodyti vėluojančias užduotis")
    print(Colors.CYAN + "11." + Colors.END + " Rūšiuoti pagal terminą")
    print(Colors.CYAN + "121." + Colors.END + " Išsaugoti ir išeiti")

    print_line()


# =========================
# PAGRINDINĖ PROGRAMA
# =========================

def main():
    manager = TaskManager()
    manager.load_from_file()

    while True:
        show_menu()

        choice = input_colored("Pasirinkite veiksmą: ")

        if choice == "1":
            print_header("NAUJOS UŽDUOTIES PRIDĖJIMAS")

            title = input_colored("Užduoties pavadinimas: ")
            description = input_colored("Aprašymas: ")
            priority = choose_priority()
            deadline = choose_deadline()
            status = choose_status()

            task = Task(
                task_id=manager.get_next_id(),
                title=title,
                description=description,
                priority=priority,
                deadline=deadline,
                status=status
            )

            manager.add_task(task)

        elif choice == "2":
            manager.show_tasks()

        elif choice == "3":
            manager.show_tasks()
            task_id = get_number("\nĮveskite užduoties ID: ")
            manager.show_task_details(task_id)

        elif choice == "4":
            manager.show_tasks()
            task_id = get_number("\nĮveskite užduoties ID: ")
            manager.mark_as_done(task_id)

        elif choice == "5":
            manager.show_tasks()
            task_id = get_number("\nĮveskite užduoties ID: ")
            manager.delete_task(task_id)

        elif choice == "6":
            manager.show_tasks()
            task_id = get_number("\nĮveskite užduoties ID: ")
            manager.edit_task(task_id)

        elif choice == "7":
            status = choose_status()
            manager.filter_by_status(status)

        elif choice == "8":
            priority = choose_priority()
            manager.filter_by_priority(priority)

        elif choice == "9":
            keyword = input_colored("\nĮveskite paieškos žodį: ")
            manager.search_tasks(keyword)

        elif choice == "10":
            manager.show_overdue_tasks()

        elif choice == "11":
            manager.sort_by_deadline()

        elif choice == "12":
            manager.sort_by_priority()

        elif choice == "13":
            manager.save_to_file()
            print_success("Duomenys išsaugoti. Programa baigta.")
            break

        else:
            print_error("Neteisingas pasirinkimas. Bandykite dar kartą.")


main()