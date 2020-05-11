import os
import inspect as i
import tkinter as tk
import tkinter.filedialog as tkfd
import threading as t

import csgo_demoparser.DemoParser as dp
import flash_functions as ff


thread = t.Thread()


class MyButtonStyle:
    def __init__(self, root, label, cmd, name=None):
        self.text = tk.StringVar()
        self.text.set(label)
        self.btn = tk.Button(root, textvariable=self.text, command=cmd, name=name)
        self.btn.config(font=("arial", 10, ""), fg="white", bg="#101010", activebackground="#404040", bd=3)


class MyLabelStyle:
    def __init__(self, root, label):
        self.text = tk.StringVar()
        self.text.set(label)
        self.frame = tk.Label(root, textvariable=self.text)
        self.frame.config(font=("arial", 10, ""), fg="white", bg="#101010")


class MyEntryStyle:
    def __init__(self, root, label):
        self.text = tk.StringVar()
        self.text.set(label)
        self.frame = tk.Entry(root, textvariable=self.text)
        self.frame.config(justify=tk.CENTER, font=("arial", 10, ""), borderwidth=2, bg="#f0f0f0",
                          readonlybackground="#f0f0f0", width=5)


class AlertWindow:
    def __init__(self, root, message):
        self.window = tk.Toplevel(root)
        self.window.transient(root)
        self.window.title("error")
        self.window.minsize(100, 50)
        self.window.resizable(False, False)
        self.window.attributes("-topmost")
        self.window.config(bg="#101010")
        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)
        x = MyLabelStyle(self.window, message)
        x.frame.pack()
        x = MyButtonStyle(self.window, "Close", self.window.destroy)
        x.btn.pack()
        self.window.update_idletasks()
        self.window.geometry("+%d+%d" % (calc_window_pos(root, self.window)))
        self.window.grab_set()
        self.window.focus_set()


class MainWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Bang Bang Flashes")
        # self.window.minsize(sizex, sizey)
        # self.window.resizable(False, False)
        self.window.config(bg="#101010")
        frame = tk.Frame(self.window, bg="#101010")
        x = MyLabelStyle(frame, "Check flash over")
        x.frame.pack(side=tk.LEFT, padx=5, pady=2)
        self.entry = MyEntryStyle(frame, "0")
        self.entry.frame.pack(side=tk.LEFT, padx=5, pady=2)
        x = MyLabelStyle(frame, "seconds")
        x.frame.pack(side=tk.LEFT, padx=5, pady=2)
        frame.pack()
        self.status = MyLabelStyle(self.window, "waiting")
        self.status.frame.config(font=("arial", 12, ""), fg="#33ccff")
        self.status.frame.pack(padx=5, pady=5)
        frame = tk.Frame(self.window, bg="#101010")
        x = MyButtonStyle(frame, "Analyze", cmd=lambda: get_demo_path())
        x.btn.pack(side=tk.LEFT, padx=5, pady=2)
        x = MyButtonStyle(frame, "flash.txt", cmd=open_results)
        x.btn.pack(side=tk.RIGHT, padx=5, pady=2)
        frame.pack()


def calc_window_pos(x, y):
    if x.winfo_height() - y.winfo_height() < 0:
        return x.winfo_x() + (x.winfo_width() - y.winfo_width()) / 2, x.winfo_y()
    return x.winfo_x() + (x.winfo_width() - y.winfo_width()) / 2, x.winfo_y() + (
            x.winfo_height() - y.winfo_height()) / 2


def get_demo_path():
    global thread
    if thread.is_alive():
        AlertWindow(app.window, "Already analyzing a demo")
        return
    if check_seconds(app.entry.text.get()):
        ff.sec_threshold = float(app.entry.text.get())
    else:
        AlertWindow(app.window, "Seconds are not valid")
        return
    path = tkfd.askopenfilename()
    if path == "":
        return
    ff.file = open(get_app_path(), "w", encoding="utf-8")
    app.status.text.set("analyzing...")
    app.status.frame.config(fg="red")
    thread = t.Thread(target=analyze_demo, args=(path,), daemon=True)
    thread.start()


def analyze_demo(path):
    parser = dp.DemoParser(demo_path=path, ent="NONE")
    parser.subscribe_to_event("parser_start", ff.new_demo)
    parser.subscribe_to_event("gevent_player_blind", ff.player_blind)
    parser.subscribe_to_event("parser_new_tick", ff.get_entities)
    parser.subscribe_to_event("gevent_player_death", ff.player_death)
    parser.subscribe_to_event("gevent_player_team", ff.player_team)
    parser.subscribe_to_event("gevent_player_spawn", ff.player_spawn)
    parser.subscribe_to_event("gevent_begin_new_match", ff.begin_new_match)
    parser.subscribe_to_event("gevent_round_officially_ended", ff.round_officially_ended)
    parser.subscribe_to_event("parser_update_pinfo", ff.update_pinfo)
    parser.subscribe_to_event("cmd_dem_stop", ff.match_ended)
    parser.subscribe_to_event("cmd_dem_stop", ff.print_end_stats)
    parser.parse()
    app.status.text.set("done / waiting")
    app.status.frame.config(fg="#33ccff")
    ff.file.close()


def get_app_path():
    temp = os.path.abspath(i.getsourcefile(lambda: 0))
    temp = temp[:temp.rfind("\\")]
    temp = temp + r"\flashes.txt"
    return temp


def open_results():
    path = get_app_path()
    # path = path[:path.rfind("\\")]
    os.system("start {}".format(path))


def check_seconds(text):
    try:
        float(text)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    app = MainWindow()
    app.window.mainloop()
