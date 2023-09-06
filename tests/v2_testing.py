import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widget import *

#app = ttk.Window(themename='cosmo', hdpi=False)
#app = ttk.Window(themename='cosmo')
app = ttk.Window(themename='superhero')
"""
    Slow Styles:
    - Notebook
    - Progressbar

    Problem styles:
    - Panedwindow (handle is to small, can't drag, need hover style)

"""

# frame = Frame()
# frame.pack(expand=YES, anchor='nw', fill='both')
#
# # nb = Notebook(frame, width=300, height=300)
# # nb.add(Frame(nb, width=300, height=300), text='Tab 1')
# # nb.pack(padx=20, pady=20)
# #
# # pb = Progressbar(frame, value=75, length=300)
# # pb.pack(padx=20, pady=20)
#
# lf = Labelframe(frame, text="Widgets", padding=50)
# lf.pack(anchor='nw', padx=20, pady=20, fill='x')
#
# for x in range(20):
#     cb = Checkbutton(text="Option 1")
#     cb.pack(fill=X, padx=10, pady=10)
#
# for x in range(20):
#     Button(text=f'Button {x}').pack(fill=X, padx=20, pady=20)
#     #Button(text='Outline', bootstyle='outline-button').pack(fill=X, padx=20, pady=20)


# for _ in range(30):
#     sb = Scrollbar(orient='h')
#     sb.pack(fill=X, expand=True, padx=20, pady=20)
#     sb.set(0.1, 0.9)

# for _ in range(30):
#     sb = Scrollbar()
#     sb.pack(side=LEFT, fill=Y, expand=True, padx=20, pady=20)
#     sb.set(0.1, 0.9)

for x in range(5):
    Entry().pack(fill=X, padx=20, pady=20)

# for x in range(20):
#     Separator(bootstyle='danger').pack(fill=X, padx=20, pady=20)

# for x in range(20):
#     Separator(bootstyle='danger', orient='v').pack(side=LEFT, fill=Y, padx=20, pady=20)

# for x in range(40):
#     Checkbutton(text=f'Button {x}').pack()
#
# for _ in range(10):
#     Menubutton(text='Button', bootstyle='outline-menubutton').pack(padx=20, pady=10)
#     Button(text='Button', bootstyle='outline-button').pack(padx=20, pady=10)

# for x in range(10):
#     s = Checkbutton(text=f'My Switch {x}')
#     s.pack(fill=X, pady=10)

#
# for _ in range(5):
#     Spinbox(values='israel judy abigail katelyn').pack(fill=X, expand=True, padx=20, pady=10)

# Label(text="Hello world", font="TkDisplay").pack()
# cbo = Combobox(values='israel judy abigail katelyn')
# cbo.pack(fill=X, expand=True, padx=20, pady=10)





# from tkinter import ttk
# import tkinter as tk
#
# app = tk.Tk()
# style = ttk.Style()
# style.theme_use('clam')
#
# for x in range(20):
#     ttk.Button(text=f'Button #{x}').pack(padx=2, pady=2)
#
if __name__ == '__main__':
    app.mainloop()