import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
from datetime import datetime
from tkinter import filedialog


class LinkDataPlotter:
    def __init__(self, root):
        """
        Initialize the LinkDataPlotter class.
        Creates the main application window and sets up UI elements.
        """
        self.root = root
        self.root.title("Plot Gui")
        self.root.geometry('+500+200')
        self.data = {}
        self.file_selected = False

        # Create the UI elements
        self.create_widgets()

    def create_widgets(self):
        """
        Create and pack the UI elements such as buttons and frames.
        """

        # Create a frame for file selection
        file_frame = ttk.Frame(self.root)
        file_frame.pack(pady=10)

        # File selection button
        file_button = ttk.Button(file_frame, text='Select File', command=self.load_file)
        file_button.pack()

        # Create a frame for range label to see max range
        self.range_label_frame = ttk.Frame(self.root)
        self.range_label_frame.pack(pady=10)

        # Create a frame for checkbox
        self.checkbox_frame = ttk.Frame(self.root)
        self.checkbox_frame.pack(pady=10)

        # Create a frame for range enter
        range_frame = ttk.Frame(self.root)
        range_frame.pack(pady=10)

        ttk.Label(range_frame, text='X-axis end:').pack(side=tk.LEFT)
        self.x_end = tk.Entry(range_frame, width=10)
        self.x_end.pack(side=tk.LEFT, padx=5)

        # Button to generate the plot
        plot_button = ttk.Button(self.root, text='Plot', command=self.plot_links)
        plot_button.pack(pady=10)

        # Create a frame for y-axis label entry
        y_label_frame = ttk.Frame(self.root)
        y_label_frame.pack(pady=10)

        ttk.Label(y_label_frame, text='Y-axis Label:').pack(side=tk.LEFT)
        self.y_label_entry = tk.Entry(y_label_frame, width=20)
        self.y_label_entry.pack(side=tk.LEFT, padx=5)

        # Frame to hold plot
        self.plot_frame = ttk.Frame(self.root)
        self.plot_frame.pack(fill=tk.BOTH, expand=True)

    def load_file(self):
        """
        Load data from a selected CSV file.
        This function opens a file dialog to select a CSV file and reads its contents.
        """
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.data = {}
            self.file_selected = True

            # Open and read the CSV file
            with open(file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                for row in reader:
                    for key, value in row.items():
                        if key not in self.data:
                            self.data[key] = []
                        self.data[key].append(value)

            # Create checkboxes for th data columns
            self.create_checkboxes()

    def create_checkboxes(self):
        """
        Create checkboxes for each data column in the CSV file.
        """

        # clear existing checkboxes
        for widget in self.checkbox_frame.winfo_children():
            widget.destroy()

        # Checkboxes for selecting links
        self.check_vars = {}
        for key in self.data.keys():
            if key != 'czas' and key != 'time' and key != 'Time':
                self.check_vars[key] = tk.BooleanVar()
                checkbox = ttk.Checkbutton(self.checkbox_frame, text=key, variable=self.check_vars[key])
                checkbox.pack(anchor=tk.NW, padx=5)

        # Set label for range
        range_label = ttk.Label(self.range_label_frame, text=f'max range: {len(self.data[next(iter(self.data))]) - 1}')
        range_label.pack(side=tk.LEFT)

    def plot_links(self):
        """
        Plot the selected data columns.
        This function creates a plot based on the selected checkboxes.
        """

        # Check if file is selected if not get warning
        if not self.file_selected:
            messagebox.showwarning(title='Warning', message='Please select a CSV file')
            return

        # Check the range of x
        zakres = len(self.data[next(iter(self.data))]) - 1
        try:
            x_end = int(self.x_end.get())
        except ValueError:
            messagebox.showerror("Invalid input", f"Please select correct value range from 0 to : {zakres}")
            return

        if x_end < 0 or x_end > zakres:
            messagebox.showerror("Invalid input", f"Please select correct value range from 0 to : {zakres}")
            return

        # Retrieve the y-axis label from the entry
        y_axis_label = self.y_label_entry.get().strip()
        if not y_axis_label:
            y_axis_label = 'Value'

        # Set the figure size
        plt.figure(figsize=(10, 5))

        # Generate x-values as line numbers (0, 1, 2, ...)
        x_start = 0
        x_values = list(range(x_start, x_end + 1))

        for key, var in self.check_vars.items():
            if var.get():
                y_values = list(map(float, self.data[key][x_start:x_end + 1]))
                plt.plot(x_values, y_values, label=key)

        # Set plot labels and title
        plt.xlabel('Time, s')
        plt.ylabel(y_axis_label)
        plt.title('Link Data')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)

        # Clear previous plot
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Display new plot
        canvas = FigureCanvasTkAgg(plt.gcf(), master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = LinkDataPlotter(root)
    root.mainloop()






