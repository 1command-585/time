import tkinter as tk
from tkinter import ttk, messagebox
import math
from datetime import datetime

class MultiClockTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("时钟 & 计时器（双模式）")
        self.root.geometry("600x700")
        self.root.resizable(True, True)

        # 创建选项卡控件
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        # 1. 时钟模式界面
        self.clock_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.clock_frame, text="🕒 时钟模式")
        self.init_clock_mode()

        # 2. 计时器模式界面（包含正计时和倒计时）
        self.timer_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.timer_frame, text="⏱️ 计时器模式")
        self.init_timer_mode()

        # 启动时钟模式的实时刷新
        self.update_clock_display()

    # ==================== 时钟模式 ====================
    def init_clock_mode(self):
        """初始化时钟模式：模拟时钟画布 + 电子时钟标签"""
        # 画布用于绘制模拟时钟
        self.canvas = tk.Canvas(self.clock_frame, bg='white', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 电子时钟标签
        self.digital_label = tk.Label(self.clock_frame, font=("Arial", 36, "bold"), fg="blue")
        self.digital_label.pack(pady=10)

        # 绑定窗口大小改变事件，重绘模拟时钟
        self.root.bind('<Configure>', self.on_resize)

    def on_resize(self, event):
        """窗口大小改变时重新绘制模拟时钟（仅当时钟选项卡可见时）"""
        if event.widget == self.root:
            # 获取当前选中的选项卡
            current_tab = self.notebook.index(self.notebook.select())
            if current_tab == 0:  # 时钟模式
                self.draw_analog_clock()

    def draw_analog_clock(self):
        """绘制模拟时钟表盘和指针"""
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width < 10 or height < 10:
            return

        # 圆心和半径
        radius = min(width, height) / 2 * 0.85
        cx, cy = width / 2, height / 2

        # 绘制外圆
        self.canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius,
                                outline="black", width=3)

        # 绘制刻度及数字
        for i in range(60):
            angle = math.radians(i * 6 - 90)
            if i % 5 == 0:
                inner = radius * 0.85
                outer = radius
                hour = i // 5 if i // 5 != 0 else 12
                text_x = cx + radius * 0.7 * math.cos(angle)
                text_y = cy + radius * 0.7 * math.sin(angle)
                self.canvas.create_text(text_x, text_y, text=str(hour),
                                        font=("Arial", int(radius * 0.12), "bold"))
            else:
                inner = radius * 0.92
                outer = radius
            start_x = cx + inner * math.cos(angle)
            start_y = cy + inner * math.sin(angle)
            end_x = cx + outer * math.cos(angle)
            end_y = cy + outer * math.sin(angle)
            width_line = 2 if i % 5 == 0 else 1
            self.canvas.create_line(start_x, start_y, end_x, end_y,
                                    fill="black", width=width_line)

        # 获取当前时间
        now = datetime.now()
        hour = now.hour % 12
        minute = now.minute
        second = now.second

        # 角度
        hour_angle = math.radians((hour + minute/60) * 30 - 90)
        minute_angle = math.radians(minute * 6 - 90)
        second_angle = math.radians(second * 6 - 90)

        hour_len = radius * 0.5
        minute_len = radius * 0.7
        second_len = radius * 0.85

        # 时针
        hour_x = cx + hour_len * math.cos(hour_angle)
        hour_y = cy + hour_len * math.sin(hour_angle)
        self.canvas.create_line(cx, cy, hour_x, hour_y, fill="black", width=6, capstyle=tk.ROUND)

        # 分针
        minute_x = cx + minute_len * math.cos(minute_angle)
        minute_y = cy + minute_len * math.sin(minute_angle)
        self.canvas.create_line(cx, cy, minute_x, minute_y, fill="black", width=4, capstyle=tk.ROUND)

        # 秒针（红色）
        second_x = cx + second_len * math.cos(second_angle)
        second_y = cy + second_len * math.sin(second_angle)
        self.canvas.create_line(cx, cy, second_x, second_y, fill="red", width=2, capstyle=tk.ROUND)

        # 中心圆点
        self.canvas.create_oval(cx - 5, cy - 5, cx + 5, cy + 5, fill="black")

    def update_clock_display(self):
        """更新时间：更新电子时钟文字，并重绘模拟时钟（如果时钟选项卡可见）"""
        # 更新电子时钟
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        self.digital_label.config(text=time_str)

        # 重绘模拟时钟（仅当时钟选项卡被选中时，提高性能）
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 0:
            self.draw_analog_clock()

        self.root.after(1000, self.update_clock_display)

    # ==================== 计时器模式 ====================
    def init_timer_mode(self):
        """初始化计时器模式：包含正计时器和倒计时器（使用Notebook子选项卡）"""
        # 在计时器模式中再创建一个子选项卡，用于区分正计时和倒计时
        sub_notebook = ttk.Notebook(self.timer_frame)
        sub_notebook.pack(fill='both', expand=True)

        # 正计时器界面
        self.forward_frame = ttk.Frame(sub_notebook)
        sub_notebook.add(self.forward_frame, text="正计时器")
        self.init_forward_timer()

        # 倒计时器界面
        self.backward_frame = ttk.Frame(sub_notebook)
        sub_notebook.add(self.backward_frame, text="倒计时器")
        self.init_backward_timer()

    # ----- 正计时器 -----
    def init_forward_timer(self):
        # 时间显示
        self.forward_label = tk.Label(self.forward_frame, text="00:00:00", font=("Arial", 48))
        self.forward_label.pack(pady=30)

        btn_frame = tk.Frame(self.forward_frame)
        btn_frame.pack(pady=10)

        self.forward_start_btn = tk.Button(btn_frame, text="开始", command=self.forward_start, width=10)
        self.forward_start_btn.pack(side='left', padx=5)

        self.forward_pause_btn = tk.Button(btn_frame, text="暂停", command=self.forward_pause, width=10)
        self.forward_pause_btn.pack(side='left', padx=5)

        self.forward_reset_btn = tk.Button(btn_frame, text="重置", command=self.forward_reset, width=10)
        self.forward_reset_btn.pack(side='left', padx=5)

        self.forward_running = False
        self.forward_seconds = 0
        self.forward_after_id = None

    def forward_update(self):
        if self.forward_running:
            self.forward_seconds += 1
            self.forward_label.config(text=self.format_time(self.forward_seconds))
            self.forward_after_id = self.root.after(1000, self.forward_update)

    def forward_start(self):
        if not self.forward_running:
            self.forward_running = True
            self.forward_update()

    def forward_pause(self):
        if self.forward_running:
            self.forward_running = False
            if self.forward_after_id:
                self.root.after_cancel(self.forward_after_id)
                self.forward_after_id = None

    def forward_reset(self):
        self.forward_pause()
        self.forward_seconds = 0
        self.forward_label.config(text="00:00:00")

    # ----- 倒计时器 -----
    def init_backward_timer(self):
        # 输入框
        input_frame = tk.Frame(self.backward_frame)
        input_frame.pack(pady=20)

        tk.Label(input_frame, text="时:", font=("Arial", 12)).pack(side='left')
        self.hour_entry = tk.Entry(input_frame, width=5, font=("Arial", 12))
        self.hour_entry.pack(side='left', padx=5)
        self.hour_entry.insert(0, "0")

        tk.Label(input_frame, text="分:", font=("Arial", 12)).pack(side='left')
        self.min_entry = tk.Entry(input_frame, width=5, font=("Arial", 12))
        self.min_entry.pack(side='left', padx=5)
        self.min_entry.insert(0, "0")

        tk.Label(input_frame, text="秒:", font=("Arial", 12)).pack(side='left')
        self.sec_entry = tk.Entry(input_frame, width=5, font=("Arial", 12))
        self.sec_entry.pack(side='left', padx=5)
        self.sec_entry.insert(0, "0")

        self.set_btn = tk.Button(self.backward_frame, text="设置倒计时", command=self.set_countdown, width=15)
        self.set_btn.pack(pady=5)

        self.backward_label = tk.Label(self.backward_frame, text="00:00:00", font=("Arial", 48))
        self.backward_label.pack(pady=20)

        btn_frame = tk.Frame(self.backward_frame)
        btn_frame.pack(pady=10)

        self.backward_start_btn = tk.Button(btn_frame, text="开始", command=self.backward_start, width=10)
        self.backward_start_btn.pack(side='left', padx=5)

        self.backward_pause_btn = tk.Button(btn_frame, text="暂停", command=self.backward_pause, width=10)
        self.backward_pause_btn.pack(side='left', padx=5)

        self.backward_reset_btn = tk.Button(btn_frame, text="重置", command=self.backward_reset, width=10)
        self.backward_reset_btn.pack(side='left', padx=5)

        self.backward_running = False
        self.backward_seconds = 0
        self.saved_seconds = 0
        self.backward_after_id = None

    def set_countdown(self):
        try:
            hours = int(self.hour_entry.get())
            minutes = int(self.min_entry.get())
            seconds = int(self.sec_entry.get())
            total = hours * 3600 + minutes * 60 + seconds
            if total < 0:
                raise ValueError
            self.saved_seconds = total
            self.backward_seconds = total
            self.backward_label.config(text=self.format_time(total))
            if self.backward_running:
                self.backward_pause()
        except ValueError:
            messagebox.showerror("错误", "请输入有效的非负整数（时、分、秒）")

    def backward_update(self):
        if self.backward_running and self.backward_seconds > 0:
            self.backward_seconds -= 1
            self.backward_label.config(text=self.format_time(self.backward_seconds))
            self.backward_after_id = self.root.after(1000, self.backward_update)
        elif self.backward_running and self.backward_seconds == 0:
            self.backward_pause()
            messagebox.showinfo("倒计时结束", "时间到！")

    def backward_start(self):
        if not self.backward_running and self.backward_seconds > 0:
            self.backward_running = True
            self.backward_update()

    def backward_pause(self):
        if self.backward_running:
            self.backward_running = False
            if self.backward_after_id:
                self.root.after_cancel(self.backward_after_id)
                self.backward_after_id = None

    def backward_reset(self):
        self.backward_pause()
        self.backward_seconds = self.saved_seconds
        self.backward_label.config(text=self.format_time(self.backward_seconds))

    # ----- 辅助方法 -----
    @staticmethod
    def format_time(seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"


if __name__ == "__main__":
    root = tk.Tk()
    app = MultiClockTimerApp(root)
    root.mainloop()