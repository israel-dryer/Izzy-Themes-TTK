import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widget import *
from tkinter import Variable
from tkinter import font

DEFAULT_THEME = 'litera'

ZEN = """Beautiful is better than ugly. 
Explicit is better than implicit. 
Simple is better than complex. 
Complex is better than complicated.
Flat is better than nested. 
Sparse is better than dense.  
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!"""


def setup_demo(window: ttk.Window):

    def change_theme(e):
        window.style.theme_use(root.tk.getvar('selectTheme'))

    root = Frame(window, padding=10)
    theme_names = app.style.theme_names()

    # setup variables
    root.tk.setvar('selectTheme', DEFAULT_THEME)

    # header frame
    header = Frame(root, padding='10 10 10 0')
    title = Label(header, textvariable='selectTheme', font='TkTitleLarge')
    #cbo_lbl = Label(header, text="Select a theme:")
    #cbo = Combobox(header, textvariable='selectTheme', values=theme_names)
    #cbo.bind("<<ComboboxSelected>>", change_theme)

    # header frame geometry
    header.pack(fill=X)
    title.pack(side=LEFT)
    #cbo.pack(side=RIGHT)
    #cbo_lbl.pack(side=RIGHT, padx=10)

    # Separator(root).pack(pady=10, padx=10, fill=X)

    left_frm = Frame(root, padding=5)
    left_frm.pack(side=LEFT, fill=X, expand=True, anchor=NW)

    right_frm = Frame(root, padding=5)
    # right_frm.pack(side=RIGHT, anchor=NE)

    color_group = Labelframe(left_frm, text="Theme color options", padding=10)
    #color_group.pack(side=TOP)

    for color in window.style.theme_current().scheme:
        color_btn = Button(color_group, text=color, bootstyle=color)
        color_btn.pack(side=LEFT, expand=YES, padx=5, fill=X)

    option_group = Labelframe(left_frm, text="Checkbuttons & radiobuttons",
                              padding=10)
    #option_group.pack(fill=X, pady=10, side=TOP)

    check1 = Checkbutton(option_group, text="selected")
    check1.pack(side=LEFT, expand=YES, padx=5)
    check1.invoke()

    check2 = Checkbutton(option_group, text="alternate")
    check2.pack(side=LEFT, expand=YES, padx=5)

    check4 = Checkbutton(option_group, text="deselected")
    check4.pack(side=LEFT, expand=YES, padx=5)
    check4.invoke()
    check4.invoke()

    check3 = Checkbutton(option_group, text="disabled", state=DISABLED)
    check3.pack(side=LEFT, expand=YES, padx=5)

    radio1 = Radiobutton(option_group, text="selected", value=1)
    radio1.pack(side=LEFT, expand=YES, padx=5)
    radio1.invoke()

    radio2 = Radiobutton(option_group, text="deselected", value=2)
    radio2.pack(side=LEFT, expand=YES, padx=5)

    radio3 = Radiobutton(option_group, text="disabled", value=3,
                         state=DISABLED)
    radio3.pack(side=LEFT, expand=YES, padx=5)

    # table_frm = Frame(left_frm)
    # table_frm.pack(pady=5, fill=X, side=TOP)

    table_data = [
        ("South Island, New Zealand", 1),
        ("Paris", 2),
        ("Bora Bora", 3),
        ("Maui", 4),
        ("Tahiti", 5),
    ]

    # tv = Treeview(table_frm, columns=[0, 1], show=HEADINGS, height=5)
    # for row in table_data:
    #     tv.insert("", END, values=row)
    #
    # tv.selection_set("I001")
    # tv.heading(0, text="City")
    # tv.heading(1, text="Rank")
    # tv.column(0, width=300)
    # tv.column(1, width=70, anchor=CENTER)
    # tv.pack(side=LEFT, anchor=NE, fill=X)

    # # notebook with table and text tabs
    # nb = Notebook(table_frm)
    # nb.pack(side=LEFT, padx=(10, 0), expand=YES, fill=BOTH)
    # nb_text = "This is a notebook tab.\nYou can put any widget you want here."
    # nb.add(Label(nb, text=nb_text), text="Tab 1", sticky=NW)
    # nb.add(Label(nb, text="A notebook tab."), text="Tab 2", sticky=NW)
    # nb.add(Frame(nb), text="Tab 3")
    # nb.add(Frame(nb), text="Tab 4")
    # nb.add(Frame(nb), text="Tab 5")

    # text widget
    #txt = ScrolledText(master=lframe, height=5, width=50, autohide=True)
    #txt.insert(END, ZEN)
    #txt.pack(side=LEFT, anchor=NW, pady=5, fill=BOTH, expand=YES)
    left_frm_inner = Frame(left_frm)
    left_frm_inner.pack(fill=BOTH, expand=YES, padx=10)
    scale1 = Scale(left_frm_inner, orient=HORIZONTAL, value=75, from_=100,
                   to=0)
    scale1.pack(fill=X, pady=5, expand=YES)

    Progressbar(left_frm_inner, orient=HORIZONTAL, value=50).pack(
        fill=X, pady=5, expand=YES)

    Progressbar(left_frm_inner, orient=HORIZONTAL, value=75, bootstyle=SUCCESS
                ).pack(fill=X, pady=5, expand=YES)

    # m = ttk.Meter(
    #     master=lframe_inner,
    #     metersize=150,
    #     amountused=45,
    #     subtext="meter widget",
    #     bootstyle=INFO,
    #     interactive=True,
    # )
    # m.pack(pady=10)

    sb = Scrollbar(left_frm_inner, orient=HORIZONTAL)
    sb.set(0.1, 0.9)
    sb.pack(fill=X, pady=5, expand=YES)

    sb = Scrollbar(left_frm_inner, orient=HORIZONTAL, bootstyle=DANGER)
    sb.set(0.1, 0.9)
    sb.pack(fill=X, pady=5, expand=YES)

    button_group = Labelframe(right_frm, text="Buttons", padding=(10, 5))
    button_group.pack(fill=X)

    # menu = ttk.Menu(root)
    # for i, t in enumerate(window.style.theme_names()):
    #     menu.add_radiobutton(label=t, value=i)
    #
    # default = Button(button_group, text="solid button")
    # default.pack(fill=X, pady=5)
    # default.focus_set()
    #
    # mb = Menubutton(button_group, text="solid menubutton", menu=menu)
    # mb.pack(fill=X, pady=5)
    # print(mb.configure('style'))
    #
    #
    #
    # cb = Checkbutton(button_group, text="solid toolbutton", bootstyle=SUCCESS)
    # cb.invoke()
    # cb.pack(fill=X, pady=5)
    #
    # ob = Button(button_group, text="outline button",
    #             bootstyle='info-outline-button')
    # ob.pack(fill=X, pady=5)
    #
    # mb = Menubutton(button_group, text="outline menubutton",
    #                 bootstyle='outline-menubutton', menu=menu)
    # mb.pack(fill=X, pady=5)
    #
    # cb = Checkbutton(button_group, text="outline toolbutton",
    #                  bootstyle='success-outline-toolbutton')
    # cb.pack(fill=X, pady=5)
    #
    # lb = Button(button_group, text="link button", bootstyle='link-button')
    # lb.pack(fill=X, pady=5)
    #
    # cb2 = Checkbutton(button_group, text="switch", bootstyle='switch')
    # cb2.pack(fill=X, pady=5)
    # cb2.invoke()
    #
    # input_group = Labelframe(right_frm, text="Other input widgets", padding=10)
    # input_group.pack(fill=BOTH, pady=(10, 5), expand=YES)
    #
    # entry = Entry(input_group)
    # entry.pack(fill=X)
    # entry.insert(END, "entry widget")
    #
    # password = Entry(input_group, show="•")
    # password.pack(fill=X, pady=5)
    # password.insert(END, "password")
    #
    # spinbox = Spinbox(input_group, from_=0, to=100)
    # spinbox.pack(fill=X)
    # spinbox.set(45)
    #
    # cbo = Combobox(input_group, text=window.style.theme_current().name,
    #                values=theme_names, exportselection=False)
    # cbo.pack(fill=X, pady=5)
    # cbo.current(theme_names.index(window.style.theme_current().name))

    # de = ttk.DateEntry(input_group)
    # de.pack(fill=X)

    return root


if __name__ == "__main__":

    app = ttk.Window("ttkbootstrap widget demo", themename='cosmo')
    # print(font.names(app))
    bagel = setup_demo(app)
    bagel.pack(fill=BOTH, expand=YES)

    app.mainloop()
