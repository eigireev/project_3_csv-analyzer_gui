import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import csv
from collections import Counter
import statistics
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CSVAnalyzerGUI:
    def __init__(self, master):
        self.master = master
        master.title("CSV Analyzer")

        # Filename Label and Entry
        self.filename_label = ttk.Label(master, text="CSV Filename:")
        self.filename_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.filename_entry = ttk.Entry(master, width=30)
        self.filename_entry.grid(row=0, column=1, sticky=tk.E, padx=5, pady=5)

        # Browse Button
        self.browse_button = ttk.Button(master, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        # Filter Column Label and Entry
        self.filter_column_label = ttk.Label(master, text="Filter Column:")
        self.filter_column_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.filter_column_entry = ttk.Entry(master, width=30)
        self.filter_column_entry.grid(row=1, column=1, sticky=tk.E, padx=5, pady=5)

        # Filter Value Label and Entry
        self.filter_value_label = ttk.Label(master, text="Filter Value:")
        self.filter_value_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.filter_value_entry = ttk.Entry(master, width=30)
        self.filter_value_entry.grid(row=2, column=1, sticky=tk.E, padx=5, pady=5)

        # Sort Column Label and Entry
        self.sort_column_label = ttk.Label(master, text="Sort Column:")
        self.sort_column_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.sort_column_entry = ttk.Entry(master, width=30)
        self.sort_column_entry.grid(row=3, column=1, sticky=tk.E, padx=5, pady=5)

        # Date Column Label and Entry
        self.date_column_label = ttk.Label(master, text="Date Column:")
        self.date_column_label.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.date_column_entry = ttk.Entry(master, width=30)
        self.date_column_entry.grid(row=4, column=1, sticky=tk.E, padx=5, pady=5)

        # Analyze Button
        self.analyze_button = ttk.Button(master, text="Analyze CSV", command=self.analyze_csv)
        self.analyze_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Visualize Button
        self.visualize_button = ttk.Button(master, text="Visualize Data", command=self.visualize_data)
        self.visualize_button.grid(row=5, column=2, columnspan=1, pady=10)

        # Results Treeview
        self.results_label = ttk.Label(master, text="Results:")
        self.results_label.grid(row=8, column=0, sticky=tk.W, padx=5, pady=5)
        self.results_tree = ttk.Treeview(master, columns=("Column", "Average", "Minimum", "Maximum", "Median", "Mode", "Standard Deviation"), show="headings")
        self.results_tree.grid(row=9, column=0, columnspan=3, padx=5, pady=5, sticky=tk.NSEW)

        # Define Headings
        self.results_tree.heading("Column", text="Column")
        self.results_tree.heading("Average", text="Average")
        self.results_tree.heading("Minimum", text="Minimum")
        self.results_tree.heading("Maximum", text="Maximum")
        self.results_tree.heading("Median", text="Median")
        self.results_tree.heading("Mode", text="Mode")
        self.results_tree.heading("Standard Deviation", text="Standard Deviation")

        # Column widths
        self.results_tree.column("Column", width=100)
        self.results_tree.column("Average", width=100)
        self.results_tree.column("Minimum", width=100)
        self.results_tree.column("Maximum", width=100)
        self.results_tree.column("Median", width=100)
        self.results_tree.column("Mode", width=100)
        self.results_tree.column("Standard Deviation", width=100)

        # Column Selection Frame
        self.column_frame = ttk.Frame(master)
        self.column_frame.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)

        self.column_vars = {}
        self.column_checkboxes = []

        # Add scrollbars
        self.tree_scroll_y = ttk.Scrollbar(master, orient="vertical", command=self.results_tree.yview)
        self.tree_scroll_y.grid(row=9, column=3, sticky="ns")
        self.results_tree.configure(yscrollcommand=self.tree_scroll_y.set)

    def browse_file(self):
        filename = filedialog.askopenfilename(initialdir=".", title="Select a CSV file", filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))
        self.filename_entry.delete(0, tk.END)
        self.filename_entry.insert(0, filename)
        self.update_column_checkboxes(filename)

    def update_column_checkboxes(self, filename):
        # Clear existing checkboxes
        for checkbox in self.column_checkboxes:
            checkbox.destroy()
        self.column_vars = {}
        self.column_checkboxes = []

        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                header = next(reader)
                for i, column in enumerate(header):
                    self.column_vars[column] = tk.BooleanVar()
                    checkbox = tk.Checkbutton(self.column_frame, text=column, variable=self.column_vars[column])
                    checkbox.grid(row=0, column=i, padx=5, pady=5, sticky=tk.W)
                    self.column_checkboxes.append(checkbox)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return

    def analyze_csv(self):
        filename = self.filename_entry.get()
        filter_column = self.filter_column_entry.get()
        filter_value = self.filter_value_entry.get()
        sort_column = self.sort_column_entry.get()
        date_column = self.date_column_entry.get()

        # Clear previous results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        # CSV Analysis Logic (same as before, but output to results_text)
        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                header = next(reader)
                data = list(reader)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.\n")
            return

        # Filtering data
        if filter_column and filter_value:
            try:
                filter_index = header.index(filter_column)
                data = [row for row in data if row[filter_index] == filter_value]
            except ValueError:
                print(f"Error: Column '{filter_column}' not found.\n")
                return

        # Sorting data
        if sort_column:
            try:
                sort_index = header.index(sort_column)
                data.sort(key=lambda row: row[sort_index])
            except ValueError:
                print(f"Error: Column '{sort_column}' not found.\n")
                return

        # Determine numerical columns
        numerical_columns = []
        selected_columns = [column for column, var in self.column_vars.items() if var.get()]
        header_indices = [header.index(column) for column in selected_columns]

        for i in header_indices:
            try:
                float(data[0][i])
                numerical_columns.append(i)
            except ValueError:
                pass

        if not numerical_columns:
            print("No numerical columns found in the file.\n")
            return

        # Calculate statistics for numerical columns
        for i in numerical_columns:
            column_data = []
            for row in data:
                try:
                    value = float(row[i])
                    column_data.append(value)
                except ValueError:
                    print(f"Warning: Non-numerical value '{row[i]}' in column '{header[i]}', row skipped.\n")
                    continue

            if not column_data:
                print(f"Warning: Column '{header[i]}' contains no numerical data after error handling.\n")
                continue

            average = sum(column_data) / len(column_data)
            minimum = min(column_data)
            maximum = max(column_data)
            median = statistics.median(column_data)
            try:
                mode = statistics.mode(column_data)
            except statistics.StatisticsError:
                mode = "No mode"
            std_dev = statistics.stdev(column_data)

            self.results_tree.insert("", tk.END, values=(header[i], average, minimum, maximum, median, mode, std_dev))

        # Date handling (if date column is specified)
        if date_column:
            try:
                date_index = header.index(date_column)
                date_list = []
                for row in data:
                    date_str = row[date_index]
                    if date_str:  # Check if the date value is not empty
                        try:
                            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                            date_list.append(date_obj)
                        except ValueError:
                            print(f"Warning: Invalid date format '{date_str}' in row, row skipped.\n")
                            continue
                    else:
                        print(f"Warning: Missing date in row, row skipped.\n")
                        continue

                if date_list:
                    oldest_date = min(date_list)
                    newest_date = max(date_list)
                    print(f"Column '{date_column}': Oldest Date = {oldest_date}, Newest Date = {newest_date}\n")
                else:
                    print(f"Warning: No valid dates for analysis in column '{date_column}'.\n")

            except ValueError:
                print(f"Error: Invalid date format in column '{date_column}'. Expected format 'YYYY-MM-DD'.\n")
            except KeyError:
                print(f"Error: Column '{date_column}' not found.\n")

    def visualize_data(self):
        filename = self.filename_entry.get()
        selected_columns = [column for column, var in self.column_vars.items() if var.get()]

        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                header = next(reader)
                data = list(reader)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.\n")
            return

        # Create a new window for the plots
        plot_window = tk.Toplevel(self.master)
        plot_window.title("Data Visualization")

        for i, column in enumerate(selected_columns):
            try:
                column_index = header.index(column)
                column_data = [float(row[column_index]) for row in data]

                # Create a figure and an axes
                fig, ax = plt.subplots()
                ax.hist(column_data)
                ax.set_title(f'Histogram of {column}')
                ax.set_xlabel(column)
                ax.set_ylabel('Frequency')

                # Embed the figure in the Tkinter window
                canvas = FigureCanvasTkAgg(fig, master=plot_window)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.grid(row=i, column=0, padx=5, pady=5)

                canvas.draw()

            except ValueError:
                print(f"Warning: Column '{column}' contains non-numerical data and cannot be visualized.\n")
            except Exception as e:
                print(f"Error: Could not visualize column '{column}'. {e}\n")

root = tk.Tk()
gui = CSVAnalyzerGUI(root)
root.mainloop()