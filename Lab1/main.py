from functions import *
from tkinter import *
from tkinter import messagebox
from random import sample

w = 750
h = 600

root = Tk()
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)
root.geometry("%dx%d+%d+%d" % (w, h, x, y))
root.resizable(False, False)
root.title("Вікно 1")


def create_set_field(label_text, field_number):
    Label(text=label_text, font=("Arial", 18)).place(x=120, y=225 + field_number * 40)
    ent = Entry(width=15, font=("Arial", 18), state="disabled", highlightthickness=1, highlightbackground="black", highlightcolor="black")
    ent.place(x=265, y=225 + field_number * 40, height=30)
    return ent


set_message = Label(root, text="", font="Arial 14 underline")
set_message.place(x=475, y=225)

entryA = create_set_field("Множина A: ", 0)
entryB = create_set_field("Множина B: ", 1)
entryC = create_set_field("Множина C: ", 2)
entryU = create_set_field("Множина U: ", 3)

entriesList = [entryA, entryB, entryC]

setA = set()
setB = set()
setC = set()
setU = set()
setD = set()
setX = set()
setY = set()
setZ = set()

sets_ready = False

full_steps = [
    "1) A ∪ B = ",
    "2) A ∪ ¬B = ",
    "3) (A ∪ B) ∪ (A ∪ ¬B) = ",
    "4) ((A ∪ B) ∪ (A ∪ ¬B)) ∩ ¬B = ",
    "5) ((A ∪ B) ∪ (A ∪ ¬B)) ∩ ¬B ∩ A = ",
    "6) ¬A ∪ C = ",
    "7) ((A ∪ B) ∪ (A ∪ ¬B)) ∩ ¬B ∩ A ∩ (¬A ∪ C) = ",
]

simplified_steps = [
    "1) ¬B ∩ A = ",
    "2) ¬B ∩ A ∩ C = ",
]

step = 0

choice = IntVar()


def create_new_window(text):
    new_window = Toplevel(root)
    new_window.title(text)
    new_window.geometry("%dx%d+%d+%d" % (w, h, x, y))
    return new_window


def do_step(win, steps):
    global step, btn_step, btn_save, setD, answer
    if step == len(steps): return
    if len(steps) == 7:
        answer = solve_full_equation(step, setA, setB, setC, setU)
    else:
        answer = solve_simplified_equation(step, setA, setB, setC, setU)
    if answer == set(): answer = "ø"
    setD = answer
    if step + 1 == len(steps):
        btn_step.configure(state="disabled")
        btn_save.configure(state="normal")
        Label(win, text=f"D: {setD}", font=("Arial", 22)).place(x=30, y=180 + (step + 1) * 40)
    Label(win, text=f"{steps[step]} {answer}", font=("Arial", 17)).place(x=25, y=180 + step * 35)
    step += 1


def save_result(type):
    global btn_save
    set = setD if (type == "D1" or type == "D2") else setZ
    with open("sets.txt", "a+", encoding="utf-8") as file:
        file.write(f"{type} = {str(set)}\n")
    btn_save.configure(state="disabled")


def show_sets(win):
    global btn_read, btn_compare1, btn_compare2, file, D1, D2, Z1, Z2
    with open("sets.txt", "r", encoding="utf-8") as file:
        D1 = file.readline().strip()
        D2 = file.readline().strip()
        Z1 = file.readline().strip()
    Z2 = setX.union(setY)
    Label(win, text=D1, font=("Arial", 18)).place(x=30, y=50)
    Label(win, text=D2, font=("Arial", 18)).place(x=30, y=100)
    Label(win, text=Z1, font=("Arial", 18)).place(x=30, y=150)
    Label(win, text=f"Z2 = {Z2}", font=("Arial", 18)).place(x=30, y=200)
    btn_read.configure(state="disabled")
    btn_compare1.configure(state="normal")
    btn_compare2.configure(state="normal")


def set_from_string(a):
    la = re.split(r"[-{}.,:;\s]", a.split("=")[1])
    fa = filter(lambda e: e != "", la)
    return set([int(i) for i in list(fa)])


def compare_d_sets():
    global D1, D2, btn_compare1, textD
    try:
        if D1 == "" and D2 == "":
            textD.configure(text="Множини D не задані")
            textD.configure(bg="red")
        elif "ø" in D1 and "ø" in D2:
            textD.configure(text="Множини D рівні")
            textD.configure(bg="green")
        else:
            D1 = set_from_string(D1)
            D2 = set_from_string(D2)
            sets_equal = D1 == D2
            textD.configure(text="Множини D рівні") if sets_equal else textD.configure(text="Множини D не рівні")
            textD.configure(bg="green") if sets_equal else textD.configure(bg="red")
    except:
        textD.configure(text="Множини D не рівні")
        textD.configure(bg="red")
    btn_compare1.configure(state="disabled")


def compare_z_sets():
    global Z1, Z2, btn_compare2, textZ
    try:
        if Z1 == "" and Z2 == set():
            textZ.configure(text="Множини Z не задані")
            textZ.configure(bg="red")
        else:
            Z1 = set_from_string(Z1)
            sets_equal = Z1 == Z2
            textZ.configure(text="Множини Z рівні") if sets_equal else textZ.configure(text="Множини Z не рівні")
            textZ.configure(bg="green") if sets_equal else textZ.configure(bg="red")
    except:
        textZ.configure(text="Множини Z не рівні")
        textZ.configure(bg="red")
    btn_compare2.configure(state="disabled")


def window2():
    global btn_step, btn_save, step
    win2 = create_new_window("Вікно 2")
    step = 0
    Label(win2, text="A: {0} \nB: {1}\nC: {2}".format(setA, setB, setC), justify="left", font=("Arial", 20)).place(x=50, y=30)
    btn_state = "normal" if sets_ready else "disabled"
    btn_step = Button(win2, text="Дія", font=("Arial", 16), width=8, pady=12, state=btn_state, command=lambda: do_step(win2, full_steps))
    btn_step.place(x=530, y=100)
    btn_save = Button(win2, text="Зберегти", font=("Arial", 16), pady=12, state="disabled", command=lambda: save_result("D1"))
    btn_save.place(x=530, y=30)


def window3():
    global btn_step, btn_save, step
    win3 = create_new_window("Вікно 3")
    step = 0
    Label(win3, text="A: {0} \nB: {1}\nC: {2}".format(setA, setB, setC), justify="left", font=("Arial", 20)).place(x=50, y=30)
    btn_state = "normal" if sets_ready else "disabled"
    btn_step = Button(win3, text="Дія", pady=12, state=btn_state, font=("Arial", 16), width=8, command=lambda: do_step(win3, simplified_steps))
    btn_step.place(x=530, y=100)
    btn_save = Button(win3, text="Зберегти", font=("Arial", 16), pady=12, state="disabled", command=lambda: save_result("D2"))
    btn_save.place(x=530, y=30)


def window4():
    global setX, setY, setZ, btn_save
    win4 = create_new_window("Вікно 4")
    if setA == set() or setB == set():
        Label(win4, text="Введіть множини на головній сторінці!", font=("Arial", 22), pady=10, fg="red").place(x=110, y=100)
        return
    Label(win4, text="Результат виконання логічної операції", font=("Arial", 22)).place(x=110, y=50)
    Label(win4, text=f"Множина X: {setX}", font=("Arial", 18)).place(x=30, y=110)
    Label(win4, text=f"Множина Y: {setY}", font=("Arial", 18)).place(x=30, y=150)
    Label(win4, text=f"Множина Z (X ∪ Y): {setZ}", font=("Arial", 18)).place(x=30, y=190)
    btn_save = Button(win4, text="Зберегти", pady=12, font=("Arial", 16), command=lambda: save_result("Z1"))
    btn_save.place(x=310, y=245)


def window5():
    global btn_read, btn_compare1, btn_compare2, textD, textZ, D1, D2, Z
    win5 = create_new_window("Вікно 5")
    btn_read = Button(win5, text="Зчитати множини", pady=5, command=lambda: show_sets(win5), font=("Arial", 18))
    btn_read.place(x=510, y=70)
    btn_compare1 = Button(win5, text="Порівняти D", pady=5, state="disabled", command=compare_d_sets, font=("Arial", 18))
    btn_compare1.place(x=565, y=140)
    btn_compare2 = Button(win5, text="Порівняти Z", pady=5, state="disabled", command=compare_z_sets, font=("Arial", 18))
    btn_compare2.place(x=565, y=210)
    textD = Label(win5, text="", fg="white", pady=5, font=("Arial", 21))
    textD.place(x=250, y=345)
    textZ = Label(win5, text="", fg="white", pady=5, font=("Arial", 21))
    textZ.place(x=250, y=400)


def generate_sets():
    global setX, setY, setZ, setU, sets_ready
    try:
        if choice.get() == 1:
            generate_random_sets()
        else:
            generate_user_sets()
        if generate_U():
            print_sets()
        sets_ready = True
        setX = setB
        setY = not_set(setA, setU)
        setZ = association(setX, setY)
    except:
        messagebox.showerror("Помилка", "Перевірте ввід данних")


def print_sets():
    result.configure(text=f"A: {setA}\nB: {setB}\nC: {setC}\nU: {setU}")


def generate_random_sets():
    global setA, setB, setC
    setA = set(sample(range(0, 256), int(entryA.get())))
    setB = set(sample(range(0, 256), int(entryB.get())))
    setC = set(sample(range(0, 256), int(entryC.get())))


def generate_user_sets():
    global setA, setB, setC
    setA = set([int(i) for i in re.split(r"[-.,:;\s]", entryA.get())])
    setB = set([int(i) for i in re.split(r"[-.,:;\s]", entryB.get())])
    setC = set([int(i) for i in re.split(r"[-.,:;\s]", entryC.get())])


def generate_U():
    try:
        global setU
        setU = set()
        U = re.split(r"[-.,:;\s]", entryU.get())
        for i in range(int(U[0]), int(U[1]) + 1): setU.add(i)
        setU = setU.union(setA).union(setB).union(setC)
        return True
    except:
        raise Exception("Set U error")


def select():
    for i in entriesList: i.configure(state="normal")
    entryU.configure(state="normal")
    gen_btn.configure(state="normal")
    if choice.get() == 1:
        set_message.configure(text="Укажіть потужність множин", fg="black")
    else:
        set_message.configure(text="Укажіть елементи множини", fg="black")


option = calculate_option()

Label(text="Козаренко Денис Олегович", font=("Arial", 18)).place(relx=.5, y=20, anchor=CENTER)
Label(text="ІО-13", font=("Arial", 18)).place(relx=.5, y=50, anchor=CENTER)
Label(text="Номер у списку: 9", font=("Arial", 18)).place(relx=.5, y=75, anchor=CENTER)
Label(text=f"Варіант: {option}", font=("Arial", 18)).place(relx=.5, y=105, anchor=CENTER)

Button(text="Window 2", command=window2, font=("Arial", 15)).place(x=160, y=125)
Button(text="Window 3", command=window3, font=("Arial", 15)).place(x=270, y=125)
Button(text="Window 4", command=window4, font=("Arial", 15)).place(x=380, y=125)
Button(text="Window 5", command=window5, font=("Arial", 15)).place(x=490, y=125)

Label(text="Спосіб задавання множин:", font=("Arial", 15)).place(x=115, y=175)

result = Label(text="", justify="left", font=("Arial", 16))
result.place(x=110, y=405)

gen_btn = Button(text="Згенерувати", font=("Arial", 16), command=generate_sets, state="disabled")
gen_btn.place(x=500, y=265)

Radiobutton(text="Випадково", value=1, variable=choice, command=select, font=("Arial", 14)).place(x=360, y=175)
Radiobutton(text="Власноруч", value=2, variable=choice, command=select, font=("Arial", 14)).place(x=480, y=175)

root.mainloop()
