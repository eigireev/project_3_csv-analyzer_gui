import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import csv
from collections import Counter
import statistics
from datetime import datetime

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

        # Results Text Area
        self.results_label = ttk.Label(master, text="Results:")
        self.results_label.grid(row=8, column=0, sticky=tk.W, padx=5, pady=5)
        self.results_text = tk.Text(master, height=10, width=50)
        self.results_text.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

        # Column Selection Frame
        self.column_frame = ttk.Frame(master)
        self.column_frame.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)

        self.column_vars = {}
        self.column_checkboxes = []

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
            self.results_text.insert(tk.END, f"Error: File '{filename}' not found.\n")
            return

    def analyze_csv(self):
        filename = self.filename_entry.get()
        filter_column = self.filter_column_entry.get()
        filter_value = self.filter_value_entry.get()
        sort_column = self.sort_column_entry.get()
        date_column = self.date_column_entry.get()

        # CSV Analysis Logic (same as before, but output to results_text)
        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                header = next(reader)
                data = list(reader)
        except FileNotFoundError:
            self.results_text.insert(tk.END, f"Error: File '{filename}' not found.\n")
            return

        # Filtering data
        if filter_column and filter_value:
            try:
                filter_index = header.index(filter_column)
                data = [row for row in data if row[filter_index] == filter_value]
            except ValueError:
                self.results_text.insert(tk.END, f"Error: Column '{filter_column}' not found.\n")
                return

        # Sorting data
        if sort_column:
            try:
                sort_index = header.index(sort_column)
                data.sort(key=lambda row: row[sort_index])
            except ValueError:
                self.results_text.insert(tk.END, f"Error: Column '{sort_column}' not found.\n")
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
            self.results_text.insert(tk.END, "No numerical columns found in the file.\n")
            return

        # Calculate statistics for numerical columns
        for i in numerical_columns:
            column_data = []
            for row in data:
                try:
                    value = float(row[i])
                    column_data.append(value)
                except ValueError:
                    self.results_text.insert(tk.END, f"Warning: Non-numerical value '{row[i]}' in column '{header[i]}', row skipped.\n")
                    continue

            if not column_data:
                self.results_text.insert(tk.END, f"Warning: Column '{header[i]}' contains no numerical data after error handling.\n")
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

            self.results_text.insert(tk.END, f"Column '{header[i]}': Average = {average}, Minimum = {minimum}, Maximum = {maximum}, Median = {median}, Mode = {mode}, Standard Deviation = {std_dev}\n")

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
                            self.results_text.insert(tk.END, f"Warning: Invalid date format '{date_str}' in row, row skipped.\n")
                            continue
                    else:
                        self.results_text.insert(tk.END, f"Warning: Missing date in row, row skipped.\n")
                        continue

                if date_list:
                    oldest_date = min(date_list)
                    newest_date = max(date_list)
                    self.results_text.insert(tk.END, f"Column '{date_column}': Oldest Date = {oldest_date}, Newest Date = {newest_date}\n")
                else:
                    self.results_text.insert(tk.END, f"Warning: No valid dates for analysis in column '{date_column}'.\n")

            except ValueError:
                self.results_text.insert(tk.END, f"Error: Invalid date format in column '{date_column}'. Expected format 'YYYY-MM-DD'.\n")
            except KeyError:
                self.results_text.insert(tk.END, f"Error: Column '{date_column}' not found.\n")

root = tk.Tk()
gui = CSVAnalyzerGUI(root)
root.mainloop()