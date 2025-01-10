from datetime import datetime

class Task:
    def __init__(self, name, priority, due_date=None):
        self.name = name
        self.priority = priority
        self.is_completed = False
        self.due_date = due_date

    def __str__(self):
        status = "completed" if self.is_completed else "Pending"
        due_date_str = self.due_date.strftime("%Y-%m-%d") if self.due_date else "No due date"
        return f"{self.name} - {self.priority.capitalize()} Priority - {status} - Due: {due_date_str}"

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self):
        name = input("Enter Task Name: ").strip()
        priority = input("Enter Task Priority [high, medium, low]: ").strip().lower()
        due_date_str = input("Enter Due Date (YYYY-MM-DD) [optional]: ").strip()

        if priority not in {"high", "medium", "low"}:
            print("Invalid Priority. Task not added.")
            return

        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
            except ValueError:
                print("Invalid date format. Task not added.")
                return

        self.tasks.append(Task(name, priority, due_date))
        print(f"Task '{name}' added successfully!")

    def view_tasks(self):
        print("\n=== Task List ===")
        if not self.tasks:
            print("No tasks found!")
            return
        
        sorted_tasks = sorted(
            self.tasks,
            key=lambda t: (
                t.priority == "high",
                t.priority == "medium",
                not t.is_completed,
            ),
            reverse=True,
        )

        for index, task in enumerate(sorted_tasks, start=1):
            print(f"{index}. {task}")

    def mark_task_completed(self):
        self.view_tasks()
        if not self.tasks:
            return
        
        name = input("\nEnter the task name to mark as completed: ").strip()
        task = next((t for t in self.tasks if t.name.lower() == name.lower()), None)

        if task is None:
            print("Task not found!")
            return
        
        if task.is_completed:
            print("Task is already completed!")
            return
        else:
            task.is_completed = True
            print(f"Task '{task.name}' marked as completed!")

    def remove_task(self):
        self.view_tasks()
        if not self.tasks:
            return

        try:
            task_number = int(input("\nEnter the task number to remove: ").strip())
            if task_number < 1 or task_number > len(self.tasks):
                print("Invalid task number!")
                return

            task = self.tasks.pop(task_number - 1)
            print(f"Task '{task.name}' removed successfully!")
        except ValueError:
            print("Invalid input! Please enter a valid task number.")

    def main_menu(self):
        while True:
            print("\n=== Task Manager ===")
            print("1. Add Task")
            print("2. View Tasks")
            print("3. Mark Task as Completed")
            print("4. Remove Task")
            print("5. Exit")

            choice = input("Enter your choice: ").strip()
            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.view_tasks()
            elif choice == "3":
                self.mark_task_completed()
            elif choice == "4":
                self.remove_task()
            elif choice == "5":
                print("Good Bye! Exiting Task Manager...")
                break
            else:
                print("Invalid Choice. Please try again.")


if __name__ == "__main__":
    task_manager = TaskManager()
    task_manager.main_menu()
