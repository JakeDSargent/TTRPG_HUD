import tkinter as tk
from tkinter import simpledialog
import os
from PIL import ImageTk, Image
from functools import partial


class Params:
    pic_dir = ".\\Media\\" if os.name == 'nt' else "./Media/"
    font_dir = pic_dir + "Font\\" if os.name == 'nt' else pic_dir + "Font/"
    save_file = "Save.txt"
    all_sides = tk.N + tk.S + tk.E + tk.W

    # Font Box
    font_chars = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e",
                  "f","g","h","i","j","k","l","m","n","o","p","q","r","s","t",
                  "u","v","w","x","y","z","_"]
    small_font = "_s"
    medium_font = "_m"
    large_font = "_l"
    center = 0
    rjust = 1
    ljust = 2

    # HUD Items
    item_fgs = 28
    item_bgs = 4
    items_per_row = 5
    item_names = ["None", "Bow", "Boomerang", "Magic Boomerang", "Hookshot", "Bombs", "Magic Powder", "Bottle",
                  "Bee", "Fairy", "Green Potion", "Red Potion", "Blue Potion", "Fire Rod", "Ice Rod", "Bombos",
                  "Ether", "Quake", "Book of Mudora", "Bug Net", "Flute", "Hammer", "Lamp", "Shovel",
                  "Cane of Somaria", "Cane of Byrna", "Magic Cape", "Magic Mirror"]

    # Character HUDs
    chars_per_col = 3

    # Clocks
    clocks_per_row = 2
    clock_types = ["4 Clock", "6 Clock", "8 Clock"]
    clock_maxes = [4, 6, 8]
    clock_x_padding = 11


class MagicMeter:

    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master=self.master, bg="black", borderwidth=0, padx=3)
        self.images = [ImageTk.PhotoImage(Image.open(Params.pic_dir + "MM_" + str(x) + ".png")) for x in range(0, 6)]
        self.level = 5
        self.label = tk.Label(master=self.frame, image=self.images[self.level], borderwidth=0)
        self.label.pack()
        self.frame.pack()
        self.bind()

    def fill(self):
        if self.level < 5:
            self.level += 1
            self.update()

    def empty(self):
        if self.level > 0:
            self.level -= 1
            self.update()

    def update(self):
        self.label.configure(image=self.images[self.level])

    def on_click(self, event):
        if event.y > self.label.winfo_height() / 2:
            self.empty()
        else:
            self.fill()

    def bind(self):
        self.label.bind("<1>", self.on_click)


class HDMeter:

    def __init__(self, master, num_dice):
        self.master = master
        self.frame = tk.Frame(master=self.master, bg="black", borderwidth=0)
        self.images = [ImageTk.PhotoImage(Image.open(Params.pic_dir + "HD_" + str(num_dice) + str(x) + ".png")) for
                       x in range(0, num_dice + 1)]
        self.total_dice = num_dice
        self.remaining_dice = num_dice
        self.label = tk.Label(master=self.frame, image=self.images[self.remaining_dice], borderwidth=0)
        self.label.pack()
        self.frame.pack(side=tk.LEFT)
        self.bind()

    def fill(self):
        if self.remaining_dice < self.total_dice:
            self.remaining_dice += 1
            self.update()

    def empty(self):
        if self.remaining_dice > 0:
            self.remaining_dice -= 1
            self.update()

    def update(self):
        self.label.configure(image=self.images[self.remaining_dice])

    def on_click(self, event):
        if event.x < self.label.winfo_width() / 2:
            self.empty()
        else:
            self.fill()

    def bind(self):
        self.label.bind("<1>", self.on_click)


class HeartPieces:
    def __init__(self, master):
        self.master = master
        self.images = [ImageTk.PhotoImage(Image.open(Params.pic_dir + "hp_" + str(x) + ".png")) for x in range(0, 5)]
        self.pieces = 0
        self.frame = tk.Frame(master=self.master, bg="black", borderwidth=0)
        self.label = tk.Label(master=self.frame, image=self.images[self.pieces], bg="black", borderwidth=0)
        self.frame.pack()
        self.label.pack()
        self.bind()

    def fill(self):
        if self.pieces < 4:
            self.pieces += 1
            self.update()

    def empty(self):
        if self.pieces > 0:
            self.pieces -= 1
            self.update()

    def update(self):
        self.label.configure(image=self.images[self.pieces])

    def on_click(self, event):
        if event.x < self.label.winfo_width() / 2:
            self.empty()
        else:
            self.fill()

    def bind(self):
        self.label.bind("<1>", self.on_click)

class ProfilePicture:
    def __init__(self, master, file, bg="black"):
        self.master = master
        self.frame = tk.Frame(master=self.master, bg="black", borderwidth=0)
        self.text_frame = tk.Frame(master=self.master, bg="black", borderwidth=0, pady=3)
        self.image = ImageTk.PhotoImage(Image.open(Params.pic_dir + file))
        self.label = tk.Label(master=self.frame, image=self.image, bg=bg)
        self.font_box = FontBox(self.text_frame, 25, file[:-4])
        self.text_frame.pack()
        self.label.pack()
        self.frame.pack()


class CharacterHUD:

    def __init__(self, master, prof_file, hd_num, bg="black"):
        self.master = master
        self.prof_file = prof_file
        self.mm_frame = tk.Frame(master=self.master, bg="black", borderwidth=0, relief=tk.FLAT)
        self.pp_frame = tk.Frame(master=self.master, bg="black", borderwidth=0)
        self.hd_frame = tk.Frame(master=self.master, bg="black", borderwidth=0)
        self.mm = MagicMeter(self.mm_frame)
        self.prof_pic = ProfilePicture(self.pp_frame, prof_file, bg)
        self.pp_bg = bg
        self.hd = HDMeter(self.hd_frame, hd_num)
        self.master.grid_configure()
        self.pp_frame.grid(row=0, column=0)
        self.mm_frame.grid(row=0, column=1, sticky=Params.all_sides)
        self.hd_frame.grid(row=1, column=0, columnspan=2)


class HUDclock:

    def __init__(self, master, title="IMPLEMENT A FONT"):
        self.master = master
        self.title = title
        self.frame = tk.Frame(master=self.master)
        self.font_frame = tk.Frame(master=self.master)
        self.font_box = FontBox(self.font_frame, 16, self.title)
        self.clock_4_imgs = [ImageTk.PhotoImage(Image.open(Params.pic_dir + "clock_4" + str(x) + ".png"))
                             for x in range(0, 5)]
        self.clock_6_imgs = [ImageTk.PhotoImage(Image.open(Params.pic_dir + "clock_6" + str(x) + ".png"))
                             for x in range(0, 7)]
        self.clock_8_imgs = [ImageTk.PhotoImage(Image.open(Params.pic_dir + "clock_8" + str(x) + ".png"))
                             for x in range(0, 9)]
        self.all_images = [self.clock_4_imgs, self.clock_6_imgs, self.clock_8_imgs]
        self.clock = 0
        self.filled = 0
        self.label = tk.Label(master=self.master, image=self.all_images[self.filled][self.clock], borderwidth=0)
        self.font_frame.pack()
        self.label.pack()
        self.bind()

        self.selected_clock = tk.IntVar()
        self.popup_menu = tk.Menu(master=self.master, tearoff=0)

        for i in range(len(Params.clock_types)):
            self.popup_menu.add_radiobutton(label=Params.clock_types[i], value=i,
                                            variable=self.selected_clock, command=self.menu_update)

    def pop_up_menu(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def on_click(self, event):
        self.title = self.font_box.text
        if event.x < self.label.winfo_width() / 2:
            self.empty()
        else:
            self.fill()

    def empty(self):
        self.filled = self.filled - 1 if self.filled > 0 else self.filled
        self.update()

    def fill(self):
        self.filled = self.filled + 1 if self.filled < Params.clock_maxes[self.clock] else self.filled
        self.update()

    def menu_update(self):
        self.clock = self.selected_clock.get()
        self.filled = 0
        self.update()

    def update(self):
        self.label.configure(image=self.all_images[self.clock][self.filled])

    def bind(self):
        self.label.bind("<3>", self.pop_up_menu)
        self.label.bind("<1>", self.on_click)


class HUDItem:

    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master=self.master)
        self.bg_imgs = [ImageTk.PhotoImage(Image.open(Params.pic_dir + "inv_bg_" + str(x) + ".png"))
                        for x in range(0, Params.item_bgs)]
        self.fg_imgs = [ImageTk.PhotoImage(Image.open(Params.pic_dir + "inv_" + str(x) + ".png"))
                        for x in range(0, Params.item_fgs)]
        self.fg = 0
        self.bg = 0
        self.num_fgs = Params.item_fgs
        self.num_bgs = Params.item_bgs
        self.bg_label = tk.Label(master=self.master, image=self.bg_imgs[self.bg], borderwidth=0)
        self.fg_label = tk.Label(master=self.bg_label, image=self.fg_imgs[self.fg], borderwidth=0)
        self.bg_label.pack()
        self.fg_label.place(x=6, y=6)
        self.bind()

        self.selected_item = tk.IntVar()
        self.popup_menu = tk.Menu(master=self.master, tearoff=0)

        for i in range(len(Params.item_names)):
            self.popup_menu.add_radiobutton(label=Params.item_names[i], value=i,
                                            variable=self.selected_item, command=self.menu_update)

    def pop_up_menu(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def cycle_fg(self, event=None):
        self.fg = (self.fg + 1) % self.num_fgs
        self.fg_label.configure(image=self.fg_imgs[self.fg])

    def cycle_bg(self, event=None):
        self.bg = (self.bg + 1) % self.num_bgs
        self.bg_label.configure(image=self.bg_imgs[self.bg])
        self.fg_label.configure(image=self.fg_imgs[self.fg])

    def menu_update(self):
        self.fg = self.selected_item.get()
        self.update()

    def update(self):
        self.bg_label.configure(image=self.bg_imgs[self.bg])
        self.fg_label.configure(image=self.fg_imgs[self.fg])

    def bind(self):
        self.fg_label.bind("<3>", self.pop_up_menu)
        self.fg_label.bind("<1>", self.cycle_bg)


class Saver:
    TOF = 0
    Characters = 1
    Items = 2
    Clocks = 3
    Counters = 4
    HeartPieces = 5
    End = 5

    def __init__(self, partyHUD):
        self.partyHUD = partyHUD
        self.save_file = Params.save_file
        self.state = Saver.TOF

    def load(self):
        with open(Params.save_file, "r") as savefile:
            lines = savefile.read().split("\n")

        counts = {}

        for line in lines:
            if line == "# Characters":
                self.state = Saver.Characters
            elif line == "# Items":
                self.state = Saver.Items
            elif line == "# Clocks":
                self.state = Saver.Clocks
            elif line == "# Counters":
                self.state = Saver.Counters
            elif line == "# Heart Pieces":
                self.state = Saver.HeartPieces
            elif line == "# End":
                self.state = Saver.End

            if line is not "" and line[0] is not "#":
                if self.state == Saver.Characters:
                    options = line.split(",")
                    self.partyHUD.add_character(options[0], int(options[1]), options[4])
                    self.partyHUD.character_huds[-1].hd.remaining_dice = int(options[2])
                    self.partyHUD.character_huds[-1].mm.level = int(options[3])
                    self.partyHUD.character_huds[-1].hd.update()
                    self.partyHUD.character_huds[-1].mm.update()

                if self.state == Saver.Items:
                    if "ITEM_NUM=" in line:
                        options = line.split("=")
                        for i in range(int(options[1])):
                            self.partyHUD.add_item()
                    else:
                        options = line.split(",")
                        self.partyHUD.items[int(options[0])].fg = int(options[1])
                        self.partyHUD.items[int(options[0])].bg = int(options[2])
                        self.partyHUD.items[int(options[0])].update()

                if self.state == Saver.Clocks:
                    options = line.split(",")
                    self.partyHUD.add_clock(options[0])
                    self.partyHUD.clocks[-1].clock = int(options[1])
                    self.partyHUD.clocks[-1].filled = int(options[2])
                    self.partyHUD.clocks[-1].update()

                if self.state == Saver.Counters:
                    options = line.split(",")
                    counts[options[0]] = int(options[1])

                if self.state == Saver.HeartPieces:
                    self.partyHUD.heart_pieces.pieces = int(line)
                    self.partyHUD.heart_pieces.update()

        self.partyHUD.counter.saver_in(counts)

    def save(self):
        text = """

# Characters
# Profile pic,hd_num,current_hd,current_magic

"""
        for character in self.partyHUD.character_huds:
            text += character.prof_file
            text += "," + str(character.hd.total_dice)
            text += "," + str(character.hd.remaining_dice)
            text += "," + str(character.mm.level) + "," + character.pp_bg + "\n"

        text += """
# Items
# ITEM_NUM=<num item slots to display>
# slot_num,item_num,bg_num

ITEM_NUM="""
        text += str(len(self.partyHUD.items)) + "\n\n"
        for i in range(len(self.partyHUD.items)):
            text += str(i) + "," + str(self.partyHUD.items[i].fg)
            text += "," + str(self.partyHUD.items[i].bg) + "\n"

        text += """
# Clocks
# Clock Title,Clock Type [0=4 sides; 1=6; 2=8], Segments Filled

"""
        for clock in self.partyHUD.clocks:
            text += clock.title + "," + str(clock.clock) + "," + str(clock.filled) + "\n"
        text += """
# Counters

"""
        text += self.partyHUD.counter.saver_out()
        text += """
# Heart Pieces

"""
        text += str(self.partyHUD.heart_pieces.pieces) + "\n"
        text += """

#END
"""
        with open(Params.save_file, "w") as outfile:
            outfile.write(text)


class FontBox:

    def __init__(self, master, size, text="", point=Params.small_font, justify=Params.center):
        self.master = master
        self.size = size
        self.text = text
        self.justify = justify
        self.transform_text()

        if point == Params.small_font:
            self.images = {x: ImageTk.PhotoImage(Image.open(Params.font_dir + x + Params.small_font + ".png"))
                           for x in Params.font_chars}
        elif point == Params.medium_font:
            self.images = {x: ImageTk.PhotoImage(Image.open(Params.font_dir + x + Params.medium_font + ".png"))
                           for x in Params.font_chars}
        elif point == Params.large_font:
            self.images = {x: ImageTk.PhotoImage(Image.open(Params.font_dir + x + Params.large_font + ".png"))
                           for x in Params.font_chars}
        else:
            self.images = {x: ImageTk.PhotoImage(Image.open(Params.font_dir + x + ".png"))
                           for x in Params.font_chars}
        self.labels = [tk.Label(master=self.master, image=self.images["_"], borderwidth=0) for x in range(self.size)]
        for label in self.labels:
            label.pack(side=tk.LEFT)
        self.display()
        self.bind()

    def transform_text(self):
        self.text = self.text.replace(" ", "_")
        if self.justify == Params.rjust:
            self.text = self.text.rjust(self.size, "_")
        elif self.justify == Params.ljust:
            self.text = self.text.ljust(self.size, "_")
        else:
            self.text = self.text.center(self.size, "_")
        self.text = self.text[:self.size]
        self.text = self.text.lower()

    def update_text(self, event=None):

        text = simpledialog.askstring("Font Box", "Please limit to "+ str(self.size) + "characters")
        if text:
            self.text = text
        self.display()

    def display(self):
        self.transform_text()

        for i in range(len(self.text)):
            self.labels[i].configure(image=self.images[self.text[i]])

    def bind(self):
        for label in self.labels:
            label.bind("<3>", self.update_text)


class HUDCounter:
    def __init__(self, master):
        self.master = master
        self.master_frame = tk.Frame(self.master, bg="black")
        self.master_frame.pack()
        self.counts = {"rupees": 0,
                       "bombs": 0,
                       "keys": 0,
                       "picks": 0}
        self.pm_imgs = {"plus": ImageTk.PhotoImage(Image.open(Params.pic_dir + "plus.png")),
                        "plus_selected": ImageTk.PhotoImage(Image.open(Params.pic_dir + "plus_selected.png")),
                        "minus": ImageTk.PhotoImage(Image.open(Params.pic_dir + "minus.png")),
                        "minus_selected": ImageTk.PhotoImage(Image.open(Params.pic_dir + "minus_selected.png"))}
        self.rupee_imgs = {"red": ImageTk.PhotoImage(Image.open(Params.pic_dir + "red rupee.png")),
                           "blue": ImageTk.PhotoImage(Image.open(Params.pic_dir + "blue rupee.png")),
                           "green": ImageTk.PhotoImage(Image.open(Params.pic_dir + "green rupee.png"))}
        self.counter_imgs = {"bomb": ImageTk.PhotoImage(Image.open(Params.pic_dir + "bomb.png")),
                             "key": ImageTk.PhotoImage(Image.open(Params.pic_dir + "key.png")),
                             "picks": ImageTk.PhotoImage(Image.open(Params.pic_dir + "picks.png"))}
        self.add = True

        class Counter:
            def __init__(self, counter, image, amount):
                self.counter=counter
                self.image=image
                self.amount = amount

        self.counters = [Counter("rupees", self.rupee_imgs["green"], 1),
                         Counter("bombs", self.counter_imgs["bomb"], 1),
                         Counter("keys", self.counter_imgs["key"], 1),
                         Counter("picks", self.counter_imgs["picks"], 1)]
        self.counter_frames = {}
        self.icon_frames = {}
        self.font_frames = {}
        self.labels = {}
        self.font_boxes = {}

        for counter in self.counters:
            counter_frame = tk.Frame(master=self.master_frame, bg="black")

            counter_font_frame = tk.Frame(master=counter_frame, bg="black")
            counter_icon_frame = tk.Frame(master=counter_frame, bg="black")

            counter_icon = tk.Label(master=counter_icon_frame, image=counter.image,
                                    borderwidth=0)
            counter_font = FontBox(master=counter_font_frame, size=4, text="0000",
                                   point=Params.medium_font, justify=Params.ljust)

            counter_icon.pack(side=tk.LEFT)

            counter_icon_frame.pack(side=tk.LEFT)
            counter_font_frame.pack(side=tk.LEFT, padx=24)

            counter_frame.pack(fill=tk.X, pady=10)
            counter_icon.bind("<1>", partial(self.update_count, which_count=counter.counter, amt=counter.amount,
                                             font_box=counter_font))

            self.counter_frames[counter.counter] = counter_frame
            self.icon_frames[counter.counter] = counter_icon_frame
            self.font_frames[counter.counter] = counter_font_frame
            self.labels[counter.counter] = counter_icon
            self.font_boxes[counter.counter] = counter_font

        self.toggle_frame = tk.Frame(master=self.master_frame, bg="black")
        self.plus = tk.Label(master=self.toggle_frame, image=self.pm_imgs["plus_selected"], borderwidth=0)
        self.minus = tk.Label(master=self.toggle_frame, image=self.pm_imgs["minus"], borderwidth=0)
        self.plus.bind("<1>", lambda event: self.toggle_selected_function(True))
        self.minus.bind("<1>", lambda event: self.toggle_selected_function(False))

        self.plus.grid(row=0, column=1, sticky=tk.E)
        self.minus.grid(row=0, column=0, sticky=tk.W)
        self.toggle_frame.pack()

        self.labels["rupees"].bind("<3>", self.cycle_rupees)

    def update_count(self, event, which_count, amt, font_box):
        if not self.add:
            amt *= -1
        self.counts[which_count] += amt
        font_box.text = str(self.counts[which_count])
        font_box.display()

    def cycle_rupees(self, event=None):

        if str(self.labels["rupees"]["image"]) == str(self.rupee_imgs["green"]):
            self.labels["rupees"].configure(image=self.rupee_imgs["blue"])
            self.labels["rupees"].bind("<1>", partial(self.update_count, which_count="rupees", amt=5,
                                                      font_box=self.font_boxes["rupees"]))
        elif str(self.labels["rupees"]["image"]) == str(self.rupee_imgs["blue"]):
            self.labels["rupees"].configure(image=self.rupee_imgs["red"])
            self.labels["rupees"].bind("<1>", partial(self.update_count, which_count="rupees", amt=20,
                                                      font_box=self.font_boxes["rupees"]))
        elif str(self.labels["rupees"]["image"]) == str(self.rupee_imgs["red"]):
            self.labels["rupees"].configure(image=self.rupee_imgs["green"])
            self.labels["rupees"].bind("<1>", partial(self.update_count, which_count="rupees", amt=1,
                                                      font_box=self.font_boxes["rupees"]))

    def toggle_selected_function(self, add_bool=True):
        self.add = add_bool
        if self.add:
            self.plus.configure(image=self.pm_imgs["plus_selected"])
            self.minus.configure(image=self.pm_imgs["minus"])
        else:
            self.plus.configure(image=self.pm_imgs["plus"])
            self.minus.configure(image=self.pm_imgs["minus_selected"])

    def saver_out(self):
        text = ""
        for key in self.counts:
            text += key + "," + str(self.counts[key]) + "\n"
        text += "\n"
        return text

    def saver_in(self, counts):
        self.counts = counts
        for counter in self.counters:
            self.font_boxes[counter.counter].text = str(self.counts[counter.counter])
            self.font_boxes[counter.counter].display()


class PartyHUD:

    def __init__(self):
        self.master = tk.Tk()
        self.master_frame = tk.Frame(master=self.master, bg="black")
        self.master_frame.pack()
        self.master.title(60*" " + "ZelD&D Tracker")
        self.characters_frame = tk.Frame(master=self.master_frame, bg="black")
        self.characters_frame.grid(row=0, rowspan=2, column=0, sticky=Params.all_sides)
        self.items_frame = tk.Frame(master=self.master_frame, bg="black")
        self.items_frame.grid(row=0, column=1, sticky=Params.all_sides)
        self.clocks_frame = tk.Frame(master=self.master_frame, bg="black")
        self.clocks_frame.grid(row=1, column=1, sticky=Params.all_sides)
        self.counter_frame = tk.Frame(master=self.master_frame, bg="black")
        self.counter_frame.grid(row=0, column=2, sticky=Params.all_sides)
        self.hp_frame = tk.Frame(master=self.master_frame, bg="black")
        self.hp_frame.grid(row=1, column=2, sticky=Params.all_sides)
        self.heart_pieces = HeartPieces(self.hp_frame)
        self.counter = HUDCounter(self.counter_frame)
        self.frames = []
        self.character_huds = []
        self.items = []
        self.clocks = []
        self.saver = Saver(self)
        self.master.protocol("WM_DELETE_WINDOW", self.save_on_exit)

    def add_clock(self, title=""):
        frame = tk.Frame(master=self.clocks_frame)
        clock = HUDclock(master=frame, title=title)
        frame.grid(row=len(self.clocks) // Params.clocks_per_row, column=(len(self.clocks)) % Params.clocks_per_row,
                   padx=Params.clock_x_padding)
        self.frames.append(frame)
        self.clocks.append(clock)

    def add_character(self, prof_pic, hd, bg="black"):
        frame = tk.Frame(master=self.characters_frame, padx=15, pady=10, bg="black", borderwidth=0)
        c_hud = CharacterHUD(frame, prof_pic, hd, bg)
        frame.grid(row=len(self.character_huds) % Params.chars_per_col,
                   column=(len(self.character_huds)) // Params.chars_per_col)
        self.frames.append(frame)
        self.character_huds.append(c_hud)

    def add_item(self):
        frame = tk.Frame(master=self.items_frame)
        item = HUDItem(master=frame)
        frame.grid(row=len(self.items) // Params.items_per_row, column=(len(self.items)) % Params.items_per_row)
        self.frames.append(frame)
        self.items.append(item)

    def run(self):
        self.load()
        self.master.mainloop()

    def load(self):
        self.saver.load()

    def save_on_exit(self):
        self.saver.save()
        self.master.destroy()


if __name__ == "__main__":

    hud = PartyHUD()
    hud.run()

    """
    hud = PartyHUD()
    hud.add_character(Params.goron, 3)
    hud.add_character(Params.goron, 5)
    hud.add_character(Params.goron, 3)
    hud.add_item()
    hud.add_item()
    hud.add_item()
    hud.run()
    """
