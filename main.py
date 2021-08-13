import calendar
import datetime
import tkinter as tk
import tkinter.simpledialog as dialog
from typing import Optional

import tkcalendar


class CalendarDialog(dialog.Dialog):
    """Dialog box that displays a calendar and returns the selected date"""

    def body(self, master):
        self.calendar = tkcalendar.Calendar(master)
        self.calendar.pack()

    def apply(self):
        _d = (self.calendar.get_date()).split('/')
        self.result = f"{_d[1]:0>2}-{_d[0]:0>2}-20{_d[2]}"


def getDays(d1: str, d2: str) -> Optional[dict]:
    if d1 in {'', 'None'} or d2 in {'', 'None'}:
        return None
    D1 = datetime.datetime.strptime(d1, "%d-%m-%Y")
    D2 = datetime.datetime.strptime(d2, "%d-%m-%Y")
    delta = abs((D1 - D2).days)
    d = dict((k, delta // 7) for k in range(7))
    D = D1.weekday()
    for i in range(delta % 7 + 1):
        d[D] += 1
        D = 0 if D == 6 else D + 1

    return d


def main():
    root = tk.Tk()
    root.title("Days Calculator")
    root.geometry("500x500")

    def onclick(var: tk.StringVar):
        cd = CalendarDialog(root)
        var.set(cd.result)

    dateVar1, dateVar2 = tk.StringVar(), tk.StringVar()
    tk.Label(root, text="DAYS BETWEEN CALCULATOR", font=("Arial", 20, 'underline')).pack(pady=40)
    D1 = tk.Frame(root)
    D1.pack(pady=20)
    tk.Label(D1, text="FROM : ").grid(row=0, column=0)
    tk.Entry(D1, width=50, textvariable=dateVar1, state=tk.DISABLED).grid(row=0, column=1)
    tk.Button(D1, text="...", width=3, command=lambda: onclick(dateVar1)).grid(row=0, column=2)

    D2 = tk.Frame(root)
    D2.pack(pady=20)
    tk.Label(D2, text="TILL : ").grid(row=0, column=0)
    tk.Entry(D2, width=50, textvariable=dateVar2, state=tk.DISABLED).grid(row=0, column=1)
    tk.Button(D2, text="...", width=3, command=lambda: onclick(dateVar2)).grid(row=0, column=2)

    result = tk.Frame(root)

    def res(frame: tk.Frame):
        for child in frame.winfo_children():
            child.destroy()
        frame.pack_forget()
        days = getDays(dateVar1.get(), dateVar2.get())
        result.pack(pady=20)
        if days is None:
            tk.Label(result, text="Select a date").grid(row=0)
        else:
            tk.Label(result, text="Number of Days per Weekday").grid(row=0, columnspan=2)
            for i in range(7):
                tk.Label(result, text=calendar.day_name[i], justify=tk.LEFT).grid(row=i + 1, column=0, sticky=tk.W)
                tk.Label(result, text=f"= {days[i]}", justify=tk.LEFT).grid(row=i + 1, column=1, sticky=tk.W)

    tk.Button(root, text="CALCULATE", command=lambda: res(result)).pack()

    root.update()

    root.mainloop()


main()
