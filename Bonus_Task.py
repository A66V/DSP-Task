import numpy as np
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


F = 5
fs = 80
def ConstructSignal(AMP, PhASESHEFTING):
    V = np.empty(0)
    I = np.arange(0, 100, 1) / fs
    Angualr_frequency =(2 * np.pi * (F / fs))
    for i in range(100):
        V = np.append(V, AMP * np.sin(Angualr_frequency* i))
    return V, I





def correlate(s1, s2):
     index = []
     val = []
     
     for i in range(len(s1)):
         index.append(i)
         ans = 0
         
         #for j in range(len(self.expected_samples)):
             #ans += (self.expected_samples[j] * s.expected_samples[j])
         val.append((s1 * s2).sum() / len(s1))
         tmp = s2[0]
         s2 = s2[1:]
         s2 = np.append(s2, tmp)
     sum1 = (s1 * s2).sum()
     sum2 = (s1 * s2).sum()
     #for i in range(len(self.expected_samples)):
         #sum1 += self.expected_samples[i]**2
         #sum2 += s.expected_samples[i]**2
     
     norm = 1/len(s1) * ((sum1 * sum2) ** 0.5)
     return val / norm


def generate_and_plot():
    global canvas_frame  # To reference the scrollable frame

    sine, T = ConstructSignal(2, 0)
    T = np.arange(0, 100) / fs
    awgn_signal = np.random.normal(0, 5, 100)
    noise_signal = sine + awgn_signal

    auto_corr_sine = correlate(sine, sine)
    auto_corr_noisy = correlate(noise_signal, noise_signal)


    for widget in canvas_frame.winfo_children():
        widget.destroy()


    fig1 = Figure(figsize=(10, 4), dpi=100)
    ax1 = fig1.add_subplot(111)
    ax1.plot(T, sine, label="Sine Wave", color='blue')
    ax1.set_title("Sine Wave")
    ax1.grid(True)
    ax1.legend()

    fig2 = Figure(figsize=(10, 4), dpi=100)
    ax2 = fig2.add_subplot(111)
    ax2.plot(T, awgn_signal, label="AWGN Signal", color='orange')
    ax2.set_title("Additive White Gaussian Noise")
    ax2.grid(True)
    ax2.legend()

    fig3 = Figure(figsize=(10, 4), dpi=100)
    ax3 = fig3.add_subplot(111)
    ax3.plot(T, noise_signal, label="Corrupted Signal (Sine + Noise)", color='green')
    ax3.set_title("Corrupted Signal")
    ax3.grid(True)
    ax3.legend()

    fig4 = Figure(figsize=(10, 4), dpi=100)
    ax4 = fig4.add_subplot(111)
    ax4.plot(auto_corr_sine, label="Auto-correlation of Sine Wave", color='blue')
    ax4.set_title("Auto-correlation of Sine Wave")
    ax4.grid(True)
    ax4.legend()

    fig5 = Figure(figsize=(10, 4), dpi=100)
    ax5 = fig5.add_subplot(111)
    ax5.plot(auto_corr_noisy, label="Auto-correlation of Corrupted Signal", color='green')
    ax5.set_title("Auto-correlation of Corrupted Signal")
    ax5.grid(True)
    ax5.legend()

    # Embed figures in Tkinter
    for fig in [fig1, fig2, fig3, fig4, fig5]:
        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Main Application
root = tk.Tk()
root.title("Scrollable Signal Processing Graphs")
root.geometry("1200x800")

# Scrollable canvas setup
scroll_canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=scroll_canvas.yview)
scrollable_frame = ttk.Frame(scroll_canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
)

scroll_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
scroll_canvas.configure(yscrollcommand=scrollbar.set)

# Pack canvas and scrollbar
scroll_canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Frame for plots
canvas_frame = ttk.Frame(scrollable_frame)
canvas_frame.pack(fill=tk.BOTH, expand=True)


generate_button = tk.Button(root, text="Generate Plots", command=generate_and_plot)
generate_button.pack(side=tk.BOTTOM, pady=10)

root.mainloop()