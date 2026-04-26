import unittest

from main import TaskFactory, TaskManager


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.manager = TaskManager()

        self.task = TaskFactory.create_task(
            task_type="paprasta",
            task_id=1,
            title="Testinė užduotis",
            description="Aprašymas",
            priority="aukštas",
            deadline="2026-05-10",
            status="Neatlikta"
        )

    def test_add_task(self):
        self.manager.tasks.append(self.task)
        self.assertEqual(len(self.manager.tasks), 1)

    def test_find_task_by_id(self):
        self.manager.tasks.append(self.task)
        found_task = self.manager.find_task_by_id(1)
        self.assertIsNotNone(found_task)
        self.assertEqual(found_task.title, "Testinė užduotis")

    def test_mark_as_done(self):
        self.manager.tasks.append(self.task)
        self.manager.mark_as_done(1)
        self.assertEqual(self.task.status, "Atlikta")

    def test_delete_task(self):
        self.manager.tasks.append(self.task)
        self.manager.delete_task(1)
        self.assertEqual(len(self.manager.tasks), 0)

    def test_factory_creates_urgent_task(self):
        urgent_task = TaskFactory.create_task(
            task_type="skubi",
            task_id=2,
            title="Skubi užduotis",
            description="Svarbu",
            priority="aukštas",
            deadline="2026-05-11",
            status="Neatlikta"
        )

        self.assertEqual(urgent_task.get_task_type(), "Skubi užduotis")


if __name__ == "__main__":
    unittest.main()