# Testing load stuff
load_state = [0, 0, 0, 0, 0, 0, 0]
load_level = 0


# pre test window to toggle load pins
def load_press(load_pin):
    print("triggered load:", load_pin)
    load_state[load_pin] = 1 - load_state[load_pin]



# pre-test window to test gpio stuff
class PreTestWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('PreTest Window')
        self.resizable(0, 0)
        self.geometry('400x200')
        self['bg'] = 'black'

        option_list = range(5)
        ssr_buttons = [lambda i=i: load_press(option_list[i]) for i in range(len(option_list))]
        for b in range(5):
            standard_button(self, b, ssr_buttons[b])

        self.lls = standard_label(self, "Load States")

        self.l1 = standard_label(self, load_state[0])
        self.l2 = standard_label(self, load_state[1])

        self.lls.after(1000, self.update_load_state())

    def update_load_state(self):
        self.l1.config(text=load_state[0])
        self.l2.config(text=load_state[1])
        self.lls.after(1000, self.update_load_state)


# button controls
        # control buttons
        # self.control_button = button_grid(self, control_column, 0, ecu.control_button_text, command=lambda: control_button())

        # self.load_up_button = button_grid(self, load_column, 0, "Load Up",
        #                                   command=lambda: res_load.increment_load(inc=1))
        # self.load_down_button = button_grid(self, load_column, 1, "Load Down",
        #                                     command=lambda: res_load.increment_load(inc=-1))
        # self.lll = label_grid(self, load_column, 1, res_load.level)

# load displays...
        # display all loads
        # load_column_2 = 3
        # self.lls = label_grid(self, load_column_2, 0, "Load States")
        # self.load_labels = []
        # for ll in range(7):
        #     label = label_grid(self, load_column_2, 1 + ll, ll)
        #     self.load_labels.append(label)

        # speed control
        # self.pwm_label = label_grid(self, 2, 0, "Speed %: " + str(ecu.pwm))
        # self.n2_speed = label_grid(self, 2, 1, "N2 krpm: " + str(ecu.n2_speed))


        # update function
        # self.control_button.config(text=ecu.control_button_text)

        # for ll in range(len(self.load_labels)):
        #     self.load_labels[ll].config(text=res_load.load_state[ll])


# main menu
class LoadControl(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('ECU Control')
        self.resizable(0, 0)
        self.geometry('400x200')
        self['bg'] = 'black'

        # change the background color to black
        self.style = ttk.Style(self)
        self.style.configure(
            'TLabel',
            background='black',
            foreground='red')

        # Buttons

        self.pretest_button = standard_button(self, "Pre-Test", lambda: PreTestWindow())