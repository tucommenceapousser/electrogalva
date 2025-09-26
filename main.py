import tkinter as tk
from tkinter import ttk, messagebox
import math
import threading
import time

# Facteurs matériaux
FACTEURS_MATERIAUX = {
    "alu": 1.0,
    "acier": 1.2,
    "laiton": 1.1,
    "argent": 0.9,
    "cuivre": 1.0
}
TEMPS_FACTEUR = {"rapide": 1.0, "fin": 1.5}
TEMPS_BASE_MINUTES = 60.0

class TrHacknonGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("trhacknon - Electroplating Calculator")
        self.geometry("900x640")
        self.configure(bg='#0b0f12')
        self._timer_thread = None
        self._timer_running = False
        self._remaining_seconds = 0
        self._timer_total_seconds = 0
        self._build_ui()

    def _build_ui(self):
        # Inputs
        ttk.Label(self, text="Surface (cm²):", foreground='#7cffb2', background='#0b0f12').place(x=20, y=20)
        self.surface_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.surface_var).place(x=150, y=20)

        ttk.Label(self, text="Rendu (rapide/fin):", foreground='#7cffb2', background='#0b0f12').place(x=20, y=60)
        self.mode_var = tk.StringVar(value='rapide')
        ttk.Combobox(self, textvariable=self.mode_var, values=['rapide','fin']).place(x=150, y=60)

        ttk.Label(self, text="Matériau:", foreground='#7cffb2', background='#0b0f12').place(x=20, y=100)
        self.materiau_var = tk.StringVar(value='cuivre')
        ttk.Combobox(self, textvariable=self.materiau_var, values=list(FACTEURS_MATERIAUX.keys())).place(x=150, y=100)

        ttk.Label(self, text="Intensité dispo (A):", foreground='#7cffb2', background='#0b0f12').place(x=20, y=140)
        self.intensite_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.intensite_var).place(x=150, y=140)

        ttk.Button(self, text="Calculer", command=self.calculer).place(x=20, y=180)

        # Results
        self.result_text = tk.Text(self, width=80, height=20, bg='#041014', fg='#dfffe0')
        self.result_text.place(x=20, y=220)

        # Timer display
        ttk.Label(self, text="Minuterie:", foreground='#7cffb2', background='#0b0f12').place(x=600, y=20)
        self.timer_label = ttk.Label(self, text="00:00:00", font=('Consolas', 18), foreground='#7cffb2', background='#0b0f12')
        self.timer_label.place(x=600, y=60)
        self.progress = ttk.Progressbar(self, length=250, mode='determinate')
        self.progress.place(x=600, y=120)
        ttk.Button(self, text="Démarrer", command=self._start_timer).place(x=600, y=160)
        ttk.Button(self, text="Pause", command=self._pause_timer).place(x=680, y=160)
        ttk.Button(self, text="Reset", command=self._reset_timer).place(x=740, y=160)

    def calculer(self):
        try:
            surface = float(self.surface_var.get())
            mode = self.mode_var.get()
            materiau = self.materiau_var.get()
            intensite_user = float(self.intensite_var.get())
            facteur = FACTEURS_MATERIAUX.get(materiau, 1.0)

            if mode == 'rapide':
                imin = 0.05*surface*facteur
                imax = 0.15*surface*facteur
            else:
                imin = 0.05*surface*facteur
                imax = 0.10*surface*facteur

            imoy = (imin+imax)/2
            temps = (imoy/intensite_user)*TEMPS_BASE_MINUTES*TEMPS_FACTEUR[mode]

            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, f"Intensité recommandée: {imin:.2f} - {imax:.2f} A\n")
            self.result_text.insert(tk.END, f"Intensité moyenne: {imoy:.2f} A\n")
            self.result_text.insert(tk.END, f"Temps estimé avec ton intensité ({intensite_user:.2f} A): {temps:.1f} min\n")

            # Initialize timer
            self._remaining_seconds = int(temps*60)
            self._timer_total_seconds = self._remaining_seconds
            self._update_timer_display()

        except Exception as e:
            messagebox.showerror("Erreur", f"Vérifie les valeurs saisies.\n{str(e)}")

    def _update_timer_display(self):
        h = self._remaining_seconds // 3600
        m = (self._remaining_seconds % 3600) // 60
        s = self._remaining_seconds % 60
        self.timer_label.config(text=f"{h:02d}:{m:02d}:{s:02d}")
        if self._timer_total_seconds > 0:
            percent = (1 - self._remaining_seconds/self._timer_total_seconds)*100
            self.progress['value'] = percent
        else:
            self.progress['value'] = 0

    def _timer_worker(self):
        while self._timer_running and self._remaining_seconds > 0:
            time.sleep(1)
            if not self._timer_running:
                break
            self._remaining_seconds -= 1
            self._update_timer_display()
        if self._remaining_seconds <= 0:
            self._timer_running = False
            messagebox.showinfo('Terminé', "Le traitement est terminé !")

    def _start_timer(self):
        if self._remaining_seconds <= 0:
            messagebox.showwarning('Minuterie vide', "Calcule le temps avant de démarrer.")
            return
        if not self._timer_running:
            self._timer_running = True
            threading.Thread(target=self._timer_worker, daemon=True).start()

    def _pause_timer(self):
        self._timer_running = False

    def _reset_timer(self):
        self._timer_running = False
        self._remaining_seconds = self._timer_total_seconds
        self._update_timer_display()

if __name__ == '__main__':
    app = TrHacknonGUI()
    app.mainloop()
