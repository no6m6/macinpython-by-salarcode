import sys
import os
import threading
import subprocess

ALLOWED_CHARS = set('0123456789.+-*/() ')

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
    GUI_AVAILABLE = True
except Exception:
    tk = None
    GUI_AVAILABLE = False

if GUI_AVAILABLE:
    class MacApp(tk.Toplevel):
        def __init__(self, master, title, width, height, bg='#c0c0c0'):
            super().__init__(master)
            self.title(title)
            self.geometry(f'{width}x{height}')
            self.configure(bg=bg)

    class TextEdit(MacApp):
        def __init__(self, master):
            super().__init__(master, 'MacWrite', 700, 500)
            self.text = tk.Text(self, bg='white', fg='black', font=('Monaco', 12))
            self.text.pack(fill='both', expand=True)
            frame = tk.Frame(self, bg='#d4d0c8')
            frame.pack(fill='x')
            tk.Button(frame, text='Open', bg='#d4d0c8', command=self.open_file).pack(side='left', padx=4, pady=4)
            tk.Button(frame, text='Save', bg='#d4d0c8', command=self.save_file).pack(side='left', padx=4, pady=4)

        def open_file(self):
            path = filedialog.askopenfilename(initialdir=os.path.expanduser('~'))
            if path:
                try:
                    with open(path, 'r', encoding='utf-8', errors='replace') as f:
                        self.text.delete('1.0', 'end')
                        self.text.insert('1.0', f.read())
                except Exception as e:
                    messagebox.showwarning('Error', f'Could not open file:\n{e}')

        def save_file(self):
            path = filedialog.asksaveasfilename(initialdir=os.path.expanduser('~'))
            if path:
                try:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(self.text.get('1.0', 'end'))
                    messagebox.showinfo('Saved', 'File saved successfully.')
                except Exception as e:
                    messagebox.showwarning('Error', f'Could not save file:\n{e}')

    class Calculator(MacApp):
        def __init__(self, master):
            super().__init__(master, 'Calculator', 320, 420)
            self.display = tk.Entry(self, justify='right', font=('Monaco', 16), bg='white', fg='black')
            self.display.pack(fill='x', padx=8, pady=8)
            btns = [['7','8','9','/'], ['4','5','6','*'], ['1','2','3','-'], ['0','.','=','+']]
            for row in btns:
                f = tk.Frame(self)
                f.pack(expand=True, fill='both')
                for ch in row:
                    tk.Button(f, text=ch, bg='#d4d0c8', command=lambda c=ch: self.on_button(c)).pack(side='left', expand=True, fill='both', padx=2, pady=2)

        def safe_eval(self, expr):
            expr = expr.strip()
            if not expr:
                return ''
            if any(ch not in ALLOWED_CHARS for ch in expr):
                raise ValueError('Invalid characters in expression')
            return str(eval(expr, {}, {}))

        def on_button(self, ch):
            if ch == '=':
                try:
                    self.display.delete(0, 'end')
                    self.display.insert(0, self.safe_eval(self.display.get()))
                except:
                    self.display.delete(0, 'end')
                    self.display.insert(0, 'Error')
            else:
                self.display.insert('end', ch)

    class MusicPlayer(MacApp):
        def __init__(self, master):
            super().__init__(master, 'MacPlayer', 400, 200)
            self.file_path = tk.StringVar()
            tk.Entry(self, textvariable=self.file_path, width=50, bg='white', fg='black').pack(padx=6, pady=6)
            tk.Button(self, text='Play', bg='#d4d0c8', command=self.play_music).pack(side='left', padx=6, pady=6)

        def play_music(self):
            path = self.file_path.get()
            if os.path.isfile(path):
                if sys.platform == 'win32':
                    threading.Thread(target=lambda: subprocess.call(['powershell', '-c', f'(New-Object Media.SoundPlayer "{path}").PlaySync();'])).start()
                else:
                    threading.Thread(target=lambda: subprocess.call(['afplay', path])).start()

    class PaintApp(MacApp):
        def __init__(self, master):
            super().__init__(master, 'MacPaint', 600, 400)
            self.canvas = tk.Canvas(self, bg='white', bd=2, relief='sunken')
            self.canvas.pack(fill='both', expand=True)
            self.canvas.bind('<B1-Motion>', self.paint)

        def paint(self, event):
            x1, y1 = (event.x-2), (event.y-2)
            x2, y2 = (event.x+2), (event.y+2)
            self.canvas.create_oval(x1, y1, x2, y2, fill='black', outline='black')

    class MacDesktop(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title('MacClassicOS Emulator')
            self.geometry('1024x720')
            self.configure(bg='#c0c0c0')
            self.icons_frame = tk.Frame(self, bg='#c0c0c0')
            self.icons_frame.pack(side='top', anchor='nw', padx=12, pady=12)
            apps = [
                ('MacWrite', lambda: TextEdit(self)),
                ('Calculator', lambda: Calculator(self)),
                ('MacPlayer', lambda: MusicPlayer(self)),
                ('MacPaint', lambda: PaintApp(self)),
            ]
            for i, (name, cb) in enumerate(apps):
                tk.Button(self.icons_frame, text=name, width=16, height=4, bg='#d4d0c8', command=cb).grid(row=i//4, column=i%4, padx=8, pady=8)

    if __name__ == '__main__':
        if GUI_AVAILABLE:
            app = MacDesktop()
            app.mainloop()
        else:
            print('GUI not available. Run on Windows/macOS/Linux with Tkinter installed.')
