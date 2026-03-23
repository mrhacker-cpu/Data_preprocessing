import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from modules.file_handler import load_file
from modules.preprocessing import *
from modules.visualization import plot_multi_hist

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class CSVApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CSV Intelligence Studio 🚀")
        self.geometry("1500x850")

        self.df = None
        self.filtered_df = None
        self.history = []

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main()

    # ---------------- SIDEBAR ----------------
    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=250)
        sidebar.grid(row=0, column=0, sticky="ns")

        ctk.CTkLabel(sidebar, text="📊 DATA STUDIO", font=("Arial", 20, "bold")).pack(pady=20)

        ctk.CTkButton(sidebar, text="Upload CSV", command=self.upload_file).pack(pady=5)
        ctk.CTkButton(sidebar, text="Merge CSV", command=self.merge_csv).pack(pady=5)

        ctk.CTkButton(sidebar, text="Undo", command=self.undo).pack(pady=10)

        ctk.CTkButton(sidebar, text="Remove Nulls", command=self.apply_action(remove_nulls)).pack(pady=3)
        ctk.CTkButton(sidebar, text="Fill Nulls", command=self.apply_action(fill_nulls)).pack(pady=3)
        ctk.CTkButton(sidebar, text="Drop Duplicates", command=self.drop_duplicates_ui).pack(pady=3)

        ctk.CTkButton(sidebar, text="MinMax Scale", command=self.apply_action(minmax_scale)).pack(pady=3)
        ctk.CTkButton(sidebar, text="Standard Scale", command=self.apply_action(standard_scale)).pack(pady=3)
        ctk.CTkButton(sidebar, text="Join CSV", command=self.join_csv).pack(pady=5)

        ctk.CTkButton(sidebar, text="Sample Data", command=self.sample_ui).pack(pady=5)
        ctk.CTkButton(sidebar, text="Apply PCA", command=self.pca_ui).pack(pady=5)

        ctk.CTkButton(sidebar, text="Save Session", command=self.save_session).pack(pady=10)
        ctk.CTkButton(sidebar, text="Load Session", command=self.load_session).pack(pady=5)

        ctk.CTkButton(sidebar, text="Export CSV", command=self.export_csv).pack(pady=10)

        self.theme_switch = ctk.CTkSwitch(sidebar, text="Dark Mode", command=self.toggle_theme)
        self.theme_switch.select()
        self.theme_switch.pack(pady=20)

    # ---------------- MAIN ----------------
    def create_main(self):
        self.main = ctk.CTkFrame(self)
        self.main.grid(row=0, column=1, sticky="nsew")

        self.main.grid_rowconfigure(2, weight=1)
        self.main.grid_columnconfigure(0, weight=1)

        # Top bar
        top = ctk.CTkFrame(self.main)
        top.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.search_entry = ctk.CTkEntry(top, placeholder_text="Search...")
        self.search_entry.pack(side="left", padx=10)

        ctk.CTkButton(top, text="Search", command=self.search_data).pack(side="left")

        self.column_menu = ctk.CTkOptionMenu(top, values=["Select Column"])
        self.column_menu.pack(side="left", padx=10)

        self.slider = ctk.CTkSlider(top, from_=0, to=100, command=self.apply_filter)
        self.slider.pack(side="left", fill="x", expand=True, padx=10)
        self.slider_label = ctk.CTkLabel(top, text="Filter: None")
        self.slider_label.pack(side="left", padx=10)

        # Stats
        self.stats_label = ctk.CTkLabel(self.main, text="No data loaded")
        self.stats_label.grid(row=1, column=0, pady=5)

        # Content area
        content = ctk.CTkFrame(self.main)
        content.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        content.grid_columnconfigure(0, weight=3)
        content.grid_columnconfigure(1, weight=2)
        content.grid_rowconfigure(0, weight=1)

        # Table
        self.table_frame = ctk.CTkScrollableFrame(content)
        self.table_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Graph
        self.graph_frame = ctk.CTkFrame(content)
        self.graph_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Insights
        self.insight_label = ctk.CTkLabel(self.main, text="", wraplength=1200, justify="left")
        self.insight_label.grid(row=3, column=0, pady=10)

    # ---------------- CORE ----------------
    def upload_file(self):
        file = filedialog.askopenfilename(
            filetypes=[("Data Files", "*.csv *.xlsx")]
        )

        if file:
            df = load_file(file)

            # ✅ CHECK BEFORE USING
            if df is None:
                messagebox.showerror("Error", "Failed to load file")
                return

            self.df = df
            self.filtered_df = self.df.copy()

            self.update_column_menu()
            self.refresh_all()

    def merge_csv(self):
        files = filedialog.askopenfilenames(filetypes=[("CSV", "*.csv")])
        dfs = [pd.read_csv(f) for f in files]
        self.df = pd.concat(dfs, ignore_index=True)
        self.filtered_df = self.df.copy()
        self.update_column_menu()
        self.refresh_all()

    def apply_action(self, func):
        return lambda: self.apply_and_refresh(func)
    
    def drop_duplicates_ui(self):
        if self.df is None:
            return

        col = self.column_menu.get()

        if col not in self.df.columns:
            messagebox.showerror("Error", "Select a column first")
            return

        duplicates = self.df[self.df.duplicated(subset=[col], keep=False)]

        if duplicates.empty:
            messagebox.showinfo("Info", "No duplicates found")
            return

        # 🔥 PREVIEW WINDOW
        preview = ctk.CTkToplevel(self)
        preview.title("Duplicate Preview")
        preview.geometry("700x400")

        ctk.CTkLabel(preview, text=f"Duplicates based on '{col}'", font=("Arial", 16)).pack(pady=10)

        frame = ctk.CTkScrollableFrame(preview)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # show duplicate rows
        for i, c_name in enumerate(duplicates.columns):
            ctk.CTkLabel(frame, text=c_name, font=("Arial", 12, "bold")).grid(row=0, column=i)

        for r in range(min(len(duplicates), 50)):
            for c in range(len(duplicates.columns)):
                ctk.CTkLabel(frame, text=str(duplicates.iloc[r, c])).grid(row=r+1, column=c)

        # 🔥 KEEP OPTION
        keep_option = ctk.StringVar(value="first")

        option_menu = ctk.CTkOptionMenu(
            preview,
            values=["first", "last", "remove all"],
            variable=keep_option
        )
        option_menu.pack(pady=10)

        def confirm_action():
            self.save_history()

            if keep_option.get() == "remove all":
                self.df = self.df[~self.df.duplicated(subset=[col], keep=False)]
            else:
                self.df = self.df.drop_duplicates(subset=[col], keep=keep_option.get())

            self.filtered_df = self.df
            self.refresh_all()

            messagebox.showinfo("Done", "Duplicates removed successfully")
            preview.destroy()

        ctk.CTkButton(preview, text="Confirm", command=confirm_action).pack(pady=10)
    def join_csv(self):
        file = filedialog.askopenfilename(filetypes=[("Data Files", "*.csv *.xlsx")])

        if file and self.df is not None:
            df2 = load_file(file)

            if df2 is None:
                return

            col = self.column_menu.get()

            if col not in self.df.columns or col not in df2.columns:
                messagebox.showerror("Error", "Column not found in both datasets")
                return

            self.save_history()
            self.df = self.df.merge(df2, on=col, how="inner")
            self.filtered_df = self.df
            self.refresh_all()

            messagebox.showinfo("Success", "Join completed")

    def apply_and_refresh(self, func):
        if self.df is not None:
            before = len(self.df)

            self.save_history()
            self.df = func(self.df)

            after = len(self.df)

            self.filtered_df = self.df
            self.refresh_all()

            messagebox.showinfo("Result", f"{before - after} rows affected")

    def sample_ui(self):
        if self.df is not None:
            self.save_history()
            self.df = sample_data(self.df, 0.5)
            self.filtered_df = self.df
            self.refresh_all()

    def pca_ui(self):
        if self.df is not None:
            self.save_history()
            self.df = apply_pca(self.df)
            self.filtered_df = self.df
            self.refresh_all()

    def update_column_menu(self):
        if self.df is not None:
            cols = list(self.df.columns)
            self.column_menu.configure(values=cols)

            # auto-set slider range for first numeric column
            num_cols = self.df.select_dtypes(include='number').columns
            if len(num_cols) > 0:
                col = num_cols[0]
                self.slider.configure(
                    from_=float(self.df[col].min()),
                    to=float(self.df[col].max())
                )

    # ---------------- TABLE (RESPONSIVE FIX) ----------------
    def update_table(self):
        for w in self.table_frame.winfo_children():
            w.destroy()

        if self.filtered_df is None:
            return

        df = self.filtered_df

        for col_index in range(len(df.columns)):
            self.table_frame.grid_columnconfigure(col_index, weight=1)

        # Header
        for i, col in enumerate(df.columns):
            ctk.CTkLabel(self.table_frame, text=col, font=("Arial", 12, "bold")).grid(
                row=0, column=i, sticky="ew", padx=5, pady=5
            )

        # Data
        for r in range(min(len(df), 50)):
            for c in range(len(df.columns)):
                value = str(df.iloc[r, c])
                fg = "transparent" if r % 2 == 0 else "#2b2b2b"

                ctk.CTkLabel(
                    self.table_frame,
                    text=value,
                    anchor="w",
                    fg_color=fg,
                    wraplength=150
                ).grid(row=r+1, column=c, sticky="ew", padx=5, pady=2)

    # ---------------- GRAPH ----------------
    def update_graph(self):
        for w in self.graph_frame.winfo_children():
            w.destroy()

        if self.filtered_df is None:
            return

        fig = plot_multi_hist(self.filtered_df)

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        self.generate_insights()

    # ---------------- INFO ----------------
    def update_info(self):
        rows, cols = self.filtered_df.shape
        nulls = self.filtered_df.isnull().sum().sum()
        self.stats_label.configure(text=f"Rows: {rows} | Columns: {cols} | Missing: {nulls}")

    # ---------------- SEARCH ----------------
    def search_data(self):
        if self.df is not None:
            q = self.search_entry.get().lower()
            self.filtered_df = self.df[
                self.df.astype(str).apply(lambda row: row.str.lower().str.contains(q).any(), axis=1)
            ]
            self.refresh_all()

    # ---------------- FILTER ----------------
    def apply_filter(self, value):
        if self.df is not None:
            col = self.column_menu.get()

            if col in self.df.columns and pd.api.types.is_numeric_dtype(self.df[col]):
                self.filtered_df = self.df[self.df[col] <= float(value)]
                self.refresh_all()

    # ---------------- INSIGHTS ----------------
    def generate_insights(self):
        df = self.filtered_df
        insights = []

        if df.isnull().sum().sum() > 0:
            insights.append("⚠ Missing values detected")

        if df.duplicated().sum() > 0:
            insights.append("⚠ Duplicate rows detected")

        for col in df.select_dtypes(include='number').columns:
            if df[col].skew() > 1:
                insights.append(f"{col} is highly skewed")

        self.insight_label.configure(text="\n".join(insights) if insights else "No major issues detected")

    # ---------------- HISTORY ----------------
    def save_history(self):
        if self.df is not None:
            self.history.append(self.df.copy())

    def undo(self):
        if self.history:
            self.df = self.history.pop()
            self.filtered_df = self.df
            self.refresh_all()

    # ---------------- SESSION ----------------
    def save_session(self):
        import pickle
        with open("session.pkl", "wb") as f:
            pickle.dump(self.df, f)
        messagebox.showinfo("Saved", "Session saved")

    def load_session(self):
        import pickle
        try:
            with open("session.pkl", "rb") as f:
                self.df = pickle.load(f)
                self.filtered_df = self.df
                self.update_column_menu()
                self.refresh_all()
        except:
            messagebox.showerror("Error", "No session found")

    # ---------------- EXPORT ----------------
    def export_csv(self):
        if self.filtered_df is not None:
            path = filedialog.asksaveasfilename(defaultextension=".csv")
            if path:
                self.filtered_df.to_csv(path, index=False)

    def refresh_all(self):
        self.update_table()
        self.update_graph()
        self.update_info()

    def toggle_theme(self):
        mode = "dark" if self.theme_switch.get() else "light"
        ctk.set_appearance_mode(mode)


if __name__ == "__main__":
    app = CSVApp()
    app.mainloop()