# Import necessary modules
import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
import json

# Define a class for the app


class TreeviewApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        # Set window title, size and make it non-resizable
        self.master.title("Umamusume Zenkan Checker")
        self.master.geometry("1070x420")
        self.master.resizable(width=False, height=False)

        # Initialize an empty list to hold checked items
        self.checked_items = []

        # Load data from JSON file
        self.list_grade = self.load_data()

        # Create frames to hold the checkboxes and treeview
        self.frames_grade, self.frame_treeview = self.create_frame()

        self.create_menubar()

        # Create tabs for each grade and add checkboxes for races
        for i, _ in enumerate(self.list_grade):
            self.create_grade_tab(self.frames_grade[i], self.list_grade[i])

        # Create treeview and scrollbar
        self.create_treeview(self.frame_treeview)
        self.create_scrollbar(self.frame_treeview)

    # Function to load data from JSON file
    def load_data(self):
        list_grade = []
        with open('TrophyRoom.json', encoding='utf-8') as f:
            data = json.load(f)
            data_g1 = data['G1']
            data_g2 = data['G2']
            data_g3 = data['G3']
            list_grade.append(data_g1)
            list_grade.append(data_g2)
            list_grade.append(data_g3)
        return list_grade

    # Function to create frames for holding checkboxes and treeview
    def create_frame(self):
        # Create Grade frames
        # frame_g1, frame_g2, frame_g3 is in frame_grade
        frames_grade = []
        frame_grade = tk.Frame(self.master)
        frame_grade.grid(row=0, columnspan=3, sticky=tk.NSEW)

        frame_g1 = tk.Frame(frame_grade)
        frame_g2 = tk.Frame(frame_grade)
        frame_g3 = tk.Frame(frame_grade)
        frame_g1.grid(row=1, column=0, padx=5, sticky=tk.NW)
        frame_g2.grid(row=1, column=1, padx=5, sticky=tk.NW)
        frame_g3.grid(row=1, column=2, padx=5, sticky=tk.NW)
        frames_grade.append(frame_g1)
        frames_grade.append(frame_g2)
        frames_grade.append(frame_g3)

        # Create Grade labels
        label_g1 = tk.Label(frame_g1, text='G1', font=("bold"), bd=5)
        label_g2 = tk.Label(frame_g2, text='G2', font=("bold"), bd=5)
        label_g3 = tk.Label(frame_g3, text='G3', font=("bold"), bd=5)
        label_g1.grid(sticky=tk.NW)
        label_g2.grid(sticky=tk.NW)
        label_g3.grid(sticky=tk.NW)

        # Create Treeview frames
        frame_treeview = tk.Frame(self.master)
        frame_treeview.grid(row=2, column=0, columnspan=3, sticky=tk.NS)

        return frames_grade, frame_treeview

    # Function to create tabs for each grade and add checkboxes for races
    def create_grade_tab(self, frame, list_races):
        # Calculate the number of tabs
        checkbox_max = 15
        tab_count = len(list_races) // checkbox_max
        if len(list_races) % checkbox_max != 0:
            tab_count += 1

        # 15races in list_checkboxes
        list_checkboxes = [list_races[i:i + checkbox_max]
                           for i in range(0, len(list_races), checkbox_max)]

        notebook = ttk.Notebook(frame)
        list_tab = []
        self.list_var = []

        list_var_num = 0
        rows = 0
        columns = 0
        for tab_num in range(tab_count):
            # Create tabs frame
            tab = tk.Frame(notebook)
            list_tab.append(tab)
            notebook.add(list_tab[tab_num], text=f'Page{tab_num+1}')

        for tab_num, list_checkbox in enumerate(list_checkboxes):
            for race_num, race in enumerate(list_checkbox):
                if (race_num % 3 == 0):
                    rows += 1
                    columns = 0

                checkbox_var = tk.BooleanVar()
                checkbox_var.set(False)
                self.list_var.append(checkbox_var)

                checkbox_race = tk.Checkbutton(
                    list_tab[tab_num],
                    text=race['Name'],
                    variable=self.list_var[list_var_num],
                    command=lambda checkbox=race,
                    var=self.list_var[list_var_num]: self.handle_checkbox(
                        checkbox,
                        var))
                checkbox_race.grid(row=rows, column=columns, sticky=tk.NW)

                columns += 1
                list_var_num += 1
        notebook.grid()

    # Function to create treeview
    def create_treeview(self, frame):
        # Create treeview
        self.tree = ttk.Treeview(frame, show='headings')
        self.tree['columns'] = (
            'Phase',
            'Schedule',
            'Name',
            'Grade',
            'Place',
            'CourseType',
            'Distance',
            'DistanceType',
            'Handed')

        # Set column widths and headings
        self.tree.column('Phase', width=100, minwidth=50)
        self.tree.column('Schedule', width=70, minwidth=60)
        self.tree.column('Name', minwidth=50)
        self.tree.column('Grade', width=40, minwidth=20)
        self.tree.column('Place', minwidth=20)
        self.tree.column('CourseType', width=40, minwidth=20)
        self.tree.column('Distance', width=70, minwidth=20)
        self.tree.column('DistanceType', width=60, minwidth=20)
        self.tree.column('Handed', width=30, minwidth=20)

        self.tree.heading('Phase', text='フェーズ')
        self.tree.heading('Schedule', text='開催時期')
        self.tree.heading('Name', text='レース名')
        self.tree.heading('Grade', text='グレード')
        self.tree.heading('Place', text='開催地')
        self.tree.heading('CourseType', text='コース')
        self.tree.heading('Distance', text='距離')
        self.tree.heading('DistanceType', text='距離区分')
        self.tree.heading('Handed', text='回り')

        self.tree.grid(sticky=tk.NS)

    # Function to create scrollbar
    def create_scrollbar(self, frame):
        # Create scrollbar
        scrollbar = ttk.Scrollbar(
            frame, orient='vertical', command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.tree.configure(yscrollcommand=scrollbar.set)

    def toggle_checkbutton(self, list_checkbutton):
        for var in list_checkbutton:
            var.set(True)
        

    # Function to handle checkbox clicks and update the treeview
    def handle_checkbox(self, checkbox, var):
        for frame in self.frames_grade:
            for child in frame.winfo_children():
                if isinstance(
                        child,
                        tk.Checkbutton) and child["Name"] == checkbox["Name"]:
                    child.select()
        if checkbox in self.checked_items:
            self.checked_items.remove(checkbox)
        else:
            self.checked_items.append(checkbox)
        self.update_treeview()
        print(var)

    # Function to update the treeview based on checked items

    def update_treeview(self):
        self.tree.delete(*self.tree.get_children())
        for item in self.checked_items:
            self.tree.insert(
                '',
                'end',
                values=(
                    item['Phase'],
                    item['Schedule'],
                    item['Name'],
                    item['Grade'],
                    item['Place'],
                    item['CourseType'],
                    item['Distance'],
                    item['DistanceType'],
                    item['Handed']
                ))

    def create_menubar(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        setting = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='ファイル', menu=setting)

        setting.add_command(label='保存', command=self.save_file)
        setting.add_command(label='読み込み', command=self.read_file)

        setting.add_separator()
        setting.add_command(label='終了', command=quit)

    # Function to save checked items into JSON file
    def save_file(self):
        save_filename = filedialog.asksaveasfilename(
            title='名前を付けて保存',
            filetypes=[("jsonファイル", ".json")],
            initialdir="./",
            defaultextension=".json"
        )
        for file in save_filename:
            print(file)

        with open(save_filename, 'w', encoding='utf-8') as f:
            json.dump(self.checked_items, f, indent=2, ensure_ascii=False)

    # Function to read checked items from JSON file and update checkboxes
    def read_file(self):
        read_filename = filedialog.askopenfilename(
            title="個別ファイルを開く",
            filetypes=[("jsonファイル", ".json")],
            initialdir="./"
        )
        with open(read_filename, 'r', encoding='utf-8') as f:
            self.checked_items = json.load(f)
            self.toggle_checkbutton(self.checked_items)
            self.update_treeview()



# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = TreeviewApp(master=root)
    app.mainloop()
