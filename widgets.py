
from tkinter import *
from tkinter import ttk, filedialog, messagebox, colorchooser
import re, random
from win32api import GetSystemMetrics as ruler
from math import ceil
import cv2
from tkcalendar import Calendar
import ttkthemes
import numpy as np
from textwrap import wrap
from string import punctuation, ascii_lowercase

punctuations = [i for i in punctuation]

s_width = ruler(0)
s_height = ruler(1)

def w(width:float):
    ratio = width / 1366
    return ceil((ratio * s_width))

def h(height:float):
    ratio = height / 768
    return ceil((ratio * s_height))

class Restrict:
    def __init__(self, widget) -> None:
        self.widget = widget

    def restrict_length(self, max_len, add_event = False):
        if add_event:
            self.widget.bind("<KeyRelease>", lambda e: restrict(), add = "+")
        else:
            self.widget.bind("<KeyRelease>", lambda e: restrict())
        def restrict():
            if len(str(self.widget.get())) > max_len:
                try:
                    self.widget.delete(max_len-1, END)
                except TclError:
                    pass
    
    def restrict_delete(self):
        self.widget.bind("<BackSpace>", lambda _: "break")
        self.widget.bind("<Delete>", lambda _: "break")
        self.widget.bind("<KeyPress>", lambda _: "break")
    
class Validate:
    def __init__(self) -> None:
        pass

    def validate_email(self, email):
        email = email.strip()
        if "@gmail.com" in email and not email[0] not in punctuations and " " not in email:
            return True
        elif "@" in email and '.com' in email and "gmail" not in email and email[0] not in punctuations and " " not in email:
            return True
        return False
    
    def all_are_numbers(self, value):
        nums = [str(i) for i in range(10)]
        decision = True
        for i in str(value):
            if i not in nums:
                decision = False
        return decision

    def all_are_letters(self, value):
        letters = [i for i in ascii_lowercase]
        decision = True
        for j in str(value):
            if j not in letters:
                decision = False
            return decision

    def validate_rwf_phone_number(self, phone_number):
        if phone_number.startswith('0') and len(phone_number) == 10 and self.all_are_numbers(phone_number):
            return True
        return False
        
class frame(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master=master,bd = 0, **kwargs)
        num = re.compile("\d{1,}")
        try:
            found_num = num.findall(master['bg'])
            if found_num:
                text = master['bg'][:master['bg'].index(found_num[0])]
                num = int(master['bg'][master['bg'].index(found_num[0]):]) - 3
                self.config(bg = text+str(num))
        except Exception:
            pass

class lframe(LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master = master, font = ('arial', w(12)), bd=0, fg = "gray20", labelanchor='ne', **kwargs)
        num = re.compile("\d{1,}")
        try:
            found_num = num.findall(master['bg'])
            if found_num:
                text = master['bg'][:master['bg'].index(found_num[0])]
                num = int(master['bg'][master['bg'].index(found_num[0]):]) - 3
                self.config(bg = text+str(num))
        except Exception:
            pass

class treeview(ttk.Treeview):
    def __init__(self, master, columns, col_width = w(130), rowheight = h(100),include_index = False, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.master = master

        # self.alter_rows()

        style = ttk.Style()
        style.configure("Treeview", font = ('arial', w(11)), background=master['bg'], fieldbackground=master['bg'], foreground="#000", rowheight = rowheight)
        self.include_index = include_index
        
        self["column"] = columns
        index_zero_width = 0
        index_zero_text = ""

        if self.include_index:
            index_zero_width = w(50)
            index_zero_text = "SN"
        
        self.column("#0", stretch=False, width = index_zero_width)
        self.heading("#0", text = index_zero_text)

        i = 0
        for col in columns:
            self.column(col,width = col_width, stretch=True)
            self.heading(col, text = col, anchor = CENTER)
            i += 1

        self.index_for_single_list_data = 0

        
    def alter_rows(self, odd_color = 'gray70', even_color = 'khaki'):
        style = ttkthemes.ThemedStyle(self.master)
        style.theme_use("clam")
        style.map("Treeview", background=[('selected', 'gray40')], foreground = [('selected', 'gold')])
        self.tag_configure('odd', background=odd_color)
        self.tag_configure('even', background=even_color)


    def insert_data(self,data, wrap_length = 70, odd_color = 'gray70', even_color = 'khaki'):
        self.alter_rows(odd_color=odd_color, even_color=even_color)
        def wrapping(data_list):
            """I assume that datalist is a list as the name implies"""
            all_row = []
            for item in data_list:
                # print(f"CURRENT ITEM: {item}")
                if type(item) == str:
                    wrapped = wrap(item, wrap_length)
                    all_row.append("\n".join(wrapped))
                else:
                    all_row.append(item)
                
            return all_row
                
        try:
            if type(data[0]) not in [list, tuple]:
                if self.include_index:
                    tag = ('odd')
                
                    if self.index_for_single_list_data % 2 ==0:
                        tag = ('even',)
                    data_wrapped = wrapping(data)
                    print(" [K: ] {data_wrapped}")
                    self.insert("", index=self.index_for_single_list_data,text=self.index_for_single_list_data + 1, values = data_wrapped, tags = tag)
                else:
                    data_wrapped = wrapping(data)
                    print(" [I: ] {data_wrapped}")
                    self.insert("", index=self.index_for_single_list_data, values = data_wrapped)
                self.index_for_single_list_data += 1
                
            else:
                for index, row in enumerate(data):
                    tag = ('odd')
                    if self.index_for_single_list_data % 2 ==0:
                        tag = ('even',)
                    if self.include_index:
                        data_wrapped = wrapping(row)
                        print(" [H: ] {data_wrapped}")
                        self.insert("", index=index,text=self.index_for_single_list_data+1, values = data_wrapped, tags=tag)
                    else:
                        data_wrapped = wrapping(row)
                        print(" [G: ] {data_wrapped}")
                        self.insert("", index=index, values = data_wrapped)
                    self.index_for_single_list_data += 1
        except IndexError:
            pass

class btn(Button):
    def __init__(self, master,image = None, **kwargs):
        super().__init__(master=master, compound = "left", bd = 0,font = w(12),image = image, **kwargs)
        
        prev_color = 'gray90'
        # configure save button
        if 'save' in str(self['text']).lower():
            self.config(bg = "#9400D3", fg = "#fff", image = image)
            prev_color = self.cget('bg')
        
        elif 'edit' in str(self['text']).lower():
            self.config(bg = "#0b4", fg = "#fff", image = image)
            prev_color = self.cget('bg')

        elif 'date' in str(self['text']).lower():
            self.config(bg = "#00BFFF", fg = "#000", image = image)
            prev_color = self.cget('bg')
        
        elif "add" in str(self['text']).lower():
            self.config(bg = "#008000", fg = "#fff", image = image)
            prev_color = self.cget('bg')

        elif "delete" in str(self['text']).lower():
            self.config(bg = "#600", fg = "#fff", image=image)
            prev_color = self.cget('bg')

        elif 'set' in str(self['text']).lower():
            self.config(bg = "#DAA520", fg = "#fff", image=image)
            prev_color = self.cget('bg')

        elif 'close' in str(self['text']).lower():
            self.config(image = image, bg = "maroon", fg = "#fff")
            prev_color = self.cget('bg')

        elif 'display' in str(self['text']).lower() or 'show' in str(self['text']).lower(): 
            self.config(bg = "#008080", fg = "#fff", image=image)
            prev_color = self.cget('bg')

        elif "cancel" in str(self['text']).lower():
            self.config(image = image, bg = "gray50")
            prev_color = self.cget('bg')
        
        elif "attach" in str(self["text"]).lower() or "browse" in str(self["text"]).lower():
            self.config(image = image, bg = "#b04", fg = "#fff")
            prev_color = self.cget('bg')
        
        elif "send" in str(self['text']).lower():
            self.config(image = image, bg = "#FF6E00", fg = "#fff")
            prev_color = self.cget('bg')
        
        elif "print" in str(self['text']).lower():
            self.config(bg = "#FEE3B8", image = image)
            prev_color = self.cget('bg')
        
        elif "plan" in str(self['text']).lower():
            self.config(bg = "#600", fg = "#fff", image = image)
            prev_color = self.cget('bg')

        if " all" in str(self['text']).lower():
            self.config(image = image)
        
        if " id" in str(self['text']).lower():
            self.config(image = image)
        
        self.bind('<Enter>', lambda e: self.config(bg = '#39ff13'))
        self.bind('<Leave>', lambda e: self.config(bg = prev_color))
    

class Display_image:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def image(self, img:str):
        try:
            frame = cv2.imread(img)
            cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Image", w(800), h(600))
            cv2.imshow("Image", frame)
        except cv2.error:
            pass

class panedw(ttk.Panedwindow):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)

class EntryBtns:
    def __init__(self, parent, saved_data_holder, entry_tags, entry_fr_height = h(50),
                        entry_fr_side = TOP, fill = X, widget_2_create = 'entry'
                        , browse = False, ent_id_width = 5, default = None):
        
        self.saved_data_holder = saved_data_holder
        self.entry_tags = entry_tags
        self.entry_fr_height = entry_fr_height
        self.entry_fr_side = entry_fr_side
        self.widget_2_create = widget_2_create
        self.default = default

        self.fr = frame(master = parent)
        self.fr.pack(side=entry_fr_side, fill=fill, padx = w(2), expand = True)
        
        if widget_2_create == 'entry':
            self.ent = entry(self.fr, fg="gray50", default=default)
            self.ent.pack(side=LEFT, fill=X, ipadx=w(40), expand = True, pady = h(2))

        elif widget_2_create == 'text':
            self.ent = Textb(self.fr, default=default, height = h(4))
            self.ent.pack(padx = w(1), pady=h(1), side = LEFT, expand = True, fill = X)
                

        self.ent_id = entry(self.fr, width = ent_id_width)
        self.ent_id.pack(side=LEFT, padx = w(2), pady = h(2))
        
        # AVOID EDITING ENT_ID
        self.ent_id.bind("<Enter>", lambda e: self.ent_id.config(state = DISABLED))
        self.ent_id.bind("<Leave>", lambda e: self.ent_id.config(state = NORMAL))

        if browse:
            # IF BROWSE, WHEN USER CLICK IN ENTRY THEN AUTOMATICALLY BROWSE A FILE
            self.ent.bind("<Button-1>", lambda e: Browse.get_file(self = Browse, extensions=".txt .docx .pdf .xlsx .png .jpg",
                                                                   file_holder=self.ent))
        
        btn_width = w(5)
        self.activate_save = btn(master = self.fr, text = "edit", command = lambda: self.activate(), width = btn_width, bg = "#b04", fg = "#fff")
        self.activate_save.pack(side = RIGHT,fill = X, expand=True, padx = w(2), pady = h(2), ipadx = w(25))
        self.save = btn(master = self.fr, text = "save", command = lambda: self.save_data(), width = btn_width, bg = "#0b4")
        self.save.pack(side = RIGHT,fill = X, expand = True, padx = w(2), pady = h(2), ipadx = w(25))
        

    def save_data(self):
        if self.widget_2_create in ['entry', 'combo']:
            if str(self.ent.get()).strip() != self.default:
                data_id = random.randint(1, 1000)
                if data_id in self.entry_tags:
                    while data_id not in self.entry_tags:
                        data_id = random.randint(1, 1000)
                        self.entry_tags.append(data_id)
                        if data_id in self.entry_tags:
                            break
                else:
                    self.entry_tags.append(data_id)
                # ADD DATA TO THE SAVED DATA HOLDER
                try:
                    self.saved_data_holder[data_id] = self.ent.get()
                except TypeError:
                    self.saved_data_holder[data_id] = self.ent.get(0.0, END)
                self.ent_id.delete(0, END)
                self.ent_id.insert(END, data_id)
                        # DISABLE SAVE BTN
                self.save.config(state = DISABLED)

        else:
            if str(self.ent.get(0.0, END)).strip() != self.default:
                id_ = random.randint(1, 1000)
                if id_ in self.entry_tags:
                    while id_ not in self.entry_tags:
                        id_ = random.randint(1, 1000)
                        self.entry_tags.append(id_)
                        if id_ in self.entry_tags:
                            break
                self.entry_tags.append(id_)
                # ADD DATA TO THE SAVED DATA HOLDER
                try:
                    self.saved_data_holder[id_] = self.ent.get()
                except TypeError:
                    self.saved_data_holder[id_] = self.ent.get(0.0, END)
                self.ent_id.delete(0, END)
                self.ent_id.insert(END, id_)

                # DISABLE SAVE BTN
                self.save.config(state = DISABLED)
                
        
    def activate(self):
        self.save.config(state = NORMAL)
        # RESET THE PRE-SAVED DATA FOR THESE CORRESPONDING WIDGET
        try:
            del self.saved_data_holder[int(self.ent_id.get())]
            self.entry_tags.remove(int(self.ent_id.get()))
        except (ValueError, TypeError):
            # USE THESE CODES WHEN WE ARE USING TextbOX INSTEAD OF ENTRYBOX OR COMBOBOX AS DATA GATE
            try:
                del self.saved_data_holder[self.ent_id.get()]
                self.entry_tags.remove(self.ent_id.get())
            except KeyError:
                pass
    
    def get_widgets(self):
        return self.save, self.activate_save, self.ent, self.ent_id, self.fr

# COLOR CHOOSER
def choose_color(color_holder = None):
    color = colorchooser.askcolor(title="Choose a color")
    if color[1] is not None:
        if color_holder:
            color_holder.delete(0, END)
            color_holder.insert(END, color[1])

#==============ENTRY===============
class entry(Entry):
    def __init__(self, master, default = None, font = ('arial', w(12)), **kwargs):
        super().__init__(master = master, bg = master['bg'], highlightbackground='gray50', highlightcolor="gray50", highlightthickness=1,bd=0, font = font, **kwargs)
        
        if default:
            self.bind("<KeyPress>", lambda e: remove_txt())
            self.bind("<Leave>", lambda e: add_txt())
            self.delete(0, END)
            self.insert(END, default)
            self.config(fg = "gray50")

        num = re.compile("\d{1,}")
        try:
            found_num = num.findall(master['bg'])
            if found_num:
                text = master['bg'][:master['bg'].index(found_num[0])]
                num = int(master['bg'][master['bg'].index(found_num[0]):]) - 3
                self.config(bg = text+str(num))
        except Exception:
            pass

        def remove_txt():
            if default.strip() in str(self.get()).strip():
                self.delete(0, END)
                self.config(fg = "#000")
        
        def add_txt():
            if len(str(self.get()).strip()) == 0:
                self.insert(END, default)
                self.config(fg = "gray50")


#=====================COMBOBOX=======================
class combo(ttk.Combobox):
    def __init__(self, master, label_txt = None, label_side = LEFT,bd_color = "#0b4", default = None, **kwargs):
        super().__init__(master, font = ('arial', w(12)),**kwargs)
        self.master = master
        self.st = ttk.Style()
        self.st.theme_use('clam')
        
        self.st.configure('comb.TCombobox', foreground = "#023", fieldbackground = self.master['bg'],
                            bordercolor = bd_color, background = bd_color)
        try:
            if label_txt:
                label(master=self.master, text = label_txt).pack(side = label_side, padx = w(2), pady=w(2))
        except Exception:
            pass
        
        def remove_default():
            if self.get() == default:
                self.set('')
        
        def set_default():
            print("LEAVING COMBOBOX.....")
            if self.get().strip() == "" or len(self.get().strip()) == 0:
                self.set(default)
                print("[DEFAULT SET]")
            else:
                print(f"COMBO VALUE FOUND: {self.get().strip()}: length: {len(self.get().strip())}")

        if self.cget('state') != 'readonly':
            if default:
                self.set(default)
                self.bind("<Button-1>", lambda e: remove_default())
                self.bind("<Leave>", lambda e: set_default())

    
class checkb(ttk.Checkbutton):
    def __init__(self, master, **kwargs):
        super().__init__(master = master, **kwargs)
        style = ttk.Style()
        style.configure("TCheckbutton", background = master['bg'], foreground="#023", font=("Arial", w(12)))
    
class radiob(ttk.Radiobutton):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)
        style = ttk.Style()
        style.configure("Custom.TRadiobutton", background = master['bg'], foreground= "#045", 
                        font=("Arial", w(12)))   

class Scrol(ttk.Scrollbar):
    def __init__(self, master, **kwargs):
        """YOU SHOULD USE CONFIG TO SET THE COMMAND OF THIS SCROLLBAR"""
        super().__init__(master = master, **kwargs)
        scr_style = ttk.Style()
        scr_style.configure('Vertical.TScrollbar', background = "#023", bordercolor = "#0b4", arrowcolor = "#0b4")
        scr_style.configure('Horizontal.TScrollbar', background = "#023", bordercolor = "#0b4", arrowcolor = "#0b4")

class Scrol_frame(Canvas):
    def __init__(self, master, scr_x = None, scr_y = None, **kwargs):
        super().__init__(master = master,bg = master['bg'], **kwargs) # master = master,

        self.Scrol_frame = frame(self)

        self.Scrol_frame.bind("<Configure>", lambda e: self.configure(scrollregion = self.bbox("all")))
        self.create_window((0, 0), window = self.Scrol_frame, anchor = "nw")
        if scr_y:
            self.config(yscrollcommand = scr_y.set)
            scr_y.config(command = self.yview)
            scr_y.pack(side = RIGHT, pady = h(1), padx = w(1),fill = Y)
        if scr_x:
            self.config(xscrollcommand = scr_x.set)
            scr_x.config(command = self.xview)
            scr_x.pack(side = BOTTOM, pady = h(2), padx = w(1), fill = X, expand = True, anchor = S)

        num = re.compile("\d{1,}")
        try:
            found_num = num.findall(master['bg'])
            if found_num:
                text = master['bg'][:master['bg'].index(found_num[0])]
                num = int(master['bg'][master['bg'].index(found_num[0]):]) - 3
                self.config(bg = text+str(num))
        except Exception:
            pass

    def scr_fr(self):
        return self.Scrol_frame

class label(Label):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, font = ('arial', w(12)), bg = master['bg'], **kwargs)

class Textb(Text):
    def __init__(self, master, hbg = "gray80", default = None, **kwargs):
        super().__init__(master, font = ('arial', w(12)), highlightbackground=hbg, highlightcolor=hbg, highlightthickness=1, bg = master['bg'],fg = "gray30", bd = 0, **kwargs)
        if default:
            self.bind("<KeyPress>", lambda e: remove_txt())
            self.bind("<Leave>", lambda e: add_txt())

            self.delete(0.0, END)
            self.insert(END, default)
            
        def remove_txt():
            if default.strip() in str(self.get(0.0, END)).strip():
                self.delete(0.0, END)
                self.config(fg = "#000")
        
        def add_txt():
            if len(str(self.get(0.0, END)).strip()) == 0:
                self.insert(END, default)
                self.config(fg = "gray30")
        num = re.compile("\d{1,}")
        try:
            found_num = num.findall(master['bg'])
            if found_num:
                text = master['bg'][:master['bg'].index(found_num[0])]
                num = int(master['bg'][master['bg'].index(found_num[0]):]) - 3
                self.config(bg = text+str(num))
        except Exception:
            pass


class spinbox(ttk.Spinbox):
    def __init__(self, master, **kwargs):
        super().__init__(master =master, **kwargs)

class calendar(Calendar):
    def __init__(self, master, global_date_holder:Variable, date_holder_widget = None, create_toplevel = False, **kw):
        super().__init__(master = master, **kw)
        self.master = master
        self.global_time_holder = global_date_holder
        self.datetime_fr = None
        self.choosen_date = date_holder_widget
        if not create_toplevel:
            self.datetime_fr = lframe(self.master)
            self.datetime_fr.pack(side=RIGHT, padx = w(2))
        else:
            # CREATE TOPLEVEL WINDOW TO HOLD THE CALENDAR AND THE TIME SELECTOR
            self.datetime_fr = Toplevel()
            self.datetime_fr.title("Select time and date")
            self.datetime_fr.geometry(f'{w(250)}x{h(480)}')
            # self.datetime_fr.resizable(False, False)
            # self.datetime_fr.iconbitmap("images/clock.ico")
            self.datetime_fr.resizable(False, False)
        
        # MAKE CALENDAR
        self.make_cal()

    def make_cal(self):
        self.datetime_fr1 = lframe(self.datetime_fr)
        self.datetime_fr2 = lframe(self.datetime_fr)
        self.datetime_fr3 = lframe(self.datetime_fr)
        self.datetime_fr1.pack(fill = X)
        self.datetime_fr2.pack(fill = X)
        self.datetime_fr3.pack(fill = X)

        cal = Calendar(self.datetime_fr1, weekendbackground = "pink", weekendforeground = "#000", selectmode = "day")
        cal.pack(fill = BOTH, expand = True)

        time_fr = lframe(self.datetime_fr2, width = w(50))
        time_fr.pack(padx = w(2), fill=BOTH)
        label(time_fr, text = "Hour").pack(side = TOP, fill = X, pady = h(1))
        hour = spinbox(time_fr, from_=0, to=23)
        hour.pack(side = TOP, fill = X)
        Label(time_fr, text = "Minute").pack(side = TOP, fill = X, pady = h(1))
        minute = spinbox(time_fr, from_=0, to=59)
        minute.pack(side = TOP, fill = X, pady = h(1))
        Label(time_fr, text = "Second").pack(side = TOP, fill = X, pady = h(1))
        second = spinbox(time_fr, from_=0, to=59)
        second.pack(side = TOP, fill = X, pady = h(1))
        

        def set_selected():
            global global_date_holder
            data = str(cal.get_date()).split("/")
            h = str(hour.get())
            m = str(minute.get())
            s = str(second.get())
            if len(data[0]) != 2:
                data[0] = "0"+data[0]
            if len(data[1]) != 2:
                data[1] = "0"+data[1]
            if len(data[2]) != 4:
                data[2] = "20"+data[2]
            if len(h) != 2:
                h = "0" + h
            if len(m) != 2:
                m = "0" + m
            if len(s) != 2:
                s = "0" + s
            final_datetime = data[2] + "-" + data[0] + "-" + data[1] + " " + f"{h}:{m}:{s}"
            # COPY THE SELECTED DATE AND TIME
            # clipboard(data = final_datetime, action = "copy")
            # GLOBALIZE SELECTED DATE
            global_date_holder = final_datetime
            
            if self.choosen_date:
                try:
                    self.choosen_date.delete(0, END)
                    self.choosen_date.insert(END, final_datetime)
                except Exception:
                    try:
                        self.choosen_date.delete(0.0, END)
                        self.choosen_date.insert(END, final_datetime)
                    except Exception:
                        pass
            self.datetime_fr.destroy()
            
            
        set_date = btn(master=self.datetime_fr3, text = "set date", command = set_selected)
        set_date.pack(side=LEFT, fill=X, expand=True)
        close = btn(master=self.datetime_fr3, text = "close", 
                         command = lambda: self.datetime_fr.destroy())
        close.pack(side=LEFT, fill=X, expand = True)

class Browse:
    def __init__(self):
        pass
    
    def get_file(self, extensions: str, file_holder:Entry):
        file = filedialog.askopenfilename(filetypes = [('All file', extensions)])
        file_holder.delete(0, END)
        file_holder.insert(END, file)
        file_holder.focus()
    
    def browse_path(self, dir_holder = None):
        dir = filedialog.askdirectory()
        if dir_holder:
            dir_holder.delete(0, END)
            dir_holder.insert(END, dir)
        else:
            return dir

class LoginSignup:
    def __init__(self,master,width = w(450), height = h(250), login = False, frame_pack_side = TOP) -> None:
        self.base_frame = lframe(master, width = width, height = height)
        self.base_frame.config(bd = 1)
        self.base_frame.pack(side = frame_pack_side, padx = w(1), pady = h(1))
        self.base_frame.pack_propagate(False)
        self.base_frame.config(bg = "beige")

        self.login_frame = []
        self.signup_frame = []

        if login:
            self.login()
        else:
            self.signup()

    def login(self):
        global lusername, lpassword, login_btn
        for fr in self.login_frame:
            fr.destroy()

        login_fr = frame(self.base_frame)
        login_fr.pack(fill = BOTH, expand = True)
        self.login_frame.append(login_fr)
        self.signup_frame.append(login_fr)

        # title
        title = label(login_fr, text = "Login")
        title.config(font = ('arial',w(30), "bold"), fg = "#089")
        title.pack(side = TOP, pady = h(1), padx = w(1))
        self.login_frame.append(title)

        # username
        lusername = entry(login_fr, default="Enter username")
        lusername.config(font = 20)
        lusername.pack(side = TOP, pady = h(4), padx = w(1), fill = X, expand = True)

        # password
        lpassword = entry(login_fr, default="Enter password")
        lpassword.pack(side = TOP, pady = h(2), padx = w(1), fill = X, expand = True)

        btns = frame(login_fr)
        btns.config(bg = login_fr['bg'])
        btns.pack(fill = X, side = BOTTOM, expand = True, padx = w(1), pady = h(1), anchor=S)

        login_btn = btn(btns, text = "sign in")
        login_btn.config(bg = "#b04", fg = "#fff")
        login_btn.pack(side = LEFT, padx = w(3), expand = True, fill = X)

        signup_btn = btn(btns, text = "Sign up", command = self.signup)
        signup_btn.config(bg = "#023", fg = "#fff")
        signup_btn.pack(side = LEFT, padx = w(3), expand = True, fill = X)


        cancel_btn = btn(btns, text = "cancel", command = lambda: self.base_frame.destroy())
        cancel_btn.config(bg = "#600", fg = "#fff")
        cancel_btn.pack(side = RIGHT, padx = w(3), expand = True, fill = X)
    
    @property
    def Login_btn(self):
        return login_btn

    def login_user_data(self):
        return lusername.get(), lpassword.get()

    def signup(self):
        global signup_btn, username, password, re_password
        for fr in self.signup_frame:
            fr.destroy()
            
        signup_fr = frame(self.base_frame)
        signup_fr.pack(fill = BOTH, expand = True)
        signup_fr.pack_propagate(False)
        self.signup_frame.append(signup_fr)
        self.login_frame.append(signup_fr)
        
        # title
        title = label(signup_fr, text = "Sign up")
        title.config(font = ('arial',w(30), "bold"), fg = "#089")
        title.pack(side = TOP, pady = h(1), padx = w(1))
        self.signup_frame.append(title)
        
        # username
        username = entry(signup_fr, default="Enter username")
        username.pack(side = TOP, pady = h(1), padx = w(3), fill = X, expand = True)

        # password
        password = entry(signup_fr, default="Enter password (8 characters min)")
        password.pack(side = TOP, pady = h(1), padx = w(3), fill = X, expand = True)

        re_password = entry(signup_fr, default="Re-type password")
        re_password.pack(side = TOP, pady = h(1), padx = w(3), fill = X, expand = True)

        btns = frame(signup_fr)
        btns.config(bg = signup_fr['bg'])
        btns.pack(fill = X, side = TOP, expand = True, padx = w(1), pady = h(1), anchor=S)

        login_btn = btn(btns, text = "login", command = self.login)
        login_btn.config(bg = "#b04", fg = "#fff")
        login_btn.pack(side = LEFT, padx = w(1), expand = True, fill = X)

        signup_btn = btn(btns, text = "Sign up")
        signup_btn.config(bg = "#023", fg = "#fff")
        signup_btn.pack(side = LEFT, padx = w(1), expand = True, fill = X)

        cancel_btn = btn(btns, text = "cancel", command = lambda: self.base_frame.destroy())
        cancel_btn.config(bg = "#600", fg = "#fff")
        cancel_btn.pack(side = LEFT, padx = w(1), expand = True, fill = X)

    @property
    def Signup_btn(self):
        return signup_btn
    
    def signup_user_data(self):
        return username.get(), password.get(), re_password.get()

class Table_gui:
    def __init__(self, parent):
        self.rows = 1
        self.cols = 1
        self.data = []
        self.entries = []
        self.cols_created = []

        # BASE FRAME
        self.base_frame = frame(parent)
        self.base_frame.pack(fill = X, expand = True, padx = w(1), pady = h(1), side = LEFT)

        self.btn_frame = frame(self.base_frame)
        self.btn_frame.pack(side = BOTTOM, fill = X, expand = True, padx = w(1), pady = h(1))

        self.row = btn(self.btn_frame, text = "add row", command=self.make_row)
        self.row.pack(side = LEFT, padx = w(1), pady = h(1), anchor=W)

        self.col = btn(self.btn_frame, text = "add column", command= lambda: self.make_column(self.base_frame))
        self.col.pack(side = LEFT, padx = w(1), pady = h(1), anchor=W)

        # INITIAL COLUMN AT START
        self.make_column(self.base_frame)
    
    def entry(self, frame:Frame):
        e = entry(frame)
        e.bind("<KeyRelease>", lambda e: replace_empty_in_data())
        e.pack(side = TOP, padx = w(1), pady = h(1), fill = X, expand = True)
        # TRACK THE ANCHORED ENTRY IN THE LIST OF ENTRIES AND BE ABLE TO REPLACE ITS VALUE IN THE DATA
        def replace_empty_in_data():
            found = False
            for index,row in enumerate(self.entries):
                for data_index, entry in enumerate(row):
                    if e == entry:
                        self.data[index][data_index] = e.get()
                        found = True
                # IF THE ENTRY POSITION WAS FOUND, STOP ITERATION FROM CONTINUING BECAUSE THERE IS NO DUPLICATES IN ENTRIES CREATED
                if found:
                    break
            # DISPLAY THE UPDATE DATAFRAME
            self.final_data()

        return e
    
    def frame(self, parent):
        f = frame(parent)
        f.pack(side = LEFT, padx = w(1), pady = h(1), fill = X, expand = True)
        return f
    
    def make_row(self):
        """if the row is created the entries are spreaded across the whole columns, so i need to know what the are the available column
        so that I can spread an entry across the those columns. defautly, the column 1 should be created as I make the instance of the class"""
        for index,row in enumerate(self.entries):
            ent = self.entry(self.cols_created[index])
            #APPEND THIS ENTRY TO THE ENTRIES AVAILABLE FOR ALL THE COLUMBS
            row.append(ent)
            # APPEND THE POSITION HOLDER OF THIS COLUMN IN THE DATA
            self.data[index].append('')
        self.rows += 1

    def make_column(self, parent):
        for i in range(self.cols):
            fr = self.frame(parent)
            self.cols_created.append(fr)
            # HOLD VALUES
            self.data.append([])
            # HOLD ENTRIES
            self.entries.append([])
            for j in range(self.rows):
                ent = self.entry(fr)
                self.entries[-1].append(ent)
                self.data[-1].append('')
    
    def final_data(self):
        # BY NOW, THE DATAFRAME WILL BE BEING DISLPLAY IN THE TERMINAL
        nd = np.array(self.data)
        transposed_data = nd.T
        return transposed_data.tolist()


class Modify:
    def __init__(self, parent):
        """bind a widget to button-3: right mouse click and then extend the functionalities"""
        self.parent = parent

    def widget_triger(self, widget, btns = 4, btn_labels = {'1':'delete', '2':'edit', '3':'status', '4':'details'}):
        """event: like `<Button-1>`"""
        fr = frame(self.parent)
        fr.place(x = widget.winfo_rootx(), y = widget.winfo_rooty(), width = w(250), height = h(30*btns))

        # delete member from the database
        delete_btn = btn(fr, text = btn_labels['1'], activebackground = fr.cget('bg'))
        delete_btn.bind("<Button-1>", lambda e: fr.destroy(), add = "+")
        delete_btn.pack(side = TOP, padx = w(1), pady = h(0), fill=X, expand = True, anchor = NW)

        # change name, qualification, department, knowledgeability and so on
        edit_btn = btn(fr, text = btn_labels['2'], activebackground = fr.cget('bg'))
        edit_btn.bind("<Button-1>", lambda e: fr.destroy(), add = "+")
        edit_btn.pack(side = TOP, padx = w(1), pady = h(0), fill=X, expand = True, anchor = NW)

        # in work, in leave, idle or other status
        status = btn(fr, text = btn_labels['3'], activebackground = fr.cget('bg'), bg = "#112200", fg = "#fff")
        status.bind("<Button-1>", lambda e: fr.destroy(), add = "+")
        status.pack(side = TOP, padx = w(1), pady = h(0), fill=X, expand = True, anchor = NW)

        # to get the data analysis of single clicked employee or else member
        details = btn(fr, text = btn_labels['4'], activebackground = fr.cget('bg'), bg = "#ffaa00")
        details.bind("<Button-1>", lambda e: fr.destroy(), add = "+")
        details.pack(side = TOP, padx = w(1), pady = h(0), fill=X, expand = True, anchor = NW)

        close_btn = btn(fr, text = "close",activebackground = fr.cget('bg'), command = lambda: fr.destroy())
        close_btn.pack(side = TOP, padx = w(1), pady = h(0), fill=X, expand = True, anchor = NW)

        return delete_btn, edit_btn, status, details



# CONSTANTS
comb_syle = 'comb.TCombobox'
check_style = "TCheckbutton"
radio_style = "Custom.TRadiobutton"
