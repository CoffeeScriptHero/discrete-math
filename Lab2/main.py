from tkinter import *
from functions import *

w = 700
h = 600

root = Tk()
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)
root.geometry("%dx%d+%d+%d" % (w, h, x, y))
root.resizable(False, False)
root.title("Вікно 1")

choice = IntVar()

female_names = ["Вероніка", "Анастасія", "Софія", "Яна", "Надія", "Олена", "Зоя", "Діана", "Лідія"]
male_names = ["Денис", "Вадим", "Роман", "Ігор", "Павло", "Данило", "Захар", "Ернест", "Артем"]

option = calculate_option()

A = set()
B = set()


def create_new_window(text, w, h):
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    new_window = Toplevel(root)
    new_window.title(text)
    new_window.geometry("%dx%d+%d+%d" % (w, h, x, y))
    return new_window


def fill_listbox(lbox, list):
    for i in list: lbox.insert(END, i)


def select():
    global add_btn, female_lbox, male_lbox
    female_lbox.selection_clear(0, 'end')
    male_lbox.selection_clear(0, 'end')
    add_btn.configure(state="normal")


def add_names():
    global A, B, female_lbox, male_lbox, setA_text, setB_text, clear_a, clear_b, save_btn
    sets = [A, B]
    current = choice.get() - 1
    for i in female_lbox.curselection(): sets[current].add(female_lbox.get(i))
    for i in male_lbox.curselection(): sets[current].add(male_lbox.get(i))
    if current == 0:
        setA_text.configure(text=f"A: {A if len(A) != 0 else '{}'}")
    else:
        setB_text.configure(text=f"B: {B if len(B) != 0 else '{}'}")
    clear_a.configure(state="normal")
    clear_b.configure(state="normal")


def clear_set(set):
    global A, B, setA_text, setB_text
    if set == "A":
        A.clear()
        setA_text.configure(text="A: {}")
    elif set == "B":
        B.clear()
        setB_text.configure(text="B: {}")


def save_names():
    global save_btn
    with open("names.txt", "a+", encoding="utf-8") as file:
        file.truncate(0)
        file.write(f"{str(A) if len(A) > 0 else '{}'}\n")
        file.write(f"{str(B) if len(B) > 0 else '{}'}\n")


def set_from_string(a):
    la = re.split(r"[-{}.,:;'\s]", a)
    fa = filter(lambda e: e != '', la)
    return set([i for i in list(fa)])


def read_names():
    global A, B, setA_text, setB_text
    with open("names.txt", "r", encoding="utf-8") as file:
        A = set_from_string(file.readline().strip())
        B = set_from_string(file.readline().strip())
    setA_text.configure(text=f"A: {A if len(A) != 0 else '{}'}")
    setB_text.configure(text=f"B: {B if len(B) != 0 else '{}'}")


def window2():
    global female_lbox, male_lbox, setA_text, setB_text, add_btn, save_btn, clear_a, clear_b
    choice.set(0)
    A.clear()
    B.clear()
    win2 = create_new_window("Вікно 2", 700, 600)
    female_lbox = Listbox(win2, font=("Arial", 14), width=16, selectmode="multiple")
    male_lbox = Listbox(win2, font=("Arial", 14), width=16, selectmode="multiple")
    fill_listbox(female_lbox, female_names)
    fill_listbox(male_lbox, male_names)
    female_lbox.place(x=75, y=150)
    male_lbox.place(x=440, y=150)
    Label(win2, text="Оберіть множину до якої додати імена", font=("Arial", 15)).place(x=170, y=20)
    Radiobutton(win2, text="Множина А", value=1, variable=choice, command=select, font=("Arial", 14)).place(x=200, y=70)
    Radiobutton(win2, text="Множина B", value=2, variable=choice, command=select, font=("Arial", 14)).place(x=360, y=70)
    Label(win2, text="Жіночі імена", font=("Arial", 14), fg="grey").place(x=95, y=120)
    Label(win2, text="Чоловічі імена", font=("Arial", 14), fg="grey").place(x=455, y=120)
    add_btn = Button(win2, text="Додати імена", command=add_names, state="disabled", font=("Arial", 14))
    add_btn.place(x=280, y=170)
    clear_a = Button(win2, text="Очистити A", command=lambda: clear_set("A"), font=("Arial", 14))
    clear_a.place(x=285, y=230)
    clear_b = Button(win2, text="Очистити B", command=lambda: clear_set("B"), font=("Arial", 14))
    clear_b.place(x=285, y=290)
    save_btn = Button(win2, text="Зберегти", command=save_names, font=("Arial", 14))
    save_btn.place(x=230, y=400)
    read_btn = Button(win2, text="Зчитати", command=read_names, font=("Arial", 14))
    read_btn.place(x=360, y=400)
    setA_text = Label(win2, text="A: {}", font=("Arial", 15))
    setB_text = Label(win2, text="B: {}", font=("Arial", 15))
    setA_text.place(x=30, y=450)
    setB_text.place(x=30, y=500)


def draw_canvas(canvas, a, b, r, dir="last", distance=175):
    x = 15
    y = 20
    for i in a:
        canvas.create_text(x + 15, y - 10, text=i)
        canvas.create_oval(x, y, x + 30, y + 30, fill="CadetBlue1")
        x += 60
    x = 15
    y = distance
    for i in b:
        canvas.create_text(x + 15, y + 40, text=i)
        canvas.create_oval(x, y, x + 30, y + 30, fill="violet")
        x += 60
    x = 30
    y = 50
    for i in range(len(r)):
        f = list(a).index(r[i][0])
        s = list(b).index(r[i][1])
        canvas.create_line(x+60*f, y, 30 + 60*s, distance, arrow=dir)


def window3():
    global s_list, r_list
    win3 = create_new_window("Вікно 3", 800, 600)
    if len(A) <= 2 or len(B) <= 2:
        Label(win3, text="Множини А та В дуже маленькі\nабо не задані", fg="red", font=("Arial", 22)).place(x=195, y=240)
        return
    s_list = create_first_relationship(A, B, female_names)
    r_list = create_second_relationship(A, B, s_list, female_names)
    a_lbox = Listbox(win3, font=("Arial", 14), width=16, selectmode="disabled")
    b_lbox = Listbox(win3, font=("Arial", 14), width=16, selectmode="disabled")
    fill_listbox(a_lbox, A)
    fill_listbox(b_lbox, B)
    a_lbox.place(x=30, y=50)
    b_lbox.place(x=30, y=330)
    Label(win3, text="Множина А", font=("Arial", 14), fg="grey").place(x=65, y=20)
    Label(win3, text="Множина B", font=("Arial", 14), fg="grey").place(x=65, y=300)
    Label(win3, text="aSb, якщо a мати b", font=("Arial", 15)).place(x=330, y=15)
    aSb = Canvas(win3, width=600, height=235)
    aSb.place(x=245, y=50)
    draw_canvas(aSb, A, B, s_list)
    Label(win3, text="aRb, якщо a теща b", font=("Arial", 15)).place(x=330, y=290)
    aRb = Canvas(win3, width=600, height=235)
    aRb.place(x=245, y=330)
    draw_canvas(aRb, A, B, r_list)


def btn1_handler():
    global canvas, s_list, r_list, operation
    canvas.delete("all")
    new_list = [*s_list, *r_list]
    operation["text"] = "R \u222A S"
    draw_canvas(canvas, A, B, new_list, distance=200)


def btn2_handler():
    global canvas, s_list, r_list, operation
    canvas.delete("all")
    new_list = [pair for pair in s_list if pair in r_list]
    operation["text"] = "R \u2229 S"
    draw_canvas(canvas, A, B, new_list, distance=200)


def btn3_handler():
    global canvas, s_list, r_list, operation
    canvas.delete("all")
    new_list = [pair for pair in r_list if pair not in s_list]
    operation["text"] = "R \ S"
    draw_canvas(canvas, A, B, new_list, distance=200)


def btn4_handler():
    global canvas, s_list, r_list, operation
    canvas.delete("all")
    U = [*s_list, *r_list]
    new_list = [pair for pair in U if pair not in r_list]
    operation["text"] = "U \ R"
    draw_canvas(canvas, A, B, new_list, distance=200)


def btn5_handler():
    global canvas, s_list, operation
    canvas.delete("all")
    operation["text"] = "S⁻¹"
    draw_canvas(canvas, A, B, s_list, "first", 200)


def window4():
    global canvas, s_list, r_list, operation
    win4 = create_new_window("Вікно 4", 700, 600)
    if len(A) <= 2 or len(B) <= 2:
        Label(win4, text="Множини А та В дуже маленькі\nабо не задані", fg="red", font=("Arial", 22)).place(x=150, y=240)
        return
    canvas = Canvas(win4, width=600, height=250)
    canvas.place(x=70, y=180)
    Button(win4, text="R \u222A S", command=btn1_handler, font=("Arial", 14)).place(x=40, y=60)
    Button(win4, text="R \u2229 S", command=btn2_handler, font=("Arial", 14)).place(x=130, y=60)
    Button(win4, text="R \ S", command=btn3_handler, font=("Arial", 14)).place(x=220, y=60)
    Button(win4, text="U \ R", command=btn4_handler, font=("Arial", 14)).place(x=305, y=60)
    Button(win4, text="S⁻¹", command=btn5_handler, font=("Arial", 14)).place(x=390, y=60)
    Label(win4, text="Операції над відношеннями", font=("Arial", 14)).place(x=40, y=25)
    operation = Label(win4, text="R \u222A S", font=("Arial", 20))
    btn1_handler()
    operation.place(x=290, y=120)


Label(text="Козаренко Денис Олегович", font=("Arial", 18)).place(relx=.5, y=195, anchor=CENTER)
Label(text="ІО-13", font=("Arial", 18)).place(relx=.5, y=225, anchor=CENTER)
Label(text="Номер у списку: 9", font=("Arial", 18)).place(relx=.5, y=250, anchor=CENTER)
Label(text=f"Варіант: {option}", font=("Arial", 18)).place(relx=.5, y=280, anchor=CENTER)

Button(text="Window 2", command=window2, font=("Arial", 15)).place(x=195, y=305)
Button(text="Window 3", command=window3, font=("Arial", 15)).place(x=310, y=305)
Button(text="Window 4", command=window4, font=("Arial", 15)).place(x=425, y=305)


root.mainloop()
