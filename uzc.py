import tkinter as tk
import tkinter.ttk as ttk
import json


class TreeviewApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("TREEVIEW TEST")
        self.master.geometry("1000x500")

        data = self.load_data_from_file()
        items = self.get_grade_items(data)

        grade_frames = self.create_grade_frames()
        tab_frames = []

        for num, frame in enumerate(grade_frames):
            tab_frame = self.create_tab_frame(frame, items[num])
            tab_frames.append(tab_frame)

        tv_frame = self.create_treeview_frame()
        tree = self.create_treeview(tv_frame, items[0][0])

    def load_data_from_file(self):
        with open('./uma/venvUmaZenkanChecker/TrophyRoom.json', 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_grade_items(self, data):
        return [data['G1'], data['G2'], data['G3']]

    def create_grade_frames(self):
        grade_frame = tk.Frame(self.master)
        grade_frame.grid(row=1, column=1, sticky=tk.NW)

        G1_label = tk.Label(grade_frame, text='G1', font="bold")
        G2_label = tk.Label(grade_frame, text='G2', font="bold")
        G3_label = tk.Label(grade_frame, text='G3', font="bold")

        G1_frame = tk.Frame(grade_frame)
        G2_frame = tk.Frame(grade_frame)
        G3_frame = tk.Frame(grade_frame)

        G1_label.grid(row=0, column=0, sticky=tk.W)
        G2_label.grid(row=0, column=1, sticky=tk.W)
        G3_label.grid(row=0, column=2, sticky=tk.W)

        G1_frame.grid(row=1, column=0, sticky=tk.NW)
        G2_frame.grid(row=1, column=1, sticky=tk.NW)
        G3_frame.grid(row=1, column=2, sticky=tk.NW)

        return [G1_frame, G2_frame, G3_frame]

    def create_tab_frame(self, parent_frame, race_list):
        checkbox_vars = []
        checkbox_max = 15
        cols = 3
        tab_count = (len(race_list) // checkbox_max) + \
            (1 if len(race_list) % checkbox_max != 0 else 0)
        notebook = ttk.Notebook(parent_frame)

        for i in range(tab_count):
            tab = tk.Frame(notebook)
            notebook.add(tab, text=f'page{i+1}')
            start_index = i * checkbox_max
            end_index = min((i + 1) * checkbox_max, len(race_list))
            tab_race_list = race_list[start_index:end_index]

            for index, race_value in enumerate(tab_race_list):
                checkbox_var = tk.BooleanVar()
                checkbox_vars.append(checkbox_var)
                checkbox = tk.Checkbutton(
                    tab, text=race_value['Name'], variable=checkbox_var)
                row = index // cols
                column = index % cols
                checkbox.grid(row=row + 1, column=column, sticky=tk.W)

        notebook.grid(row=2, column=0, sticky=tk.W)
        return tab_count, checkbox_vars

    def create_treeview_frame(self):
        tv_frame = tk.Frame(self.master, width=500)
        tv_frame.grid(row=2, column=1, pady=5, sticky=tk.NSEW)
        return tv_frame

    def create_treeview(self, tv_frame, item):
        tree = ttk.Treeview(tv_frame, show='headings')
        keys = list(item.keys())
        tree['columns'] = keys
        tree.grid(row=2, column=0, sticky=tk.EW)

        tree['columns'] = (
            'Phase',
            'Schedule',
            'Name',
            'Grade',
            'Place',
            'CourseType',
            'Distance',
            'DistanceType',
            'Handed')
        tree.column('Phase', width=50, minwidth=50)
        tree.column('Schedule', width=60, minwidth=60)
        tree.column('Name', width=150, minwidth=50)
        tree.column('Grade', width=40, minwidth=20)
        tree.column('Place', width=50, minwidth=20)
        tree.column('CourseType', width=40, minwidth=20)
        tree.column('Distance', width=100, minwidth=20)
        tree.column('DistanceType', width=60, minwidth=20)
        tree.column('Handed', width=30, minwidth=20)

        tree.heading('Phase', text='フェーズ')
        tree.heading('Schedule', text='開催時期')
        tree.heading('Name', text='レース名')
        tree.heading('Grade', text='グレード')
        tree.heading('Place', text='開催地')
        tree.heading('CourseType', text='コース')
        tree.heading('Distance', text='距離')
        tree.heading('DistanceType', text='距離区分')
        tree.heading('Handed', text='回り')
        return tree


if __name__ == "__main__":
    root = tk.Tk()
    app = TreeviewApp(master=root)
    app.mainloop()
