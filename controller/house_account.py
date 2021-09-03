from tkinter import *
from tkinter import messagebox
from service import savings as ss
from common import constants as const
from model import saving as mod_sav


class GraphicalInterface:
    def __init__(self, root: Tk, savings_sv: ss.SavingsSv):
        self.selected_asset_string: str = const.EMPTY_FIELD
        self.selected_asset: mod_sav.Saving = mod_sav.null_object
        self.master: Tk = root
        self._savings_sv: ss.SavingsSv = savings_sv
        root.title("House Savings: v0.0.1")

        # HEADER
        asset_header = Label(root, text="Assets: ", font=("Ubuntu", 12))
        asset_header.grid(row=0, column=0, pady=10, sticky=W, padx=20)

        # ASSETS_LIST
        self.assets_list = Listbox(root, width=30, border=2)
        self.assets_list.configure(font=("Ubuntu", 13))
        self.assets_list.grid(row=1, column=0, pady=10, padx=(20, 0))
        scrollbar = Scrollbar(command=self.assets_list.yview)
        scrollbar.grid(row=1, column=1, sticky=W)
        self.assets_list.configure(yscrollcommand=scrollbar.set)
        self.assets_list.bind('<<ListboxSelect>>', self.peek_asset)

        # REFRESH BUTTON
        self.rfh_img = PhotoImage(file="assets/r.png")
        refresh_btn = Button(root, image=self.rfh_img, width=48, height=48, compound=CENTER)
        refresh_btn.grid(row=6, column=0)

        # EDIT
        edit_header = Label(root, text="Edit: ", font=("Ubuntu", 12))
        edit_header.grid(row=7, column=0, pady=10, sticky=W, padx=20)

        # ASSET NAME
        self.asset_name_update = StringVar()
        asset_label = Label(root, text='Asset Name:', font=('Ubuntu', 10))
        asset_label.grid(row=8, column=0, sticky=W, padx=(20, 0), pady=10)
        self.asset_name_update_entry = Entry(root, textvariable=self.asset_name_update)
        self.asset_name_update_entry.grid(row=8, column=0, pady=10)

        # ASSET VALUE
        self.asset_val_update = StringVar()
        asset_label = Label(root, text='Asset Value:', font=('Ubuntu', 10))
        asset_label.grid(row=9, column=0, sticky=W, padx=(20, 0), pady=(0, 20))
        self.asset_val_entry = Entry(root, textvariable=self.asset_val_update)
        self.asset_val_entry.grid(row=9, column=0, pady=(0, 20))

        # UPDATE BUTTON
        update_assets_btn = Button(root, text="update", command=self.update_asset)
        update_assets_btn.grid(row=8, column=0, padx=(300, 0), sticky=S)
        self.repopulate_assets()

        # RUN LOOP. it is last command in the method
        root.mainloop()

    def peek_asset(self, _) -> None:
        selected_idx = self.assets_list.curselection()[0]
        self.selected_asset_string = self.assets_list.get(selected_idx)
        saving, err = mod_sav.parse_from_str(self.selected_asset_string)
        if err != const.EMPTY_FIELD:
            messagebox.showerror("Parse Error", err)
            return
        self.selected_asset = saving
        self.asset_val_entry.delete(0, END)
        self.asset_name_update_entry.delete(0, END)
        self.asset_name_update_entry.insert(0, saving.name)
        self.asset_val_entry.insert(0, saving.value)

    def update_asset(self) -> None:
        if self.selected_asset is mod_sav.null_object:
            return
        cur_id: int = self.selected_asset.id
        cur_value: str = self.asset_val_update.get()
        cur_name: str = self.asset_name_update.get()

        updated_asset = mod_sav.Saving(cur_id, cur_name, cur_value)
        self._savings_sv.update(updated_asset)
        self.repopulate_assets()

    def repopulate_assets(self):
        self.assets_list.delete(0, END)
        savings = self._savings_sv.fetch_all()
        for s in savings:
            self.assets_list.insert(END, s)


_is_init = False


def run_gui():
    global _is_init
    if not _is_init:
        app = Tk()
        GraphicalInterface(app, ss.savings_sv_instance)
        _is_init = True
