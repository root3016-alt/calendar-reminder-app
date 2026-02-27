import tkinter as tk
from splash import SplashScreen
from app import App

def main():
    # Show splash screen first
    splash_root = tk.Tk()
    splash = SplashScreen(splash_root)
    splash_root.mainloop()

    # Then launch main app
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()