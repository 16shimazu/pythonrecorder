import os, cv2, threading
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
save_dir = os.path.expanduser(r'~\Documents\pythonrecorder')
os.makedirs(save_dir, exist_ok=True)
class WebcamRecorderApp:
    def __init__(self, root):
        self.root = root;self.root.title("Webcam Recorder");self.cap = cv2.VideoCapture(0);self.is_recording = False;self.video_writer = None;self.video_label = tk.Label(root);self.video_label.pack();self.record_button = tk.Button(root, text="Start Recording", command=self.toggle_recording);self.record_button.pack();self.update_frame()
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB);img = ImageTk.PhotoImage(Image.fromarray(frame));self.video_label.imgtk = img;self.video_label.configure(image=img)
            if self.is_recording and self.video_writer: self.video_writer.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        self.root.after(10, self.update_frame)
    def toggle_recording(self):
        if self.is_recording: self.stop_recording()
        else: self.start_recording()
    def start_recording(self):
        filename = os.path.join(save_dir, f'recording_{cv2.getTickCount()}.mp4');fourcc = cv2.VideoWriter_fourcc(*'mp4v');frame_width = int(self.cap.get(3));frame_height = int(self.cap.get(4));self.video_writer = cv2.VideoWriter(filename, fourcc, 20.0, (frame_width, frame_height));self.is_recording = True;self.record_button.config(text="Stop Recording");messagebox.showinfo("Recording Started", f"Recording started. Saving to {filename}")
    def stop_recording(self):
        self.is_recording = False;self.record_button.config(text="Start Recording")
        if self.video_writer: self.video_writer.release();self.video_writer = None
        messagebox.showinfo("Recording Stopped", "Recording stopped.")
    def on_closing(self):
        self.cap.release()
        if self.video_writer: self.video_writer.release()
        self.root.destroy()
root = tk.Tk()
app = WebcamRecorderApp(root)
root.protocol("WM_DELETE_WINDOW", app.on_closing)
root.mainloop()
