import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from PIL import Image, ImageTk

class VideoTextRemover:
    HANDLE_SIZE = 8
    ACCENT_COLOR = "#4a6fa5"
    DARK_BG = "#2d2d2d"
    LIGHT_BG = "#3a3a3a"
    TEXT_COLOR = "#ffffff"
    HIGHLIGHT_COLOR = "#5a8fd8"
    
    def __init__(self, root):
        self.root = root
        self.root.title("Video Text Remover Pro")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)
        
        # Set window icon
        try:
            self.root.iconbitmap("icon.ico")  # Add your icon file
        except:
            pass
            
        # Configure style
        self.configure_styles()
        
        # Main container
        self.setup_main_container()
        
        # Canvas area
        self.setup_canvas_area()
        
        # Controls panel
        self.setup_controls_panel()
        
        # Bindings
        self.setup_bindings()
        
        # Internal state
        self.initialize_state()

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('.', background=self.DARK_BG, foreground=self.TEXT_COLOR)
        
        # Frame styles
        style.configure('TFrame', background=self.DARK_BG)
        style.configure('Bordered.TFrame', background=self.LIGHT_BG, 
                       borderwidth=1, relief='solid', bordercolor='#444')
        
        # Label styles
        style.configure('TLabel', background=self.DARK_BG, foreground=self.TEXT_COLOR,
                       font=('Segoe UI', 9))
        style.configure('Title.TLabel', font=('Segoe UI', 11, 'bold'))
        style.configure('Accent.TLabel', foreground=self.ACCENT_COLOR)
        
        # Button styles
        style.configure('TButton', font=('Segoe UI', 9), borderwidth=1)
        style.configure('Accent.TButton', background=self.ACCENT_COLOR, 
                        foreground='white', font=('Segoe UI', 9, 'bold'))
        style.map('Accent.TButton',
                  background=[('active', self.HIGHLIGHT_COLOR), ('disabled', '#555')])
        
        # Entry styles
        style.configure('TEntry', fieldbackground=self.LIGHT_BG, 
                        foreground=self.TEXT_COLOR, insertcolor='white')
        
        # Scale styles
        style.configure('Horizontal.TScale', troughcolor='#4b4b4b', 
                       background=self.ACCENT_COLOR)
        
        # Progressbar styles
        style.configure('Horizontal.TProgressbar', troughcolor='#4b4b4b', 
                       background=self.ACCENT_COLOR, thickness=10)
        
        # Notebook styles
        style.configure('TNotebook', background=self.DARK_BG)
        style.configure('TNotebook.Tab', background=self.LIGHT_BG, 
                       padding=[10, 5], font=('Segoe UI', 9))
        style.map('TNotebook.Tab',
                 background=[('selected', self.ACCENT_COLOR)],
                 foreground=[('selected', 'white')])

    def setup_main_container(self):
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configure grid weights
        self.main_container.columnconfigure(0, weight=3)
        self.main_container.columnconfigure(1, weight=1)
        self.main_container.rowconfigure(0, weight=1)

    def setup_canvas_area(self):
        # Canvas container with shadow effect
        canvas_container = ttk.Frame(self.main_container, style='Bordered.TFrame')
        canvas_container.grid(row=0, column=0, sticky='nsew', padx=(0, 10), pady=5)
        canvas_container.rowconfigure(0, weight=1)
        canvas_container.columnconfigure(0, weight=1)
        
        # Canvas with black background
        self.canvas = tk.Canvas(canvas_container, bg='#000000', highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky='nsew', padx=1, pady=1)
        
        # Status bar at bottom of canvas
        self.canvas_status = ttk.Frame(canvas_container, height=20, style='Bordered.TFrame')
        self.canvas_status.grid(row=1, column=0, sticky='ew')
        self.canvas_status_label = ttk.Label(self.canvas_status, text="Ready", style='Accent.TLabel')
        self.canvas_status_label.pack(side='left', padx=5)

    def setup_controls_panel(self):
        # Main controls frame
        controls_frame = ttk.Frame(self.main_container)
        controls_frame.grid(row=0, column=1, sticky='nsew')
        
        # Notebook for tabbed interface
        self.notebook = ttk.Notebook(controls_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Video Controls Tab
        self.setup_video_tab()
        
        # Mask Tools Tab
        self.setup_mask_tab()
        
        # Processing Tab
        self.setup_processing_tab()

    def setup_video_tab(self):
        video_tab = ttk.Frame(self.notebook)
        self.notebook.add(video_tab, text='Video')
        
        # Load video section
        load_frame = ttk.LabelFrame(video_tab, text=' Video Source ')
        load_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(load_frame, text='Load Video', style='Accent.TButton',
                  command=self.load_video).pack(fill='x', padx=5, pady=5)
        
        # Video info
        self.video_info = ttk.Label(load_frame, text="No video loaded", style='Accent.TLabel')
        self.video_info.pack(pady=(0, 5))
        
        # Frame navigation
        nav_frame = ttk.LabelFrame(video_tab, text=' Frame Navigation ')
        nav_frame.pack(fill='x', padx=5, pady=5)
        
        self.frame_slider = ttk.Scale(nav_frame, from_=0, to=0, orient='horizontal')
        self.frame_slider.pack(fill='x', padx=5, pady=5)
        self.frame_slider.bind('<ButtonRelease-1>', lambda e: self.on_slider(self.frame_slider.get()))
        
        self.frame_label = ttk.Label(nav_frame, text='Frame: 0/0')
        self.frame_label.pack()
        
        # Navigation buttons
        btn_frame = ttk.Frame(nav_frame)
        btn_frame.pack(fill='x', pady=5)
        
        ttk.Button(btn_frame, text='<<', command=lambda: self.seek_frame(0)).pack(side='left', expand=True)
        ttk.Button(btn_frame, text='<', command=self.prev_frame).pack(side='left', expand=True)
        ttk.Button(btn_frame, text='>', command=self.next_frame).pack(side='left', expand=True)
        ttk.Button(btn_frame, text='>>', command=lambda: self.seek_frame(self.total_frames-1)).pack(side='left', expand=True)

    def setup_mask_tab(self):
        mask_tab = ttk.Frame(self.notebook)
        self.notebook.add(mask_tab, text='Mask Tools')
        
        # Mask controls
        ctrl_frame = ttk.LabelFrame(mask_tab, text=' Mask Controls ')
        ctrl_frame.pack(fill='x', padx=5, pady=5)
        
        btn_frame = ttk.Frame(ctrl_frame)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(btn_frame, text='Undo', command=self.undo).pack(side='left', expand=True)
        ttk.Button(btn_frame, text='Redo', command=self.redo).pack(side='left', expand=True)
        
        btn_frame2 = ttk.Frame(ctrl_frame)
        btn_frame2.pack(fill='x', padx=5, pady=(0, 5))
        
        ttk.Button(btn_frame2, text='Delete', command=self.delete_selected).pack(side='left', expand=True)
        ttk.Button(btn_frame2, text='Clear All', command=self.clear_all).pack(side='left', expand=True)
        
        # Mask list
        list_frame = ttk.LabelFrame(mask_tab, text=' Mask List ')
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.mask_list = tk.Listbox(list_frame, bg=self.LIGHT_BG, fg=self.TEXT_COLOR,
                                  selectbackground=self.ACCENT_COLOR, selectforeground='white')
        self.mask_list.pack(fill='both', expand=True, padx=5, pady=5)
        self.mask_list.bind('<<ListboxSelect>>', self.on_mask_select)

    def setup_processing_tab(self):
        process_tab = ttk.Frame(self.notebook)
        self.notebook.add(process_tab, text='Processing')
        
        # Output settings
        out_frame = ttk.LabelFrame(process_tab, text=' Output Settings ')
        out_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(out_frame, text='Output Format:').pack(anchor='w', padx=5)
        self.format_var = tk.StringVar(value='MP4')
        ttk.Combobox(out_frame, textvariable=self.format_var, 
                    values=['MP4', 'AVI', 'MOV']).pack(fill='x', padx=5, pady=(0, 5))
        
        # Processing buttons
        btn_frame = ttk.Frame(process_tab)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(btn_frame, text='Process Video', style='Accent.TButton',
                  command=self.remove_text).pack(fill='x', padx=5, pady=5)
        
        ttk.Button(btn_frame, text='Cancel Processing', 
                  command=self.cancel_processing).pack(fill='x', padx=5, pady=(0, 5))
        
        # Progress
        prog_frame = ttk.LabelFrame(process_tab, text=' Progress ')
        prog_frame.pack(fill='x', padx=5, pady=5)
        
        self.progress_var = tk.DoubleVar(value=0)
        self.progress = ttk.Progressbar(prog_frame, variable=self.progress_var, maximum=100)
        self.progress.pack(fill='x', padx=5, pady=5)
        
        self.progress_label = ttk.Label(prog_frame, text='0%')
        self.progress_label.pack()
        
        # Log
        log_frame = ttk.LabelFrame(process_tab, text=' Processing Log ')
        log_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.log = tk.Text(log_frame, height=8, bg=self.LIGHT_BG, fg=self.TEXT_COLOR,
                          font=('Consolas', 9), wrap='word')
        self.log.pack(fill='both', expand=True, padx=5, pady=5)
        
        scroll = ttk.Scrollbar(log_frame, command=self.log.yview)
        scroll.pack(side='right', fill='y')
        self.log.config(yscrollcommand=scroll.set)
        
        self.log.insert('end', 'Ready.')
        self.log.config(state='disabled')

    def setup_bindings(self):
        self.canvas.bind('<ButtonPress-1>', self.on_mouse_down)
        self.canvas.bind('<B1-Motion>', self.on_mouse_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_up)
        self.root.bind('<Control-z>', self.undo)
        self.root.bind('<Control-y>', self.redo)
        self.root.bind('<Delete>', lambda e: self.delete_selected())

    def initialize_state(self):
        self.rectangles = []
        self.undo_stack = []
        self.redo_stack = []
        self.selected_idx = None
        self.drawing = self.dragging = self.resizing = False
        self.start_x = self.start_y = self.handle_idx = None
        self.cap = None
        self.frame = None
        self.video_path = None
        self.total_frames = 0
        self.cancel_requested = False
        self.photo = None

    def log_msg(self, msg):
        self.log.config(state='normal')
        self.log.insert('end', '\n' + msg)
        self.log.see('end')
        self.log.config(state='disabled')
        self.canvas_status_label.config(text=msg)

    def load_video(self):
        path = filedialog.askopenfilename(
            filetypes=[('Video Files', '*.mp4;*.avi;*.mov;*.mkv'), ('All Files', '*.*')]
        )
        if not path: 
            return
            
        self.video_path = path
        self.cap = cv2.VideoCapture(path)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Could not open video file")
            return
            
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        duration = self.total_frames / fps
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        
        self.frame_slider.config(from_=0, to=self.total_frames-1)
        self.video_info.config(text=f"{path.split('/')[-1]}\n{self.total_frames} frames | {minutes}m {seconds}s | {fps:.1f} fps")
        self.log_msg(f'Loaded video: {path}')
        self.seek_frame(0)

    def on_slider(self, val):
        idx = int(float(val))
        self.seek_frame(idx)

    def seek_frame(self, idx):
        if not self.cap: 
            return
            
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = self.cap.read()
        if not ret: 
            return
            
        self.frame = frame
        self.display_frame(frame)
        self.frame_label.config(text=f'Frame: {idx+1}/{self.total_frames}')
        self.frame_slider.set(idx)

    def prev_frame(self):
        if not self.cap: 
            return
            
        idx = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
        if idx > 0:
            self.seek_frame(idx-1)

    def next_frame(self):
        if not self.cap: 
            return
            
        idx = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
        if idx < self.total_frames-1:
            self.seek_frame(idx+1)

    def display_frame(self, frame):
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w = img.shape[:2]
        
        # Calculate scaling to fit canvas while maintaining aspect ratio
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        scale = min(canvas_width/w, canvas_height/h)
        nw, nh = int(w*scale), int(h*scale)
        
        resized = cv2.resize(img, (nw, nh))
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(resized))
        
        self.canvas.delete('all')
        self.canvas.create_image(canvas_width//2, canvas_height//2, image=self.photo, anchor='center')
        self.draw_rectangles()

    def draw_rectangles(self):
        self.canvas.delete('rect')
        self.mask_list.delete(0, tk.END)
        
        for idx, (x1,y1,x2,y2) in enumerate(self.rectangles):
            # Draw rectangle
            col = self.ACCENT_COLOR if idx==self.selected_idx else 'red'
            self.canvas.create_rectangle(x1,y1,x2,y2, outline=col, width=2, dash=(5,1), tags='rect')
            
            # Add to listbox
            self.mask_list.insert(tk.END, f"Mask {idx+1}: ({x1},{y1}) to ({x2},{y2})")
            
            # Draw handles if selected
            if idx==self.selected_idx:
                self.draw_handles((x1,y1,x2,y2))
        
        # Highlight selected item in listbox
        if self.selected_idx is not None:
            self.mask_list.selection_clear(0, tk.END)
            self.mask_list.selection_set(self.selected_idx)
            self.mask_list.see(self.selected_idx)

    def draw_handles(self, rect):
        x1,y1,x2,y2 = rect
        handles = [
            (x1, y1),  # Top-left
            ((x1+x2)//2, y1),  # Top-center
            (x2, y1),  # Top-right
            (x2, (y1+y2)//2),  # Middle-right
            (x2, y2),  # Bottom-right
            ((x1+x2)//2, y2),  # Bottom-center
            (x1, y2),  # Bottom-left
            (x1, (y1+y2)//2)  # Middle-left
        ]
        
        for hx,hy in handles:
            self.canvas.create_rectangle(
                hx-self.HANDLE_SIZE, hy-self.HANDLE_SIZE,
                hx+self.HANDLE_SIZE, hy+self.HANDLE_SIZE,
                fill='white', outline=self.ACCENT_COLOR, width=2, tags='rect'
            )

    def on_mouse_down(self, event):
        x, y = event.x, event.y
        
        # Check if we're resizing a handle
        if self.selected_idx is not None:
            rect = self.rectangles[self.selected_idx]
            handles = self.get_handles(rect)
            
            for i, (hx, hy) in enumerate(handles):
                if abs(x-hx) <= self.HANDLE_SIZE and abs(y-hy) <= self.HANDLE_SIZE:
                    self.resizing = True
                    self.handle_idx = i
                    self.start_x, self.start_y = x, y
                    self.orig_rect = rect
                    return
        
        # Check if we're dragging an existing rectangle
        for i, (x1, y1, x2, y2) in enumerate(self.rectangles):
            if x1 <= x <= x2 and y1 <= y <= y2:
                self.selected_idx = i
                self.dragging = True
                self.start_x, self.start_y = x, y
                self.orig_rect = self.rectangles[i]
                self.draw_rectangles()
                return
        
        # Otherwise, start drawing a new rectangle
        self.selected_idx = None
        self.drawing = True
        self.start_x, self.start_y = x, y
        self._snapshot()

    def get_handles(self, rect):
        x1, y1, x2, y2 = rect
        return [
            (x1, y1),  # Top-left
            ((x1+x2)//2, y1),  # Top-center
            (x2, y1),  # Top-right
            (x2, (y1+y2)//2),  # Middle-right
            (x2, y2),  # Bottom-right
            ((x1+x2)//2, y2),  # Bottom-center
            (x1, y2),  # Bottom-left
            (x1, (y1+y2)//2)  # Middle-left
        ]

    def on_mouse_drag(self, event):
        x, y = event.x, event.y
        
        if self.drawing:
            self.display_frame(self.frame)
            self.canvas.create_rectangle(
                self.start_x, self.start_y, x, y, 
                outline=self.ACCENT_COLOR, width=2, dash=(5,1), tags='rect'
            )
        elif self.resizing:
            x1, y1, x2, y2 = self.rectangles[self.selected_idx]
            coords = [x1, y1, x2, y2]
            
            # Determine which edges to move based on handle
            if self.handle_idx == 0:  # Top-left
                coords[0], coords[1] = x, y
            elif self.handle_idx == 1:  # Top-center
                coords[1] = y
            elif self.handle_idx == 2:  # Top-right
                coords[2], coords[1] = x, y
            elif self.handle_idx == 3:  # Middle-right
                coords[2] = x
            elif self.handle_idx == 4:  # Bottom-right
                coords[2], coords[3] = x, y
            elif self.handle_idx == 5:  # Bottom-center
                coords[3] = y
            elif self.handle_idx == 6:  # Bottom-left
                coords[0], coords[3] = x, y
            elif self.handle_idx == 7:  # Middle-left
                coords[0] = x
                
            self.rectangles[self.selected_idx] = tuple(coords)
            self.draw_rectangles()
        elif self.dragging:
            dx, dy = x - self.start_x, y - self.start_y
            x1, y1, x2, y2 = self.orig_rect
            self.rectangles[self.selected_idx] = (x1+dx, y1+dy, x2+dx, y2+dy)
            self.draw_rectangles()

    def on_mouse_up(self, event):
        if self.drawing:
            x, y = event.x, event.y
            # Only add if it's a meaningful rectangle (not just a click)
            if abs(x - self.start_x) > 10 and abs(y - self.start_y) > 10:
                self.rectangles.append((self.start_x, self.start_y, x, y))
                self.selected_idx = len(self.rectangles) - 1
            self.drawing = False
            self.draw_rectangles()
        else:
            self.resizing = self.dragging = False

    def on_mask_select(self, event):
        selection = self.mask_list.curselection()
        if selection:
            self.selected_idx = selection[0]
            self.draw_rectangles()

    def _snapshot(self):
        self.undo_stack.append(list(self.rectangles))
        self.redo_stack.clear()

    def undo(self, event=None):
        if not self.undo_stack: 
            return
            
        self.redo_stack.append(list(self.rectangles))
        self.rectangles = self.undo_stack.pop()
        self.selected_idx = None
        self.draw_rectangles()

    def redo(self, event=None):
        if not self.redo_stack: 
            return
            
        self.undo_stack.append(list(self.rectangles))
        self.rectangles = self.redo_stack.pop()
        self.selected_idx = None
        self.draw_rectangles()

    def delete_selected(self):
        if self.selected_idx is not None:
            self._snapshot()
            self.rectangles.pop(self.selected_idx)
            self.selected_idx = None
            self.draw_rectangles()

    def clear_all(self):
        if self.rectangles:
            self._snapshot()
            self.rectangles = []
            self.selected_idx = None
            self.draw_rectangles()

    def remove_text(self):
        if not self.cap:
            messagebox.showerror('Error', 'Please load a video first')
            return
            
        if not self.rectangles:
            messagebox.showerror('Error', 'Please select text regions to remove')
            return
            
        out = filedialog.asksaveasfilename(
            defaultextension='.mp4',
            filetypes=[('MP4', '*.mp4'), ('AVI', '*.avi'), ('MOV', '*.mov')]
        )
        if not out: 
            return
            
        self.log_msg('Starting inpainting process...')
        threading.Thread(
            target=self._remove_worker,
            args=(out,),
            daemon=True
        ).start()

    def _remove_worker(self, out_path):
        cap = cv2.VideoCapture(self.video_path)
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Get canvas dimensions for coordinate conversion
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(out_path, fourcc, fps, (w, h))
        
        for i in range(total):
            if self.cancel_requested: 
                break
                
            ret, frame = cap.read()
            if not ret: 
                break
                
            # Create mask
            mask = np.zeros(frame.shape[:2], dtype=np.uint8)
            
            for x1, y1, x2, y2 in self.rectangles:
                # Convert canvas coordinates to video coordinates
                xx1 = int(x1 * w / canvas_w)
                xx2 = int(x2 * w / canvas_w)
                yy1 = int(y1 * h / canvas_h)
                yy2 = int(y2 * h / canvas_h)
                
                mask[yy1:yy2, xx1:xx2] = 255
                
            # Inpaint the masked areas
            res = cv2.inpaint(frame, mask, 3, cv2.INPAINT_TELEA)
            out.write(res)
            
            # Update progress
            pct = (i+1)/total*100
            self.progress_var.set(pct)
            self.progress_label.config(text=f'{int(pct)}%')
            self.root.update()
            
        cap.release()
        out.release()
        
        if self.cancel_requested:
            self.log_msg('Processing cancelled by user')
        else:
            self.log_msg(f'Processing complete. Saved to: {out_path}')
            messagebox.showinfo('Success', 'Video processing completed successfully')

    def cancel_processing(self):
        self.cancel_requested = True
        self.log_msg('Cancelling... Please wait')

if __name__ == '__main__':
    root = tk.Tk()
    app = VideoTextRemover(root)
    root.mainloop()