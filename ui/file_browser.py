import tkinter as tk
from tkinter import filedialog
import logging

def browse_excel_file():
    try:
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Pilih file Excel",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        root.destroy()
        if not file_path:
            raise ValueError("Tidak ada file Excel yang dipilih!")
        return file_path
    except Exception as e:
        logging.error(f"‣ Error saat memilih file Excel: {str(e)}")
        print(f"‣ Error: Gagal memilih file Excel: {str(e)}")
        raise