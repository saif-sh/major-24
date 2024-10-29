# main.py

import tkinter as tk
from gui import SpeechEmotionApp

def main():
    root = tk.Tk()
    app = SpeechEmotionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
