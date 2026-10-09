# ---------------------------------------------------------
# Assignment 1 - Q10
# Tkinter Assignment Tracker with File Persistence
# ---------------------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
import os


DATA_FILE = "assignments.json"


class AssignmentTracker:

    def __init__(self, root):

        self.root = root
        self.root.title("Assignment Tracker")
        self.root.geometry("900x600")

        # Load saved data
        self.records = self.load_data()

        self.create_widgets()

        self.refresh_table()

    # -----------------------------------------------------
    # File handling
    # -----------------------------------------------------

    def load_data(self):
        """Load records from JSON file."""

        if not os.path.exists(DATA_FILE):
            return []

        try:

            with open(
                DATA_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except (json.JSONDecodeError, OSError):

            return []

    def save_data(self):
        """Save records to JSON."""

        with open(
            DATA_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.records,
                file,
                indent=4
            )

    # -----------------------------------------------------
    # GUI
    # -----------------------------------------------------

    def create_widgets(self):

        # Title
        title = tk.Label(
            self.root,
            text="Student Assignment Tracker",
            font=("Arial", 18, "bold")
        )

        title.pack(pady=10)

        # Input frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=5)

        # Enrollment
        tk.Label(
            input_frame,
            text="Enrollment:"
        ).grid(row=0, column=0, padx=5)

        self.enrollment_entry = tk.Entry(
            input_frame
        )

        self.enrollment_entry.grid(
            row=0,
            column=1,
            padx=5
        )

        # Name
        tk.Label(
            input_frame,
            text="Name:"
        ).grid(row=0, column=2, padx=5)

        self.name_entry = tk.Entry(
            input_frame
        )

        self.name_entry.grid(
            row=0,
            column=3,
            padx=5
        )

        # Assignment
        tk.Label(
            input_frame,
            text="Assignment:"
        ).grid(row=1, column=0, padx=5)

        self.assignment_entry = tk.Entry(
            input_frame
        )

        self.assignment_entry.grid(
            row=1,
            column=1,
            padx=5
        )

        # Status
        tk.Label(
            input_frame,
            text="Status:"
        ).grid(row=1, column=2, padx=5)

        self.status_combo = ttk.Combobox(
            input_frame,
            values=["Pending", "Completed"],
            state="readonly"
        )

        self.status_combo.set("Pending")

        self.status_combo.grid(
            row=1,
            column=3,
            padx=5
        )

        # Marks
        tk.Label(
            input_frame,
            text="Marks:"
        ).grid(row=2, column=0, padx=5)

        self.marks_entry = tk.Entry(
            input_frame
        )

        self.marks_entry.grid(
            row=2,
            column=1,
            padx=5
        )

        # Remarks
        tk.Label(
            input_frame,
            text="Remarks:"
        ).grid(row=2, column=2, padx=5)

        self.remarks_entry = tk.Entry(
            input_frame
        )

        self.remarks_entry.grid(
            row=2,
            column=3,
            padx=5
        )

        # -------------------------------------------------
        # Buttons
        # -------------------------------------------------

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Add Submission",
            command=self.add_submission
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="Update Marks",
            command=self.update_marks
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="Export CSV",
            command=self.export_csv
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_fields
        ).grid(row=0, column=3, padx=5)

        # -------------------------------------------------
        # Filter
        # -------------------------------------------------

        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=5)

        tk.Label(
            filter_frame,
            text="Filter:"
        ).pack(side=tk.LEFT)

        self.filter_combo = ttk.Combobox(
            filter_frame,
            values=[
                "All",
                "Pending",
                "Completed"
            ],
            state="readonly"
        )

        self.filter_combo.set("All")

        self.filter_combo.pack(
            side=tk.LEFT,
            padx=5
        )

        self.filter_combo.bind(
            "<<ComboboxSelected>>",
            lambda event: self.refresh_table()
        )

        # -------------------------------------------------
        # Table
        # -------------------------------------------------

        columns = (
            "enrollment",
            "name",
            "assignment",
            "status",
            "marks",
            "remarks"
        )

        self.table = ttk.Treeview(
            self.root,
            columns=columns,
            show="headings"
        )

        headings = {
            "enrollment": "Enrollment",
            "name": "Name",
            "assignment": "Assignment",
            "status": "Status",
            "marks": "Marks",
            "remarks": "Remarks"
        }

        for column in columns:

            self.table.heading(
                column,
                text=headings[column]
            )

            self.table.column(
                column,
                width=120
            )

        self.table.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=10
        )

        # Select record when clicking
        self.table.bind(
            "<<TreeviewSelect>>",
            self.load_selected_record
        )

    # -----------------------------------------------------
    # Validation
    # -----------------------------------------------------

    def validate_inputs(self):

        enrollment = self.enrollment_entry.get().strip()
        name = self.name_entry.get().strip()
        assignment = self.assignment_entry.get().strip()
        status = self.status_combo.get()
        marks_text = self.marks_entry.get().strip()
        remarks = self.remarks_entry.get().strip()

        if not enrollment:
            messagebox.showerror(
                "Error",
                "Enrollment is required."
            )
            return None

        if not name:
            messagebox.showerror(
                "Error",
                "Name is required."
            )
            return None

        if not assignment:
            messagebox.showerror(
                "Error",
                "Assignment is required."
            )
            return None

        # Marks can be empty for pending submissions
        if marks_text:

            try:
                marks = float(marks_text)

            except ValueError:

                messagebox.showerror(
                    "Error",
                    "Marks must be numeric."
                )

                return None

            if marks < 0 or marks > 20:

                messagebox.showerror(
                    "Error",
                    "Marks must be between 0 and 20."
                )

                return None

        else:
            marks = ""

        return {
            "enrollment": enrollment,
            "name": name,
            "assignment": assignment,
            "status": status,
            "marks": marks,
            "remarks": remarks
        }

    # -----------------------------------------------------
    # Add submission
    # -----------------------------------------------------

    def add_submission(self):

        record = self.validate_inputs()

        if record is None:
            return

        self.records.append(record)

        self.save_data()

        self.refresh_table()

        self.clear_fields()

        messagebox.showinfo(
            "Success",
            "Submission added."
        )

    # -----------------------------------------------------
    # Update selected record
    # -----------------------------------------------------

    def update_marks(self):

        selection = self.table.selection()

        if not selection:

            messagebox.showerror(
                "Error",
                "Select a record first."
            )

            return

        record = self.validate_inputs()

        if record is None:
            return

        index = int(selection[0])

        if 0 <= index < len(self.records):

            self.records[index] = record

            self.save_data()

            self.refresh_table()

            messagebox.showinfo(
                "Success",
                "Record updated."
            )

    # -----------------------------------------------------
    # Refresh table
    # -----------------------------------------------------

    def refresh_table(self):

        # Remove existing rows
        for item in self.table.get_children():
            self.table.delete(item)

        selected_filter = self.filter_combo.get()

        for index, record in enumerate(self.records):

            if (
                selected_filter != "All"
                and record["status"] != selected_filter
            ):
                continue

            self.table.insert(
                "",
                tk.END,
                iid=str(index),
                values=(
                    record["enrollment"],
                    record["name"],
                    record["assignment"],
                    record["status"],
                    record["marks"],
                    record["remarks"]
                )
            )

    # -----------------------------------------------------
    # Load selected record into input fields
    # -----------------------------------------------------

    def load_selected_record(self, event=None):

        selection = self.table.selection()

        if not selection:
            return

        index = int(selection[0])

        if index >= len(self.records):
            return

        record = self.records[index]

        self.clear_fields()

        self.enrollment_entry.insert(
            0,
            record["enrollment"]
        )

        self.name_entry.insert(
            0,
            record["name"]
        )

        self.assignment_entry.insert(
            0,
            record["assignment"]
        )

        self.status_combo.set(
            record["status"]
        )

        self.marks_entry.insert(
            0,
            record["marks"]
        )

        self.remarks_entry.insert(
            0,
            record["remarks"]
        )

    # -----------------------------------------------------
    # Clear input fields
    # -----------------------------------------------------

    def clear_fields(self):

        self.enrollment_entry.delete(
            0,
            tk.END
        )

        self.name_entry.delete(
            0,
            tk.END
        )

        self.assignment_entry.delete(
            0,
            tk.END
        )

        self.marks_entry.delete(
            0,
            tk.END
        )

        self.remarks_entry.delete(
            0,
            tk.END
        )

        self.status_combo.set("Pending")

    # -----------------------------------------------------
    # Export CSV
    # -----------------------------------------------------

    def export_csv(self):

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[
                ("CSV files", "*.csv")
            ]
        )

        if not filename:
            return

        fields = [
            "enrollment",
            "name",
            "assignment",
            "status",
            "marks",
            "remarks"
        ]

        try:

            with open(
                filename,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.DictWriter(
                    file,
                    fieldnames=fields
                )

                writer.writeheader()

                writer.writerows(
                    self.records
                )

            messagebox.showinfo(
                "Success",
                "CSV report exported."
            )

        except OSError as error:

            messagebox.showerror(
                "Error",
                str(error)
            )


def main():

    root = tk.Tk()

    app = AssignmentTracker(root)

    root.mainloop()


if __name__ == "__main__":
    main()