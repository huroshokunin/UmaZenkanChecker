import tkinter as tk
import tkinter.ttk as ttk
import json


class TreeviewApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("TREEVIEW TEST")
        self.master.geometry("1050x500")

        list_grade = self.load_data()
        frames_grade, frame_treeview = self.create_frame()

        for i, _ in enumerate(list_grade):
            self.create_grade_tab(frames_grade[i], list_grade[i])

        label = tk.Label(frame_treeview, text='TEXT')
        label.grid(sticky=tk.EW)

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

    def create_frame(self):
        # Create Grade frames
        # frame_g1, frame_g2, frame_g3 is in frame_grade
        frames_grade = []
        frame_grade = tk.Frame(self.master, bg='blue')
        frame_grade.grid(row=0, columnspan=3, sticky='nwe')

        frame_g1 = tk.Frame(frame_grade)
        frame_g2 = tk.Frame(frame_grade)
        frame_g3 = tk.Frame(frame_grade)
        frame_g1.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NW)
        frame_g2.grid(row=1, column=1, padx=5, pady=5, sticky=tk.NW)
        frame_g3.grid(row=1, column=2, padx=5, pady=5, sticky=tk.NW)
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
        frame_treeview = tk.Frame(self.master, bg='gray')
        frame_treeview.grid(row=2, columnspan=3, sticky=tk.EW)

        return frames_grade, frame_treeview

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
        rows = 0
        columns = 0
        for tab_num in range(tab_count):
            # Create tabs frame
            tab = tk.Frame(notebook, bg='green')
            list_tab.append(tab)

            notebook.add(list_tab[tab_num], text=f'Page{tab_num+1}')
        for tab_num, list_checkbox in enumerate(list_checkboxes):
            for race_num, checkbox in enumerate(list_checkbox):
                if (race_num % 3 == 0):
                    rows += 1
                    columns = 0
                checkbox_race = tk.Checkbutton(
                    list_tab[tab_num], text=checkbox['Name'])
                checkbox_race.grid(row=rows, column=columns, sticky=tk.NW)

                columns += 1
        notebook.grid(sticky=tk.NW)


if __name__ == "__main__":
    root = tk.Tk()
    app = TreeviewApp(master=root)
    app.mainloop()
