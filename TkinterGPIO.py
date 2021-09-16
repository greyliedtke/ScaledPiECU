from TkinterGUI import *

# initialize window
window = create_window("KeyTrigger")
frame = create_frame(window)

lab1 = CreatePackWidget(w_type='Label', w_cont="Fuck")
lab2 = CreatePackWidget(w_type='Label', w_cont="Grey your a freak")

count = 0
count_label = Label(frame, text=count)
count_label.pack()


def counter():
    global count
    count += 1
    count_label.config(text=count)
    count_label.after(1000, counter())


count_label.after(1000, counter())

# window.mainloop()


if __name__ == "__main__":
    window.mainloop()

# end of script
