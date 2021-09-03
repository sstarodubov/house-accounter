from tkinter import *
from tkinter import messagebox
from service import assets as ss
from common import constants as const
from model import asset as ma


class GraphicalInterface:
    def __init__(self, root: Tk, asset_sv: ss.AssetsSv):
        self.selected_asset_string: str = const.EMPTY_FIELD
        self.selected_asset: ma.Asset = ma.null_object
        self.master: Tk = root
        self._asset_sv: ss.AssetsSv = asset_sv
        root.title("House Assets: v0.0.1")

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

        # ASSET TYPE
        self.asset_type_update = StringVar()
        asset_label = Label(root, text='Asset Type:', font=('Ubuntu', 10))
        asset_label.grid(row=8, column=0, sticky=W, padx=(20, 0), pady=10)
        self.asset_type_update_entry = Entry(root, textvariable=self.asset_type_update)
        self.asset_type_update_entry.grid(row=8, column=0, pady=10)

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
        try:
            selected_idx = self.assets_list.curselection()[0]
            self.selected_asset_string = self.assets_list.get(selected_idx)
            incoming_asset, err = ma.parse_from_str(self.selected_asset_string)
            if err != const.EMPTY_FIELD:
                messagebox.showerror("Parse Error", err)
                return

            self.selected_asset = incoming_asset
            self.asset_val_entry.delete(0, END)
            self.asset_type_update_entry.delete(0, END)
            self.asset_type_update_entry.insert(0, incoming_asset.type)
            self.asset_val_entry.insert(0, incoming_asset.value)
        except IndexError:
            pass

    def update_asset(self) -> None:
        if self.selected_asset is ma.null_object:
            return
        cur_id: int = self.selected_asset.id
        cur_value: str = self.asset_val_update.get()
        cur_type = ma.build_asset_type_from_string(self.asset_type_update.get())
        if cur_type is ma.AssetTypes.UNKNOWN:
            messagebox.showerror("Unknown Assert Type", "Change assert type")
            return
        updated_asset = ma.Asset(cur_id, cur_type, cur_value)
        self._asset_sv.update(updated_asset)
        self.repopulate_assets()

    def repopulate_assets(self):
        self.assets_list.delete(0, END)
        assets = self._asset_sv.fetch_all()
        for a in assets:
            self.assets_list.insert(END, a)


_is_init = False


def run_gui():
    global _is_init
    if not _is_init:
        app = Tk()
        GraphicalInterface(app, ss.asset_sv_instance)
        _is_init = True
