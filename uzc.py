import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import json
import os
import sys


class TreeviewApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        if getattr(sys, 'frozen', False):
            self.initialdir = os.path.dirname(sys.executable)
        else:
            self.initialdir = './'

        self.master.title("Umamusume Zenkan Checker")
        self.master.geometry("1070x420")
        self.master.resizable(width=False, height=False)

        self.race_data = self.load_race_data_from_json()
        self.checked_items = []
        self.checkboxes = {}

        self.frames_grade, self.frame_treeview = self.create_frames()
        self.create_menubar()
        self.create_grade_tabs()
        self.create_treeview(self.frame_treeview)
        self.create_scrollbar(self.frame_treeview)

    def load_race_data_from_json(self):
        """レースデータをjsonファイルから読み込む"""

        if getattr(sys, 'frozen', False):  # PyInstallerでパッケージ化されている場合
            script_dir = sys._MEIPASS  # PyInstallerが一時的に作成する作業ディレクトリ
        else:  # 通常のPythonスクリプトとして実行されている場合
            script_dir = os.path.dirname(os.path.realpath(__file__))
        data_file_path = os.path.join(script_dir, 'data', 'TrophyRoom.json')

        with open(data_file_path, encoding='utf-8') as f:
            data = json.load(f)
        return [data[grade] for grade in ['G1', 'G2', 'G3']]

    def create_frames(self):
        frame_grade = self.create_grade_frames()
        frame_treeview = self.create_treeview_frame()
        return frame_grade, frame_treeview

    def create_grade_frames(self):
        frame_grade = tk.Frame(self.master)
        frame_grade.grid(row=0, columnspan=3, sticky=tk.NSEW)
        frames = [self.create_grade_frame(frame_grade, i) for i in range(3)]
        return frames

    def create_grade_frame(self, parent_frame, i):
        frame = tk.Frame(parent_frame)
        frame.grid(row=1, column=i, padx=5, sticky=tk.NW)
        tk.Label(
            frame,
            text=f'G{i+1}',
            font=(
                "",
                12,
                "bold"),
            bd=5
        ).grid(sticky=tk.NW)
        return frame

    def create_treeview_frame(self):
        frame_treeview = tk.Frame(self.master)
        frame_treeview.grid(row=2, column=0, columnspan=3, sticky=tk.NS)
        return frame_treeview

    def create_menubar(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)
        setting = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='ファイル', menu=setting)

        setting.add_command(label='保存', command=self.save_file)
        setting.add_command(label='読み込み', command=self.read_file)
        setting.add_separator()
        setting.add_command(label='終了', command=self.quit)

    def save_file(self):
        filename = filedialog.asksaveasfilename(
            title="名前を付けて保存",
            filetypes=[("Json files", "*.json")],
            initialdir=self.initialdir,
            defaultextension=".json"
        )
        if filename:
            with open(filename, 'w', encoding='utf-8') as outfile:
                json.dump(
                    self.checked_items,
                    outfile,
                    indent=2,
                    ensure_ascii=False
                )

            # ここで保存したファイル名をタイトルに追加する
            name = os.path.basename(filename)
            self.master.title(f"Umamusume Zenkan Checker - {name}")

    def read_file(self):
        filename = filedialog.askopenfilename(
            title="ファイルを開く",
            filetypes=[("Json files", "*.json")],
            initialdir=self.initialdir
        )
        if filename:
            with open(filename, 'r', encoding='utf-8') as infile:
                items = json.load(infile)
                for checkbox in self.checkboxes.values():
                    checkbox.deselect()
                for item in items:
                    if item['Name'] in self.checkboxes:
                        self.checkboxes[item['Name']].select()
                        self.handle_checkbox_click(item)

            # ここでfilenameを利用してタイトルを変更する
            name = os.path.basename(filename)
            self.master.title(f"Umamusume Zenkan Checker - {name}")

    def create_grade_tabs(self):
        for frame, races in zip(self.frames_grade, self.race_data):
            self.create_tabs_with_checkboxes(frame, races)

    def create_tabs_with_checkboxes(self, frame, races):
        races_per_tab = 15
        race_sublists = [races[i:i + races_per_tab]
                         for i in range(0, len(races), races_per_tab)]
        notebook = ttk.Notebook(frame)
        for i, sublist in enumerate(race_sublists):
            self.create_tab_with_checkboxes(notebook, sublist, i + 1)
        notebook.grid()

    def create_tab_with_checkboxes(self, notebook, races, tab_num):
        tab = tk.Frame(notebook)
        notebook.add(tab, text=f'Page{tab_num}')
        for i, race in enumerate(races):
            row, column = divmod(i, 3)
            self.create_checkbox(tab, race, row, column)

    def create_checkbox(self, parent, race, row, column):
        checkbox = tk.Checkbutton(
            parent,
            text=race['Name'],
            command=lambda race=race: self.handle_checkbox_click(race)
        )
        checkbox.grid(row=row, column=column, sticky=tk.NW)
        self.checkboxes[race['Name']] = checkbox

    def sort_by_distance(self, descending=False):
        self.checked_items.sort(
            key=lambda item: item['Distance'],
            reverse=descending)
        self.update_treeview()

    def create_treeview(self, frame):
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
            'Handed'
        )
        for column, width in zip(
                self.tree['columns'], [100, 70, 50, 40, 20, 40, 70, 90, 70]):
            self.tree.column(column, width=width, minwidth=50)
        for column, text in zip(
                self.tree['columns'], [
                    'フェーズ',
                    '開催時期',
                    'レース名',
                    'グレード',
                    '開催地',
                    'コース',
                    '距離',
                    '距離区分',
                    '回り'
                ]):
            self.tree.heading(column, text=text)

        self.tree.heading(
            'Distance',
            text='距離',
            command=self.sort_by_distance
        )
        self.tree.grid(sticky=tk.NS)

    def create_scrollbar(self, frame):
        scrollbar = ttk.Scrollbar(
            frame, orient='vertical', command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.tree.configure(yscrollcommand=scrollbar.set)

    def handle_checkbox_click(self, race):
        if race in self.checked_items:
            self.checked_items.remove(race)
        else:
            self.checked_items.append(race)
        self.update_treeview()

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
                )
            )


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = TreeviewApp(master=root)
    app.mainloop()
