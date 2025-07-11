import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import test

# Modern color palette
COLORS = {
    'bg': '#F4F6FB',
    'primary': '#2563eb',
    'accent': '#22d3ee',
    'text': '#22223b',
    'card': '#fff',
    'button': '#2563eb',
    'button_hover': '#1e40af',
    'error': '#ef4444',
    'success': '#22c55e',
}

FONT = ('Segoe UI', 11)
TITLE_FONT = ('Segoe UI', 28, 'bold')
SUBTITLE_FONT = ('Segoe UI', 16)

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        canvas = tk.Canvas(self, bg=COLORS['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas, style='Card.TFrame')
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        self.window_id = canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas = canvas
        self.bind_mousewheel(canvas)
        # Ensure the scrollable_frame always matches the canvas width
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(self.window_id, width=canvas.winfo_width())
        )
    def bind_mousewheel(self, widget):
        widget.bind_all("<MouseWheel>", self._on_mousewheel)
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

class ModernButton(ttk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.default_style = kwargs.get('style', 'Modern.TButton')
        self.hover_style = 'Modern.TButton.Hover'
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
    def on_enter(self, e):
        self.configure(style=self.hover_style)
    def on_leave(self, e):
        self.configure(style=self.default_style)

class WelcomePage:
    def __init__(self, root, switch_callback):
        self.root = root
        self.switch_callback = switch_callback
        self.root.configure(bg=COLORS['bg'])
        style = ttk.Style()
        style.configure('Card.TFrame', background=COLORS['card'], relief='flat')
        style.configure('Title.TLabel', background=COLORS['card'], font=TITLE_FONT, foreground=COLORS['primary'])
        style.configure('Subtitle.TLabel', background=COLORS['card'], font=SUBTITLE_FONT, foreground=COLORS['text'])
        style.configure('Modern.TButton', font=FONT, background=COLORS['button'], foreground='white', padding=16)
        style.configure('Modern.TButton.Hover', background=COLORS['button_hover'], foreground='white')
        style.configure('Modern.TCheckbutton',
                       background=COLORS['card'],
                       foreground=COLORS['primary'],
                       font=FONT)
        # Centered card
        card = ttk.Frame(self.root, style='Card.TFrame', padding=40)
        card.place(relx=0.5, rely=0.5, anchor='center')
        ttk.Label(card, text='Job Scheduler', style='Title.TLabel').pack(pady=(0, 10))
        ttk.Label(card, text='Optimize your workflow', style='Subtitle.TLabel').pack(pady=(0, 30))
        ModernButton(card, text='Backtracking', command=lambda: self.switch_callback('Backtracking')).pack(fill='x', pady=8)
        ModernButton(card, text='Genetic Algorithm', command=lambda: self.switch_callback('Genetic')).pack(fill='x', pady=8)
        ttk.Label(card, text='by Your Name', style='Subtitle.TLabel', font=('Segoe UI', 10), foreground=COLORS['accent']).pack(pady=(30,0))

class SchedulerPage:
    def __init__(self, root, algorithm, back_callback):
        self.root = root
        self.algorithm = algorithm
        self.back_callback = back_callback
        self.root.configure(bg=COLORS['bg'])
        style = ttk.Style()
        style.configure('Card.TFrame', background=COLORS['card'], relief='flat')
        style.configure('Section.TLabelframe', background=COLORS['card'], font=FONT)
        style.configure('Section.TLabelframe.Label', background=COLORS['card'], font=FONT, foreground=COLORS['primary'])
        style.configure('Modern.TButton', font=FONT, background=COLORS['button'], foreground='white', padding=12)
        style.configure('Modern.TButton.Hover', background=COLORS['button_hover'], foreground='white')
        style.configure('Modern.TEntry', fieldbackground=COLORS['card'], borderwidth=1, relief='solid')
        style.configure('Modern.TCheckbutton',
                       background=COLORS['card'],
                       foreground=COLORS['primary'],
                       font=FONT)
        # Header
        header = ttk.Frame(self.root, style='Card.TFrame', padding=(30, 20))
        header.pack(fill='x', pady=(0, 10))
        ttk.Label(header, text='Configure Your Job Scheduling Problem', style='Title.TLabel').pack(side='left')
        ModernButton(header, text='Back', command=self.back_callback, style='Modern.TButton').pack(side='right')
        # Main content (now scrollable)
        scrollable = ScrollableFrame(self.root)
        scrollable.pack(fill='both', expand=True)
        content = scrollable.scrollable_frame
        content.grid_columnconfigure(0, weight=1)
        # Input section
        input_card = ttk.Labelframe(content, text='Basic Data', style='Section.TLabelframe', padding=20)
        input_card.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        input_card.grid_columnconfigure(1, weight=1)
        ttk.Label(input_card, text='Number of Jobs:', style='Subtitle.TLabel').grid(row=0, column=0, sticky='w', pady=4)
        self.num_jobs = ttk.Entry(input_card, width=10, style='Modern.TEntry')
        self.num_jobs.grid(row=0, column=1, pady=4, sticky='ew')
        self.num_jobs.insert(0, '2')
        ttk.Label(input_card, text='Job Durations (comma-separated):', style='Subtitle.TLabel').grid(row=1, column=0, sticky='w', pady=4)
        self.job_durations = ttk.Entry(input_card, width=30, style='Modern.TEntry')
        self.job_durations.grid(row=1, column=1, pady=4, sticky='ew')
        self.job_durations.insert(0, '2,3')
        ttk.Label(input_card, text='Number of Machines:', style='Subtitle.TLabel').grid(row=2, column=0, sticky='w', pady=4)
        self.num_machines = ttk.Entry(input_card, width=10, style='Modern.TEntry')
        self.num_machines.grid(row=2, column=1, pady=4, sticky='ew')
        self.num_machines.insert(0, '2')
        ttk.Label(input_card, text='Machine Capacities (comma-separated):', style='Subtitle.TLabel').grid(row=3, column=0, sticky='w', pady=4)
        self.machine_caps = ttk.Entry(input_card, width=30, style='Modern.TEntry')
        self.machine_caps.grid(row=3, column=1, pady=4, sticky='ew')
        self.machine_caps.insert(0, '1,1')
        # Algorithm selection (show as label, but keep for logic)
        ttk.Label(input_card, text='Algorithm:', style='Subtitle.TLabel').grid(row=4, column=0, sticky='w', pady=4)
        self.algorithm_label = ttk.Label(input_card, text=algorithm, style='Subtitle.TLabel', foreground=COLORS['primary'])
        self.algorithm_label.grid(row=4, column=1, pady=4, sticky='w')
        # Auto-assign option
        self.auto_split = tk.BooleanVar(value=True)
        ttk.Checkbutton(input_card, text="Auto-assign jobs to machines", variable=self.auto_split, style='Modern.TCheckbutton').grid(row=5, column=0, columnspan=2, sticky="w", pady=4)
        # Constraints section
        constraints_card = ttk.Labelframe(content, text='Constraints', style='Section.TLabelframe', padding=20)
        constraints_card.grid(row=1, column=0, sticky='ew', padx=10, pady=10)
        ttk.Label(constraints_card, text='Precedence Constraints (job1 job2 per line):', style='Subtitle.TLabel').pack(anchor='w', pady=(0,2))
        self.precedence = scrolledtext.ScrolledText(constraints_card, width=30, height=2, font=FONT)
        self.precedence.pack(fill='x', pady=2)
        ttk.Label(constraints_card, text='Resource Constraints (job machine per line):', style='Subtitle.TLabel').pack(anchor='w', pady=(8,2))
        self.resources = scrolledtext.ScrolledText(constraints_card, width=30, height=2, font=FONT)
        self.resources.pack(fill='x', pady=2)
        ttk.Label(constraints_card, text='Temporal Constraints (job time per line):', style='Subtitle.TLabel').pack(anchor='w', pady=(8,2))
        self.temporal = scrolledtext.ScrolledText(constraints_card, width=30, height=2, font=FONT)
        self.temporal.pack(fill='x', pady=2)
        # Solve button
        ModernButton(content, text='Solve', command=self.solve, style='Modern.TButton').grid(row=2, column=0, pady=20, sticky='ew')
        # Results area
        self.result_card = ttk.Labelframe(content, text='Schedule', style='Section.TLabelframe', padding=20)
        self.result_card.grid(row=3, column=0, sticky='ew', padx=10, pady=10)
        self.result_label = ttk.Label(self.result_card, text='', style='Subtitle.TLabel')
        self.result_label.pack()
        self.fig, self.ax = plt.subplots(figsize=(10, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.result_card)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        # Configure grid weights
        content.grid_rowconfigure(3, weight=1)
        content.grid_columnconfigure(0, weight=1)
    def parse_constraints(self, text, convert_to_zero_based=True):
        constraints = []
        for line in text.split('\n'):
            line = line.strip()
            if line:
                try:
                    a, b = map(int, line.split())
                    if convert_to_zero_based:
                        constraints.append((a-1, b-1))
                    else:
                        constraints.append((a, b))
                except ValueError:
                    continue
        return constraints
    def parse_temporal_constraints(self, text):
        constraints = {}
        for line in text.split('\n'):
            line = line.strip()
            if line:
                try:
                    job, time = map(int, line.split())
                    constraints[job-1] = time
                except ValueError:
                    continue
        return constraints
    def solve(self):
        try:
            job_durations = [int(x.strip()) for x in self.job_durations.get().split(',')]
            machine_capacities = [int(x.strip()) for x in self.machine_caps.get().split(',')]
            num_machines = int(self.num_machines.get())
            # Validate basic inputs
            if len(job_durations) != int(self.num_jobs.get()):
                raise ValueError("Number of job durations doesn't match number of jobs")
            if len(machine_capacities) != num_machines:
                raise ValueError("Number of machine capacities doesn't match number of machines")
            # Parse constraints
            precedence_constraints = self.parse_constraints(self.precedence.get("1.0", tk.END))
            resource_constraints = self.parse_constraints(self.resources.get("1.0", tk.END))
            temporal_constraints = self.parse_temporal_constraints(self.temporal.get("1.0", tk.END))
            # Call appropriate algorithm
            if self.algorithm == "Backtracking":
                schedule, makespan = test.backtracking(
                    job_durations, num_machines, precedence_constraints,
                    resource_constraints, machine_capacities, self.auto_split.get(), temporal_constraints
                )
            else:
                schedule, makespan = test.genetic_algorithm(
                    job_durations, num_machines, precedence_constraints,
                    resource_constraints, machine_capacities, self.auto_split.get(), temporal_constraints
                )
            if schedule:
                self.plot_schedule(schedule, makespan)
                self.result_label.config(text=f"Makespan: {makespan}", foreground=COLORS['success'])
            else:
                self.result_label.config(text="No valid schedule found", foreground=COLORS['error'])
                self.ax.clear()
                self.canvas.draw()
        except Exception as e:
            self.result_label.config(text=str(e), foreground=COLORS['error'])
            self.ax.clear()
            self.canvas.draw()
    def plot_schedule(self, schedule, makespan):
        self.ax.clear()
        colors = plt.cm.Set3(np.linspace(0, 1, len(schedule)))
        # --- New logic to stack overlapping jobs ---
        # Get machine list
        machines = set(machine for _, (_, _, machine) in schedule.items())
        # Build time slots for each machine
        time_slots = {}
        for job, (start, end, machine) in schedule.items():
            for t in range(start, end):
                if (machine, t) not in time_slots:
                    time_slots[(machine, t)] = []
                time_slots[(machine, t)].append(job)
        # Assign slot positions to jobs
        job_positions = {}
        for job, (start, end, machine) in schedule.items():
            concurrent = set()
            for t in range(start, end):
                concurrent.update(time_slots.get((machine, t), []))
            used = {job_positions.get(j, -1) for j in concurrent if j in job_positions}
            pos = 0
            while pos in used:
                pos += 1
            job_positions[job] = pos
        # Plot each job in its slot
        yticks = []
        yticklabels = []
        for job, (start, end, machine) in schedule.items():
            position = job_positions[job]
            y_pos = f"Machine {machine+1} (Slot {position+1})"
            self.ax.barh(y=y_pos, width=end-start, left=start, color=colors[job], label=f"Job {job+1}")
            if y_pos not in yticklabels:
                yticks.append(y_pos)
                yticklabels.append(y_pos)
        self.ax.set_xlabel('Time', color=COLORS['text'])
        self.ax.set_title(f'Job Schedule', color=COLORS['primary'])
        self.ax.grid(True, color=COLORS['accent'], linestyle='--', alpha=0.3)
        # Remove duplicate legend entries
        handles, labels = self.ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        self.ax.legend(by_label.values(), by_label.keys(), bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
        self.ax.invert_yaxis()
        self.fig.tight_layout()
        self.fig.subplots_adjust(right=0.85)
        self.canvas.draw()

class App:
    def __init__(self, root):
        self.root = root
        self.show_welcome()
    def show_welcome(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        WelcomePage(self.root, self.show_scheduler)
    def show_scheduler(self, algorithm):
        for widget in self.root.winfo_children():
            widget.destroy()
        SchedulerPage(self.root, algorithm, self.show_welcome)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Job Scheduler")
    root.geometry("900x700")
    app = App(root)
    root.mainloop() 