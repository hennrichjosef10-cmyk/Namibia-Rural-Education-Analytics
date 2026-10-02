import abc
import tkinter as tk
from tkinter import messagebox, filedialog


# ==========================================================
# 1. Custom Exception Hierarchy
# ==========================================================

class AssetError(Exception):
    """Base exception for Learning Asset operations."""
    pass


class InvalidAssetDataError(AssetError):
    """Raised when asset attributes are invalid."""
    pass


class AssetNotFoundError(AssetError):
    """Raised when an asset cannot be located."""
    pass


class EmptyServerError(AssetError):
    """Raised when operations are executed on a server with no assets."""
    pass


# ==========================================================
# 2. Abstract Data Types (Node-Based Queue & Stack ADTs)
# ==========================================================

class Node:
    """Linked structure node for custom Abstract Data Types."""
    def __init__(self, data):
        self.data = data
        self.next = None


class QueueADT(abc.ABC):
    """Abstract Base Class for Queue Data Structure."""
    @abc.abstractmethod
    def enqueue(self, item): pass

    @abc.abstractmethod
    def dequeue(self): pass

    @abc.abstractmethod
    def is_empty(self): pass


class LinkedQueue(QueueADT):
    """Node-based Queue ADT Implementation."""
    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def enqueue(self, item):
        new_node = Node(item)
        if self.is_empty():
            self._head = new_node
            self._tail = new_node
        else:
            self._tail.next = new_node
            self._tail = new_node
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Dequeue operation failed: Queue is empty.")
        removed_data = self._head.data
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return removed_data

    def is_empty(self):
        return self._head is None


class StackADT(abc.ABC):
    """Abstract Base Class for Stack Data Structure."""
    @abc.abstractmethod
    def push(self, item): pass

    @abc.abstractmethod
    def pop(self): pass

    @abc.abstractmethod
    def is_empty(self): pass


class LinkedStack(StackADT):
    """Node-based Stack ADT Implementation."""
    def __init__(self):
        self._top = None
        self._size = 0

    def push(self, item):
        new_node = Node(item)
        new_node.next = self._top
        self._top = new_node
        self._size += 1

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop operation failed: Stack is empty.")
        popped_data = self._top.data
        self._top = self._top.next
        self._size -= 1
        return popped_data

    def is_empty(self):
        return self._top is None


# ==========================================================
# 3. Domain Model & Polymorphism Architecture
# ==========================================================

class LearningAsset(abc.ABC):
    """Abstract Base Class for all Learning Assets."""
    def __init__(self, title, file_size_kb):
        if not title:
            raise InvalidAssetDataError("Asset title cannot be empty.")
        if file_size_kb <= 0:
            raise InvalidAssetDataError("File size must be greater than zero.")

        self._title = title
        self._file_size_kb = float(file_size_kb)

    # Variant 1: Abstract Method forcing overridden behavior in derived classes
    @abc.abstractmethod
    def calculate_bandwidth_mb(self):
        return self._file_size_kb / 1024.0

    # Variant 3: Uniform Status Summary
    @abc.abstractmethod
    def get_status_summary(self):
        pass

    @abc.abstractmethod
    def to_file_string(self):
        pass


class VideoLesson(LearningAsset):
    def __init__(self, title, file_size_kb, duration_sec):
        super().__init__(title, file_size_kb)
        if duration_sec <= 0:
            raise InvalidAssetDataError("Duration must be greater than zero.")
        self._duration_sec = float(duration_sec)

    # Polymorphism Variant 1: Overriding calculate_bandwidth_mb
    def calculate_bandwidth_mb(self):
        base_mb = super().calculate_bandwidth_mb()
        streaming_overhead = (self._duration_sec / 60.0) * 0.1
        return base_mb + streaming_overhead

    # Polymorphism Variant 3: Interface Implementation
    def get_status_summary(self):
        return (f"Video Lesson: '{self._title}' | Duration: {self._duration_sec}s | "
                f"Size: {self._file_size_kb:.2f} KB | Bandwidth: {self.calculate_bandwidth_mb():.2f} MB")

    def to_file_string(self):
        return f"VideoLesson|{self._title}|{self._file_size_kb}|{self._duration_sec}\n"


class InteractiveQuiz(LearningAsset):
    def __init__(self, title, file_size_kb, question_count):
        super().__init__(title, file_size_kb)
        if question_count <= 0:
            raise InvalidAssetDataError("Question count must be at least 1.")
        self._question_count = int(question_count)

    # Polymorphism Variant 1: Overriding calculate_bandwidth_mb
    def calculate_bandwidth_mb(self):
        base_mb = super().calculate_bandwidth_mb()
        quiz_data_mb = (self._question_count * 5) / 1024.0
        return base_mb + quiz_data_mb

    # Polymorphism Variant 3: Interface Implementation
    def get_status_summary(self):
        return (f"Interactive Quiz: '{self._title}' | Questions: {self._question_count} | "
                f"Size: {self._file_size_kb:.2f} KB | Bandwidth: {self.calculate_bandwidth_mb():.2f} MB")

    def to_file_string(self):
        return f"InteractiveQuiz|{self._title}|{self._file_size_kb}|{self._question_count}\n"


class ServerNode:
    def __init__(self, node_id, region):
        self._node_id = node_id
        self._region = region
        self._assets = []
        self._action_stack = LinkedStack()
        self._task_queue = LinkedQueue()

    def add_asset(self, asset):
        if not isinstance(asset, LearningAsset):
            raise InvalidAssetDataError("Item must be an instance of LearningAsset.")
        self._assets.append(asset)
        self._action_stack.push(("ADD", asset))
        return f"Status: Added '{asset._title}' to Server Node {self._node_id}."

    def get_all_assets(self):
        if not self._assets:
            raise EmptyServerError("Catalog is empty. No assets available.")
        return self._assets

    def optimize_video_assets(self):
        if not self._assets:
            raise EmptyServerError("Optimization failed: Server contains no assets.")

        count = 0
        for asset in self._assets:
            if isinstance(asset, VideoLesson):
                asset._file_size_kb *= 0.85
                count += 1
        return f"Status: Applied 15% compression to {count} Video Lesson(s)."

    # Polymorphism Variant 2: Dynamic polymorphism across heterogeneous collection
    def get_avg_bandwidth(self):
        if not self._assets:
            raise EmptyServerError("Calculation failed: Asset list is empty.")

        total_bandwidth = sum(asset.calculate_bandwidth_mb() for asset in self._assets)
        return total_bandwidth / len(self._assets)

    def search_asset_by_title(self, title):
        if not self._assets:
            raise EmptyServerError("Search failed: Asset catalog is empty.")
        for asset in self._assets:
            if asset._title.lower() == title.lower():
                return asset
        raise AssetNotFoundError(f"Asset '{title}' not found on Server Node {self._node_id}.")

    def save_to_file(self, filepath):
        with open(filepath, "w") as f:
            f.write(f"SERVER_HEADER|{self._node_id}|{self._region}\n")
            for asset in self._assets:
                f.write(asset.to_file_string())
        return f"Status: Node data saved to '{filepath}'."

    def load_from_file(self, filepath):
        try:
            with open(filepath, "r") as f:
                lines = f.readlines()
        except Exception:
            raise FileNotFoundError(f"Target file '{filepath}' could not be opened.")

        if not lines:
            raise InvalidAssetDataError("Selected file is empty.")

        self._assets.clear()

        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")

            if parts[0] == "SERVER_HEADER":
                self._node_id = int(parts[1])
                self._region = parts[2]
            elif parts[0] == "VideoLesson":
                obj = VideoLesson(parts[1], float(parts[2]), float(parts[3]))
                self._assets.append(obj)
            elif parts[0] == "InteractiveQuiz":
                obj = InteractiveQuiz(parts[1], float(parts[2]), int(parts[3]))
                self._assets.append(obj)

        return f"Status: Successfully loaded {len(self._assets)} asset(s) from file."


class SchoolHub:
    def __init__(self, school_name, server=None):
        self._school_name = school_name
        self._server = server if server is not None else ServerNode(101, "OMUSATI")

    def set_school_name(self, new_name):
        self._school_name = new_name

    def generate_analytics_report(self):
        avg_bw = self._server.get_avg_bandwidth()
        report = (
            f"--- {self._school_name} Digital Resource Analytics ---\n"
            f"Region: {self._server._region} | Node ID: {self._server._node_id}\n"
            f"Total Cataloged Assets: {len(self._server._assets)}\n"
            f"Average Bandwidth Footprint: {avg_bw:.2f} MB\n"
            f"Status: Report compiled successfully."
        )
        return report


# ==========================================================
# 4. Graphical User Interface (Tkinter)
# ==========================================================

class SchoolHubGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Omusati Rural SchoolHub Management System")
        self.root.geometry("650x680")

        # Localized list of rural schools in the Omusati Region
        self.omusati_schools = [
            "Outapi Combined School",
            "Elim Combined School",
            "Anamulenge Combined School",
            "Onesi Senior Secondary School",
            "Tsandi Combined School",
            "Ruacana High School"
        ]

        # Initialize domain model with default Omusati rural school
        server = ServerNode(node_id=101, region="OMUSATI")
        self.hub = SchoolHub(
            school_name=self.omusati_schools[0], server=server
        )

        # Pre-populate initial learning assets
        try:
            self.hub._server.add_asset(
                VideoLesson("Biology Intro", 50000.0, 600)
            )
            self.hub._server.add_asset(
                InteractiveQuiz("Biology Quiz 1", 1200.0, 15)
            )
            self.hub._server.add_asset(
                VideoLesson("Math Basics", 80000.0, 1200)
            )
        except AssetError as err:
            messagebox.showerror("Initialization Error", str(err))

        self.show_main_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_window()

        title = tk.Label(
            self.root,
            text="OMUSATI RURAL SCHOOLHUB SYSTEM",
            font=("Arial", 16, "bold"),
        )
        title.pack(pady=15)

        subtitle = tk.Label(
            self.root,
            text=f"Active School: {self.hub._school_name}\nRegion: {self.hub._server._region}",
            font=("Arial", 11, "italic"),
            fg="darkblue"
        )
        subtitle.pack(pady=5)

        # Select / Switch School Option
        tk.Button(
            self.root,
            text="Select / Switch School",
            width=30,
            height=2,
            bg="#0284C7",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.show_select_school,
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="Add Learning Asset",
            width=30,
            height=2,
            command=self.show_add_asset,
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="View All Catalog Assets",
            width=30,
            height=2,
            command=self.show_all_assets,
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="Search Asset Catalog",
            width=30,
            height=2,
            command=self.show_search_asset,
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="Optimize Hub Storage",
            width=30,
            height=2,
            command=self.optimize_storage,
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="Generate Analytics Report",
            width=30,
            height=2,
            command=self.show_analytics,
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="Save Data to File",
            width=30,
            height=2,
            command=self.save_file,
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="Load Data from File",
            width=30,
            height=2,
            command=self.load_file,
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="Exit Application",
            width=30,
            height=2,
            command=self.root.destroy,
        ).pack(pady=15)

    def show_select_school(self):
        self.clear_window()

        tk.Label(
            self.root, text="SELECT OMUSATI RURAL SCHOOL", font=("Arial", 16, "bold")
        ).pack(pady=20)

        frame = tk.Frame(self.root)
        frame.pack(pady=15)

        tk.Label(frame, text="Select School:", font=("Arial", 11)).grid(
            row=0, column=0, padx=10, pady=5
        )

        self.selected_school_var = tk.StringVar(value=self.hub._school_name)
        school_dropdown = tk.OptionMenu(
            frame,
            self.selected_school_var,
            *self.omusati_schools
        )
        school_dropdown.config(width=30)
        school_dropdown.grid(row=0, column=1, padx=10, pady=5)

        tk.Button(
            self.root,
            text="Confirm School Selection",
            width=22,
            height=2,
            bg="green",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.apply_school_selection,
        ).pack(pady=20)

        tk.Button(
            self.root,
            text="Main Menu",
            width=18,
            command=self.show_main_menu,
        ).pack(pady=5)

    def apply_school_selection(self):
        chosen_school = self.selected_school_var.get()
        self.hub.set_school_name(chosen_school)
        messagebox.showinfo("School Selected", f"Active school set to:\n{chosen_school}")
        self.show_main_menu()

    def show_all_assets(self):
        self.clear_window()

        tk.Label(
            self.root, text=f"CURRENT CATALOG DATA ({self.hub._school_name})", font=("Arial", 14, "bold")
        ).pack(pady=15)

        frame = tk.Frame(self.root)
        frame.pack(pady=10, fill="both", expand=True, padx=20)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        text_area = tk.Text(
            frame,
            wrap="word",
            yscrollcommand=scrollbar.set,
            font=("Consolas", 10),
            padx=10,
            pady=10
        )
        text_area.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=text_area.yview)

        try:
            assets = self.hub._server.get_all_assets()
            text_area.insert("end", f"SCHOOL: {self.hub._school_name}\n")
            text_area.insert("end", f"TOTAL REGISTERED ASSETS: {len(assets)}\n")
            text_area.insert("end", "=" * 55 + "\n\n")

            for index, asset in enumerate(assets, start=1):
                text_area.insert("end", f"[{index}] {asset.get_status_summary()}\n\n")

        except EmptyServerError as err:
            text_area.insert("end", f"Catalog Status: {str(err)}")

        text_area.config(state="disabled")

        tk.Button(
            self.root,
            text="Main Menu",
            width=18,
            command=self.show_main_menu,
        ).pack(pady=15)

    def show_add_asset(self):
        self.clear_window()

        tk.Label(
            self.root, text="ADD LEARNING ASSET", font=("Arial", 16, "bold")
        ).pack(pady=15)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Asset Type:").grid(
            row=0, column=0, sticky="e", pady=5
        )
        self.asset_type_var = tk.StringVar(value="VideoLesson")
        type_dropdown = tk.OptionMenu(
            frame,
            self.asset_type_var,
            "VideoLesson",
            "InteractiveQuiz",
            command=self._toggle_type_fields,
        )
        type_dropdown.grid(row=0, column=1, sticky="w", pady=5)

        tk.Label(frame, text="Title:").grid(
            row=1, column=0, sticky="e", pady=5
        )
        self.entry_title = tk.Entry(frame, width=30)
        self.entry_title.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="File Size (KB):").grid(
            row=2, column=0, sticky="e", pady=5
        )
        self.entry_size = tk.Entry(frame, width=30)
        self.entry_size.grid(row=2, column=1, pady=5)

        self.lbl_extra = tk.Label(frame, text="Duration (sec):")
        self.lbl_extra.grid(row=3, column=0, sticky="e", pady=5)
        self.entry_extra = tk.Entry(frame, width=30)
        self.entry_extra.grid(row=3, column=1, pady=5)

        tk.Button(
            self.root, text="Submit Asset", width=18, command=self.submit_asset
        ).pack(pady=15)
        tk.Button(
            self.root,
            text="Main Menu",
            width=18,
            command=self.show_main_menu,
        ).pack(pady=5)

    def _toggle_type_fields(self, choice):
        if choice == "VideoLesson":
            self.lbl_extra.config(text="Duration (sec):")
        else:
            self.lbl_extra.config(text="Question Count:")

    def submit_asset(self):
        try:
            title = self.entry_title.get().strip()
            size = float(self.entry_size.get())
            extra = float(self.entry_extra.get())

            if self.asset_type_var.get() == "VideoLesson":
                asset = VideoLesson(title, size, extra)
            else:
                asset = InteractiveQuiz(title, size, int(extra))

            status_msg = self.hub._server.add_asset(asset)
            messagebox.showinfo("Success", status_msg)
            self.show_main_menu()

        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Size and Duration/Questions must be valid numbers.",
            )
        except AssetError as err:
            messagebox.showerror("Validation Error", str(err))

    def show_search_asset(self):
        self.clear_window()

        tk.Label(
            self.root,
            text="SEARCH ASSET CATALOG",
            font=("Arial", 16, "bold"),
        ).pack(pady=15)

        tk.Label(self.root, text="Enter Asset Title:").pack(pady=5)
        self.entry_search = tk.Entry(self.root, width=35)
        self.entry_search.pack(pady=5)

        tk.Button(
            self.root,
            text="Search",
            width=18,
            command=self.execute_search,
        ).pack(pady=10)

        self.lbl_search_result = tk.Label(
            self.root,
            text="",
            font=("Arial", 10),
            justify="center",
            wraplength=500,
        )
        self.lbl_search_result.pack(pady=20)

        tk.Button(
            self.root,
            text="Main Menu",
            width=18,
            command=self.show_main_menu,
        ).pack(pady=10)

    def execute_search(self):
        query = self.entry_search.get().strip()
        try:
            asset = self.hub._server.search_asset_by_title(query)
            self.lbl_search_result.config(
                text=f"Asset Found:\n{asset.get_status_summary()}", fg="green"
            )
        except AssetError as err:
            self.lbl_search_result.config(text=f"Error: {str(err)}", fg="red")

    def optimize_storage(self):
        try:
            status = self.hub._server.optimize_video_assets()
            messagebox.showinfo("Optimization Complete", status)
        except EmptyServerError as err:
            messagebox.showerror("Server Error", str(err))

    def show_analytics(self):
        try:
            report = self.hub.generate_analytics_report()
            messagebox.showinfo("Analytics Report", report)
        except EmptyServerError as err:
            messagebox.showerror("Server Error", str(err))

    def save_file(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if path:
            try:
                msg = self.hub._server.save_to_file(path)
                messagebox.showinfo("File Save", msg)
            except Exception as e:
                messagebox.showerror(
                    "Save Error", f"Failed to save data: {str(e)}"
                )

    def load_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if path:
            try:
                msg = self.hub._server.load_from_file(path)
                messagebox.showinfo("File Load", msg)
            except Exception as e:
                messagebox.showerror(
                    "Load Error", f"Failed to read file: {str(e)}"
                )


# ==========================================================
# 5. Application Execution Entry Point
# ==========================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = SchoolHubGUI(root)
    root.mainloop()
