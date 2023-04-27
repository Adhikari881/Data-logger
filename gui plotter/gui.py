import tkinter as tk
from tkinter import ttk
import threading
import time
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class RealTimeGraph(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Real-Time Graph")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.pack()

        # Variables
        self.is_running = False
        self.is_paused = False
        self.x_data = []
        self.y_data = []
        self.pause_index = 0

        # GUI Elements
        self.start_button = ttk.Button(self, text="Start", command=self.start)
        self.start_button.pack(side="bottom")
        self.pause_button = ttk.Button(self, text="Pause", command=self.pause)
        self.pause_button.pack(side="bottom")
        self.stop_button = ttk.Button(self, text="Stop", command=self.stop)
        self.stop_button.pack(side="bottom")

        # Graph
        self.fig, self.ax = plt.subplots()
        self.graph, = self.ax.plot(self.x_data, self.y_data)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self.update_graph)
            self.thread.start()

    def pause(self):
        if self.is_running:
            self.is_paused = not self.is_paused
            if self.is_paused:
                self.pause_button.config(text="Resume")
            else:
                self.pause_button.config(text="Pause")

    def stop(self):
        if self.is_running:
            self.is_running = False

    def update_graph(self):
        while self.is_running:
            if not self.is_paused:
                # Generate random data
                x = time.time()
                y = random.randint(0, 100)

                # Update data
                self.x_data.append(x)
                self.y_data.append(y)

                # Remove old data if necessary
                if len(self.x_data) > 100:
                    self.x_data.pop(0)
                    self.y_data.pop(0)

                # Update pause index
                if self.is_paused:
                    self.pause_index = len(self.x_data) - 1

                # Update graph
                self.graph.set_data(self.x_data[self.pause_index:], self.y_data[self.pause_index:])
                self.ax.relim()
                self.ax.autoscale_view()

                # Redraw canvas
                self.canvas.draw()

            # Wait 0.1 seconds
            time.sleep(0.1)

    def on_closing(self):
        self.stop()
        self.master.destroy()


class MyApp:
    def __init__(self):
        self.root = tk.Tk()
        self.app = RealTimeGraph(master=self.root)
        self.app.mainloop()


# if __name__ == "__main__":
#     my_app = MyApp()
