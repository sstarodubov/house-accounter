from tkinter import *


class GraphicalInterface:
    def __init__(self, root: Tk):
        self.master = root
        root.title("House Savings: v0.0.1")

        # HEADER
        asset_header = Label(root, text="Assets: ", font=("Ubuntu", 12))
        asset_header.grid(row=0, column=0, pady=10, sticky=W, padx=20)

        # ASSETS
        assets_box = Listbox(root, width=50, border=2)
        assets_box.grid(row=1, column=0, pady=10, padx=(20, 0))
        scrollbar = Scrollbar(command=assets_box.yview)
        scrollbar.grid(row=1, column=1, sticky=W)
        assets_box.configure(yscrollcommand=scrollbar.set)

        # REFRESH BUTTON
        self.rfh_img = PhotoImage(file="assets/r.png")
        refresh_btn = Button(root, image=self.rfh_img, width=48, height=48, compound=CENTER)
        refresh_btn.grid(row=6, column=0)

        # EDIT
        edit_header = Label(root, text="Edit: ", font=("Ubuntu", 12))
        edit_header.grid(row=7, column=0, pady=10, sticky=W, padx=20)

        # ASSET NAME
        asset_update_input = StringVar()
        asset_label = Label(root, text='Asset Name:', font=('Ubuntu', 10))
        asset_label.grid(row=8, column=0, sticky=W, padx=(20, 0), pady=10)
        asset_entry = Entry(root, textvariable=asset_update_input)
        asset_entry.grid(row=8, column=0, pady=10)

        # ASSET VALUE
        asset_update_input = StringVar()
        asset_label = Label(root, text='Asset Value:', font=('Ubuntu', 10))
        asset_label.grid(row=9, column=0, sticky=W, padx=(20, 0), pady=(0, 20))
        asset_entry = Entry(root, textvariable=asset_update_input)
        asset_entry.grid(row=9, column=0, pady=(0, 20))

        # UPDATE BUTTON
        update_assets_btn = Button(root, text="update")
        update_assets_btn.grid(row=8, column=0, padx=(300, 0), sticky=S)
        root.mainloop()


_is_init = False


def run_gui():
    global _is_init
    if not _is_init:
        app = Tk()
        GraphicalInterface(app)
        _is_init = True
