import os
import pandas as pd
import matplotlib.pyplot as plt

def main():
    filename = input("CSV file path: ").strip()
    output = input("Output folder: ").strip()

    try:
        os.makedirs(output, exist_ok=True)

        df = pd.read_csv(filename)
        subject_cols = list(df.columns[2:])

        for col in subject_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col] = df[col].fillna(df[col].mean())

        df.to_csv(
            os.path.join(output, "cleaned_marks.csv"),
            index=False
        )

        summary = pd.DataFrame({
            "subject": subject_cols,
            "average": [df[c].mean() for c in subject_cols],
            "minimum": [df[c].min() for c in subject_cols],
            "maximum": [df[c].max() for c in subject_cols]
        })

        summary.to_csv(
            os.path.join(output, "summary.csv"),
            index=False
        )

        grades = pd.cut(
            df[subject_cols].mean(axis=1),
            bins=[-1, 40, 50, 60, 70, 80, 90, 100],
            labels=["F", "D", "C", "B", "A", "A+", "O"]
        )

        grades.value_counts().sort_index().plot(kind="bar")
        plt.xlabel("Grade")
        plt.ylabel("Students")
        plt.tight_layout()
        plt.savefig(os.path.join(output, "grade_distribution.png"))
        plt.close()

        summary.plot(
            x="subject",
            y="average",
            kind="bar",
            legend=False
        )
        plt.ylabel("Average Marks")
        plt.tight_layout()
        plt.savefig(os.path.join(output, "subject_average.png"))
        plt.close()

        df["average"] = df[subject_cols].mean(axis=1)
        top = df.nlargest(5, "average")

        plt.bar(top["name"], top["average"])
        plt.xlabel("Student")
        plt.ylabel("Average")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.savefig(os.path.join(output, "top_performers.png"))
        plt.close()

        print("cleaned_marks.csv")
        print("summary.csv")
        print("grade_distribution.png")
        print("subject_average.png")
        print("top_performers.png")

    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()