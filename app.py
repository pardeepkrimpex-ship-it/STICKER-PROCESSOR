import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import pandas as pd, re

SPECIAL = ["JATAMANSI ROOT","RATANJOT ROOT","SUGAR BADAM","ROSEMARY","PANEER DODI","DUNAL SEEDS"]

def find_col(cols, terms):
    for c in cols:
        if any(t in str(c).lower().strip() for t in terms):
            return c
    raise ValueError("Required column missing. Found columns: " + ", ".join(map(str, cols)))

def clean_title(s):
    s = str(s)
    for b in ["SAI HERBS","YOGIMATE","MIBITES"]:
        s = re.sub(re.escape(b), "", s, flags=re.I)
    return re.split(r"[-|/]", s.strip(), maxsplit=1)[0].strip()

def get_weight(s):
    m = re.search(r"(\\d+(?:\\.\\d+)?)\\s*(KG|KGS|GRAMS?|GR|GMS?|GM)\\b", str(s), re.I)
    if not m: return None
    n, unit = float(m.group(1)), m.group(2).upper()
    if unit in ("KG","KGS"): n *= 1000
    return int(n)

def process(src, dest):
    try: df = pd.read_csv(src, low_memory=False, encoding="utf-8-sig")
    except UnicodeDecodeError: df = pd.read_csv(src, low_memory=False, encoding="latin1")
    df.columns = df.columns.astype(str).str.strip()
    tc = find_col(df.columns, ["title","product","name"])
    qc = find_col(df.columns, ["qty","quantity","unit"])
    pc = find_col(df.columns, ["price"])
    result = []
    for i, r in df.iterrows():
        title = clean_title(r[tc]); weight = get_weight(r[tc])
        try:
            qty = int(float(str(r[qc]).replace(",","")))
            price = float(str(r[pc]).replace(",",""))
        except Exception:
            raise ValueError(f"Invalid quantity/price at CSV row {i+2}")
        if qty < 0: raise ValueError(f"Negative quantity at CSV row {i+2}")
        for _ in range(qty):
            if weight == 1000 and "RAW" in title.upper() and any(x in title.upper() for x in SPECIAL):
                weights = [250]*4
            elif weight == 1000:
                weights = [500,500]
            else:
                weights = [weight]
            for w in weights:
                result.append({"Title":title, "Weight":f"{w} GMS" if w is not None else "", "Price":f"{int(price*2)}.00"})
    pd.DataFrame(result, columns=["Title","Weight","Price"]).to_excel(dest, index=False)

class App:
    def __init__(self, root):
        self.root=root; self.src=None
        root.title("Herb CSV Processor"); root.geometry("520x280"); root.resizable(False,False)
        tk.Label(root,text="HERB CSV PROCESSOR",font=("Arial",18,"bold")).pack(pady=(25,8))
        tk.Label(root,text="CSV upload karo aur processed Excel banao").pack()
        self.file_label=tk.Label(root,text="No file selected",wraplength=460,fg="gray"); self.file_label.pack(pady=18)
        tk.Button(root,text="SELECT CSV FILE",width=25,height=2,command=self.choose).pack(pady=5)
        tk.Button(root,text="PROCESS & SAVE EXCEL",width=25,height=2,bg="#1769aa",fg="white",command=self.run).pack(pady=5)
        self.status=tk.Label(root,text="Ready",fg="green"); self.status.pack(pady=12)
    def choose(self):
        self.src=filedialog.askopenfilename(filetypes=[("CSV files","*.csv")])
        if self.src: self.file_label.config(text=Path(self.src).name); self.status.config(text="CSV selected")
    def run(self):
        if not self.src: messagebox.showwarning("Select file","Pehle CSV select karo."); return
        dest=filedialog.asksaveasfilename(defaultextension=".xlsx",initialfile=Path(self.src).stem+"_PROCESSED.xlsx",filetypes=[("Excel files","*.xlsx")])
        if not dest: return
        try:
            process(self.src,dest); self.status.config(text="Complete!",fg="green"); messagebox.showinfo("Success","Processed Excel save ho gayi.")
        except Exception as e:
            self.status.config(text="Error",fg="red"); messagebox.showerror("Error",str(e))

if __name__ == "__main__":
    win=tk.Tk(); App(win); win.mainloop()
