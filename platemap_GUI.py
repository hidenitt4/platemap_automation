from tkinter import PhotoImage
import tkinter as tk
import tkcalendar
import customtkinter as ctk
from customtkinter import filedialog
from pathlib import Path
import subprocess
from PIL import Image
from construct_platemap import get_unique_drugs, construct_platemap



def add_placeholder(event=None):
    if txtbox_1.get("1.0", "end-1c") == "":
        txtbox_1.insert("1.0", placeholder_text)


def remove_placeholder(event=None):
    if txtbox_1.get("1.0", "end-1c") == placeholder_text:
        txtbox_1.delete("1.0", "end")

def optionmenu_callback(choice):
    print("optionmenu dropdown clicked:", choice)


def get_text():
    input_txt = txtbox_1.get("1.0", "end-1c")
    pw_combos = input_txt.split()
    # cmd = ['Rscript', 'denovo_generation_handmade_layout (1).R', input_txt]
    # subprocess.run(cmd)
    unique_drugs = get_unique_drugs(pw_combos)
    user_inputs = get_user_inputs()

    if any(x in ['Experiment Type','Condition','Strain', None] for x in user_inputs):
        incomplete_window = ctk.CTkToplevel(root)
        incomplete_window.title('Incomplete inputs')
        incomplete_window.geometry('230x100')
        incomplete_window.grid_columnconfigure((0), weight=1)
        # Label
        labeli = ctk.CTkLabel(master=incomplete_window, text='Please select all inputs', anchor='center')
        labeli.grid(row=0, sticky='ew', pady=2, padx=10)

        # Button
        button_i = ctk.CTkButton(master=incomplete_window, text='Close Window', command=lambda: close_window(incomplete_window))
        button_i.grid(row=1, stick='ew', pady=2, padx=10)

    else:
        construct_platemap(unique_drugs, pw_combos, user_inputs)
        success_message()
        print('Platemaps successfully created')

    return

def success_message():
    new_window = ctk.CTkToplevel(root)
    new_window.title('Update')
    new_window.geometry('230x100')
    new_window.grid_rowconfigure(0, weight=1)
    # Label
    label = ctk.CTkLabel(master=new_window, text='Platemaps successfully created!', anchor='w')
    label.grid(row=0,sticky='ew',pady=0,padx=15)

    # Button
    button_0 = ctk.CTkButton(master=new_window, text='Close Window', command=lambda: close_window(new_window))
    button_0.grid(row=1,stick='ew',pady=2,padx=20)

def close_window(frame):
    frame.destroy()
    frame.update()

    return

def calendar():
    global calendar_popup, calendar
    calendar_popup=ctk.CTkToplevel(root)
    calendar_popup.title('Input Experiment Date')
    calendar_popup.geometry('400x400')
    calendar = tkcalendar.Calendar(calendar_popup, font='Georgia 14', selectmode='day',borderwidth=10,
                                   foreground='black',othermonthweforeground='gray85',
                                   othermonthforeground='gray85',selectforeground='springgreen3')
    calendar_popup.grid_rowconfigure(0, weight=1)
    calendar_popup.grid_columnconfigure(0, weight=1)
    calendar.bind('<<CalendarSelected>>', lambda event: update_date_entry(calendar))
    calendar.grid(row=0,column=0,stick='nsew',pady=2,padx=20)


    # Calendar close_window button
    button_c = tk.Button(master=calendar_popup, text='Close Window', command=lambda: close_window(calendar_popup))
    button_c.grid(row=1,column=0, stick='ew', pady=2, padx=20)

    return

def update_date_entry(calendar):
    selected_date = calendar.selection_get()
    date_entry.configure(text=f'Selected Date: {selected_date}')
    print(f'{selected_date}')

    root.geometry('525x425')
    root.after(200, lambda: close_window(calendar_popup))


def clear_all():
    global optionmenu_var_1, optionmenu_var_2, optionmenu_var_3, date_entry
    txtbox_1.delete("1.0", "end")
    add_placeholder()

    optionmenu_var_1.set("Experiment Type")
    optionmenu_var_2.set("Condition")
    optionmenu_var_3.set("Strain")
    date_entry.configure(text='Select Date')
    root.geometry('500x425')

    return

def get_user_inputs():
    global optionmenu_var_1, optionmenu_var_2, optionmenu_var_3, calendar
    exp_type = optionmenu_var_1.get()
    condition = optionmenu_var_2.get()
    strain = optionmenu_var_3.get()

    try:
        selected_date = str(calendar.selection_get())
    except:
        selected_date = None

    return (exp_type, condition, strain, selected_date)

def to_page1():
    page2.configure(fg_color='gray92')
    frame_1.configure(fg_color='gray86')
    button_frame.configure(fg_color='gray86')
    frame_1.tkraise()
    button_frame.tkraise()

def to_page_2():
    frame_1.configure(fg_color='gray92')
    button_frame.configure(fg_color='gray92')
    page2.configure(fg_color='gray86')
    page2.tkraise()

def grab_file1():
    file_path = Path.home() / 'Downloads'
    filedialog.askopenfilename(title='Select file', filetypes=[('Excel file', '*.xlsx')],initialdir=f'{file_path}')

    return

# for-fun features
def toggle_color():

    global count, color_cycle, switch

    if not switch:
        switch = True
        change_color()
    else:
        switch = False
        revert_color()

def change_color():
    global count, color_cycle, switch

    if switch:
        if count < len(color_cycle):
            label.configure(text_color = color_cycle[count],text='EPILEPSY')
            count+=1
            root.after(100, change_color)

            if count+1 == len(color_cycle):
                count = 0

def revert_color():
    global count, color_cycle

    label.configure(text_color='gray5', text='Construct Platemap')




if __name__ == '__main__':
    count = 0
    color_cycle = ['gray5','deep pink','SlateBlue2','dark turquoise','orange','yellow3']
    switch = True

    # Establish GUI

    ctk.set_appearance_mode('light')
    ctk.set_default_color_theme('green')

    root = ctk.CTk()
    root.geometry('500x425')
    root.title('DiaMOND Tech')

    ## PAGE 1
    # Frame_1

    frame_1 = ctk.CTkFrame(master = root)
    frame_1.grid(row=0,column=0,pady=20,padx=15,sticky='nsew')
    frame_1.rowconfigure((0,1), weight=1)
    frame_1.columnconfigure((0,1), weight=1)

        # Title
    label = ctk.CTkLabel(master=frame_1, text='Construct Platemap', font=('Georgia', 24))
    label.grid(row=0,column=0,pady=12, padx=10,sticky='ew',columnspan=2)
    label.bind('<Button-1>', lambda event: toggle_color())

    # Frame_2
    frame_2 = ctk.CTkFrame(master=frame_1)
    frame_2.grid(row=1, column=0, pady=15, padx=15,sticky='nsew')
        # Textbox
    txtbox_1 = ctk.CTkTextbox(master=frame_2)
    txtbox_1.grid(row=1,column=0,pady=15, padx=10,sticky='nsew')

    placeholder_text = 'Enter PW combos here'
    add_placeholder()

    txtbox_1.bind("<Enter>", lambda event: root.after(500, remove_placeholder()))
    txtbox_1.bind("<Leave>", lambda event: root.after(500,add_placeholder()))

    # Frame_3
    frame_3 = ctk.CTkFrame(master=frame_1)
    frame_3.grid(row=1,column=1,pady=10,padx=20,sticky='w')
        # Dropdown options
        # 1
    optionmenu_var_1 = ctk.StringVar(value="Experiment Type")
    optionmenu_1 = ctk.CTkOptionMenu(frame_3, values=["Compendium", "Dose Center"],
                                             command=optionmenu_callback,
                                             variable=optionmenu_var_1)
    optionmenu_1.grid(row=1,pady=15, padx=10)
        # 2
    optionmenu_var_2 = ctk.StringVar(value="Condition")
    optionmenu_2 = ctk.CTkOptionMenu(frame_3, values=["Rich Growth", "Butyrate", "Valerate","Cholesterol",
                                                      "Nitrate","Low pH"],
                                     command=optionmenu_callback,
                                     variable=optionmenu_var_2)
    optionmenu_2.grid(row=2, pady=15, padx=10)
        # 3
    optionmenu_var_3 = ctk.StringVar(value="Strain")
    optionmenu_3 = ctk.CTkOptionMenu(frame_3, values=["Erdman","Other"],
                                     command=optionmenu_callback,
                                     variable=optionmenu_var_3)
    optionmenu_3.grid(row=3, pady=15, padx=10)
        # DateEntry
    date_entry_frame = ctk.CTkFrame(master=frame_3)
    date_entry_frame.grid(row=4, pady=2, padx=2, sticky='ew')
    date_entry_frame.rowconfigure(3, weight=1)

    date_entry = ctk.CTkButton(master=date_entry_frame, text='Select Date', command= calendar)
    date_entry.grid(row=3, pady=10, padx=10, sticky='ew')


    # Frame_4 or button frame
    button_frame = ctk.CTkFrame(master=root)
    button_frame.grid(row=1, column=0, pady=0, padx=5, sticky='nsew')
    button_frame.grid_rowconfigure((0), weight=4)
    button_frame.grid_rowconfigure((2), weight=2)
    button_frame.grid_columnconfigure((0, 1), weight=1)

        # Buttons
        # Construct
    button_1 = ctk.CTkButton(master=button_frame, text='Construct', command=lambda: get_text())
    button_1.grid(row=1, column=0,padx=10, pady=20,sticky='e')
        # Clear
    button_2 = ctk.CTkButton(master=button_frame, text='Clear all', command=clear_all,fg_color='gray',
                             hover_color='gray20')
    root.bind('<`>', lambda event: toggle_color())
    button_2.grid(row=1, column=1,padx=10, pady=20,sticky='w')



    ## PAGE 2

    page2 = ctk.CTkFrame(master=root)
    page2.grid(row=0, column=0, pady=20, padx=15, sticky='nsew',rowspan=2)

    button_4 = ctk.CTkButton(master=page2, text='Previous page', command=lambda: to_page1(), fg_color='gray',
                             hover_color='gray20')
    button_4.grid(row=0, column=0, padx=10, pady=20, sticky='w')


    # Frame_1, next page button
    img1 = ctk.CTkImage(Image.open('888647-200.png'), size=(30, 30))
    img_button1 = ctk.CTkLabel(master=button_frame, text='', image=img1)
    img_button1.bind('<Button-1>', lambda event: to_page_2())

    img_button1.grid(row=1, column=2, padx=10, pady=20, sticky='w')

    # File dialog

    button_5 = ctk.CTkButton(master=page2, text='Select file', command=lambda: grab_file1(), fg_color='gray',
                             hover_color='gray20')
    button_5.grid(row=0, column=1, padx=10, pady=20, sticky='w')

    to_page1()
    root.mainloop()




