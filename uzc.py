import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import json
import os
import sys


class TreeviewApp(tk.Frame):
    def __init__(self, master=None):
        """ 初期化 """
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

        self.frames_grade, self.frame_treeview, self.frame_sort = self.create_frames()
        self.create_menubar()
        self.create_grade_tabs()
        self.create_treeview(self.frame_treeview)
        self.create_sort_button(self.frame_sort)
        self.create_scrollbar(self.frame_treeview)

    def load_race_data_from_json(self):
        """ レースデータをjsonファイルから読み込む """
        if getattr(sys, 'frozen', False):  # PyInstallerでパッケージ化されている場合
            script_dir = sys._MEIPASS  # PyInstallerが一時的に作成する作業ディレクトリ
        else:  # 通常のPythonスクリプトとして実行されている場合
            script_dir = os.path.dirname(os.path.realpath(__file__))
        data_file_path = os.path.join(script_dir, 'data', 'TrophyRoom.json')

        with open(data_file_path, encoding='utf-8') as f:
            data = json.load(f)
        return [data[grade] for grade in ['G1', 'G2', 'G3']]

    def create_frames(self):
        """ 全体のフレームを作成するための関数呼び出し """
        frame_grade = self.create_grade_frames()
        frame_treeview = self.create_treeview_frame()
        frame_sort = self.create_sort_frame()
        return frame_grade, frame_treeview, frame_sort

    def create_grade_frames(self):
        """ レースフレームを作成するための関数呼び出しとリストに格納 """
        frame_grade = tk.Frame(self.master)
        frame_grade.grid(row=0, columnspan=3, sticky=tk.NSEW)
        frames = [self.create_grade_frame(frame_grade, i) for i in range(3)]
        return frames

    def create_grade_frame(self, parent_frame, i):
        """ レースグレードのフレームを作成する """
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
        """ ツリービューのフレームを作成する """
        frame_treeview = tk.Frame(self.master)
        frame_treeview.grid(row=2, column=0, columnspan=2, sticky=tk.NS)
        return frame_treeview

    def create_sort_frame(self):
        """ ソートボタンのフレームを作成する """
        frame_sort = tk.Frame(self.master)
        frame_sort.grid(row=2, column=2, sticky=tk.NS)
        return frame_sort

    def create_menubar(self):
        """ メニューバーを作成する """

        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)
        setting = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='ファイル', menu=setting)

        setting.add_command(label='保存', command=self.save_file)
        setting.add_command(label='読み込み', command=self.read_file)
        setting.add_separator()
        setting.add_command(label='終了', command=self.quit)

    def save_file(self):
        """ ファイルを保存する """
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
        """ ファイルを読み込む """

        filename = filedialog.askopenfilename(
            title="ファイルを開く",
            filetypes=[("Json files", "*.json")],
            initialdir=self.initialdir
        )
        if filename:
            with open(filename, 'r', encoding='utf-8') as infile:
                items = json.load(infile)
                # チェックボックスのチェックを全て外す
                for checkbox in self.checkboxes.values():
                    checkbox.deselect()
                # リスト内の要素を全て削除する
                self.checked_items.clear()
                for item in items:
                    if item['Name'] in self.checkboxes:
                        self.checkboxes[item['Name']].select()
                        self.handle_checkbox_click(item)

            # ここでfilenameを利用してタイトルを変更する
            name = os.path.basename(filename)
            self.master.title(f"Umamusume Zenkan Checker - {name}")

    def create_grade_tabs(self):
        """ レースグレードごとのタブを作成する """
        for frame, races in zip(self.frames_grade, self.race_data):
            self.create_tabs_with_checkboxes(frame, races)

    def create_tabs_with_checkboxes(self, frame, races):
        """チェックボックスを含むタブを作成する"""
        races_per_tab = 15
        race_sublists = [races[i:i + races_per_tab]
                         for i in range(0, len(races), races_per_tab)]
        notebook = ttk.Notebook(frame)
        for i, sublist in enumerate(race_sublists):
            self.create_tab_with_checkboxes(notebook, sublist, i + 1)
        notebook.grid()

    def create_tab_with_checkboxes(self, notebook, races, tab_num):
        """ チェックボックスを含むタブを作成する """
        tab = tk.Frame(notebook)
        notebook.add(tab, text=f'Page{tab_num}')
        for i, race in enumerate(races):
            row, column = divmod(i, 3)
            self.create_checkbox(tab, race, row, column)

    def create_checkbox(self, parent, race, row, column):
        """ チェックボックスを作成する """
        checkbox = tk.Checkbutton(
            parent,
            text=race['Name'],
            command=lambda race=race: self.handle_checkbox_click(race)
        )
        checkbox.grid(row=row, column=column, sticky=tk.NW)
        self.checkboxes[race['Name']] = checkbox

    def sort_by_phase(self, descending=False):
        """ レースのフェーズでソートするための関数 """
        # ジュニア期, クラシック期, クラシック/シニア期, シニア期の順に並ぶようにする
        phase_order = {
            "ジュニア期": 1,
            "クラシック期": 2,
            "クラシック/シニア期": 3,
            "シニア期": 4,
        }

        self.checked_items.sort(
            key=lambda item: phase_order.get(item["Phase"], 0),
            reverse=descending,
        )

        self.update_treeview()

    def sort_by_schedule(self, descending=False):
        """ 開催時期でソートするための関数 """
        # 月の部分だけを取り出してソートする
        # 1, 10, 2 となってしまうので、1, 2, 10 となるようにゼロパディングする
        self.checked_items.sort(
            key=lambda item: item['Schedule'].split('月')[0].zfill(2),
            reverse=descending
        )
        self.update_treeview()

    def sort_by_grade(self, descending=False):
        """ レースグレードでソートするための関数 """
        self.checked_items.sort(
            key=lambda item: item['Grade'],
            reverse=descending
        )
        self.update_treeview()

    def sort_by_course_type(self, descending=False):
        """ コースタイプでソートするための関数 """
        course_order = {"芝": 1, "ダート": 2}
        self.checked_items.sort(
            key=lambda item: course_order.get(item["CourseType"], 0),
            reverse=descending)
        self.update_treeview()

    def sort_by_distance(self, descending=False):
        """ 距離でソートするための関数 """
        self.checked_items.sort(
            key=lambda item: item['Distance'],
            reverse=descending)
        self.update_treeview()

    def sort_by_distance_type(self, descending=False):
        """ 距離タイプでソートするための関数 """
        distance_order = {"短距離": 1, "マイル": 2, "中距離": 3, "長距離": 4}
        self.checked_items.sort(
            key=lambda item: distance_order.get(item["DistanceType"], 0),
            reverse=descending)
        self.update_treeview()

    def sort_by_handed(self, descending=False):
        """ 左右回りでソートするための関数 """
        handed_order = {"左回り": 1, "右回り": 2}
        self.checked_items.sort(
            key=lambda item: handed_order.get(item["Handed"], 0),
            reverse=descending)
        self.update_treeview()

    def create_treeview(self, frame):
        """ ツリービューを作成する """
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
                self.tree['columns'], [100, 70, 120, 40, 20, 40, 70, 90, 70]):
            self.tree.column(column, width=width, minwidth=50)

        self.tree.heading(
            'Phase',
            text='フェーズ',
            command=self.sort_by_phase
        )

        self.tree.heading(
            'Schedule',
            text='開催時期',
            command=self.sort_by_schedule
        )

        self.tree.heading(
            'Name',
            text='レース名',
        )

        self.tree.heading(
            'Grade',
            text='グレード',
            command=self.sort_by_grade
        )

        self.tree.heading(
            'Place',
            text='開催地'
        )

        self.tree.heading(
            'CourseType',
            text='コース区分',
            command=self.sort_by_course_type
        )

        self.tree.heading(
            'Distance',
            text='距離',
            command=self.sort_by_distance
        )

        self.tree.heading(
            'DistanceType',
            text='距離区分',
            command=self.sort_by_distance_type
        )

        self.tree.heading(
            'Handed',
            text='回り',
            command=self.sort_by_handed
        )

        self.tree.grid(sticky=tk.NS)

    def create_scrollbar(self, frame):
        """ スクロールバーを作成する """
        scrollbar = ttk.Scrollbar(
            frame, orient='vertical', command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.tree.configure(yscrollcommand=scrollbar.set)

    def create_sort_button(self, frame):
        """ ソートボタンを作成する """
        # 別ウィンドウを作成して、複製したtreeを表示する
        button_sort = ttk.Button(
            frame,
            text='別ウィンドウでソート',
            command=self.create_sort_window
        )
        button_sort.grid(row=0, column=0, sticky=tk.NS)

    def create_sort_window(self):
        """ 別ウィンドウを作成する """
        # 別ウィンドウを作成する
        sort_window = tk.Toplevel(self)
        sort_window.title('別ウィンドウでソート')
        sort_window.geometry('600x300')

        # メインウィンドウのtreeviewをそのままコピーして表示させるようにさせる
        tree_copy = ttk.Treeview(sort_window, show='headings')
        tree_copy['columns'] = self.tree['columns']
        for column in self.tree['columns']:
            tree_copy.column(
                column,
                width=self.tree.column(column)['width'],
                minwidth=50)
            tree_copy.heading(
                column, text=self.tree.heading(column)['text'])

        tree_copy.grid(sticky=tk.NS)

        for item in self.checked_items:
            tree_copy.insert(
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

        # スクロールバーの追加
        scrollbar = ttk.Scrollbar(
            sort_window, orient='vertical', command=tree_copy.yview)
        scrollbar.grid(row=0, column=1, sticky=tk.NS)
        tree_copy.configure(yscrollcommand=scrollbar.set)

    def handle_checkbox_click(self, race):
        """ チェックボックスがクリックされたときの処理 """
        if race in self.checked_items:
            self.checked_items.remove(race)
        else:
            self.checked_items.append(race)
        self.update_treeview()

    def update_treeview(self):
        """ ツリービューを更新する """
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
