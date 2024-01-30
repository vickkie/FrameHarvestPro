# PRODUCT OF TRAKEXCEL AGENCY 2024. COPYRIGHT TERMS APPLIES
import cv2
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import sys


class VideoToFramesConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Video to Frames Pictures Converter")

        # Set custom icon
        icon_path = 'vid.ico'  # Replace with the path to your .ico file
        if getattr(sys, 'frozen', False):  # Check if running as a PyInstaller executable
            icon_path = os.path.join(sys._MEIPASS, "vid.ico")

        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)

        # Icon definitions
        self.browse_icon = tk.PhotoImage(file="folder.png" if not getattr(
            sys, 'frozen', False) else os.path.join(sys._MEIPASS, "folder.png"))
        self.cancel_icon = tk.PhotoImage(file="cancel.png" if not getattr(
            sys, 'frozen', False) else os.path.join(sys._MEIPASS, "cancel.png"))
        self.convert_icon = tk.PhotoImage(file="convert.png" if not getattr(
            sys, 'frozen', False) else os.path.join(sys._MEIPASS, "convert.png"))
        self.open_folder_icon = tk.PhotoImage(file="open-folder.png" if not getattr(
            sys, 'frozen', False) else os.path.join(sys._MEIPASS, "open-folder.png"))

        self.create_widgets()
        self.cancel_conversion = False

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Page 1: Conversion functionality
        conversion_page = ttk.Frame(self.notebook)
        self.notebook.add(conversion_page, text="Convert Video")

        self.create_conversion_widgets(conversion_page)

        # Page 2: About the program
        about_page = ttk.Frame(self.notebook)
        self.notebook.add(about_page, text="About")

        about_label = ttk.Label(
            about_page, text="Video to Frames Converter\nVersion 1.0\n© 2024 Trakexcel Agency-@Uzitrake")
        about_label.pack(padx=20, pady=14)

        explanation_text = (
            "This program allows you to convert a video file into a sequence of frames.\n\n"
            "Usage:\n"
            "1. Select a video file using the 'Browse' button.\n"
            "2. Choose an output directory where the frames will be saved.\n"
            "3. Select the output format (WebP, JPEG, PNG) from the dropdown menu.\n"
            "4. Set the quality of the images (0-100).\n"
            "5. Click 'Convert' to start the conversion process.\n"
            "6. Optionally, you can cancel the conversion using the 'Cancel' button.\n"
            "7. Once the conversion is done, use 'Open in Explorer'."
        )

        explanation_label = ttk.Label(
            about_page, text=explanation_text, anchor="w", justify="left")
        explanation_label.pack(padx=20, pady=20, fill="both")

        # Allow window expansion
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def create_conversion_widgets(self, parent):
        # Video file selection
        self.file_frame = ttk.Frame(parent, padding="10 5 10 5")
        self.file_frame.grid(row=0, column=0, sticky="ew")

        self.file_path_label = ttk.Label(
            self.file_frame, text="Video To Convert:")
        self.file_path_label.grid(row=0, column=0, sticky="w")

        self.file_path_entry = ttk.Entry(
            self.file_frame, state="disabled", width=40, font=("Helvetica", 10))
        self.file_path_entry.grid(row=0, column=1, padx=(0, 10), sticky="ew")

        self.browse_button = ttk.Button(
            self.file_frame, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=2)

        # Output directory selection
        self.output_frame = ttk.Frame(parent, padding="10 5 10 5")
        self.output_frame.grid(row=1, column=0, sticky="ew")

        self.output_path_label = ttk.Label(
            self.output_frame, text="Output Location:", font=("Helvetica", 10))
        self.output_path_label.grid(row=0, column=0, sticky="w")

        self.output_path_entry = ttk.Entry(
            self.output_frame, state="disabled", width=40, font=("Helvetica", 10))
        self.output_path_entry.grid(row=0, column=1, padx=(0, 10), sticky="ew")

        self.output_browse_button = ttk.Button(
            self.output_frame, text="Browse", command=self.browse_output_directory)
        self.output_browse_button.grid(row=0, column=2)

        # Output format selection
        self.format_frame = ttk.Frame(parent, padding="10 5 10 5")
        self.format_frame.grid(row=2, column=0, sticky="ew")

        self.format_label = ttk.Label(
            self.format_frame, text="Output Format:", font=("Helvetica", 10))
        self.format_label.grid(row=0, column=0, sticky="w")

        self.format_var = tk.StringVar()
        self.format_var.set("WebP")  # Default format
        self.format_dropdown = ttk.Combobox(self.format_frame, textvariable=self.format_var,
                                            values=["WebP", "JPEG", "PNG"])
        self.format_dropdown.grid(row=0, column=1, padx=(0, 10), sticky="ew")

        # Quality selection
        self.quality_frame = ttk.Frame(parent, padding="10 5 10 5")
        self.quality_frame.grid(row=3, column=0, sticky="ew")

        self.quality_label = ttk.Label(
            self.quality_frame, text="Quality (0-100):", font=("Helvetica", 10))
        self.quality_label.grid(row=0, column=0, sticky="w")

        self.quality_var = tk.StringVar()
        self.quality_var.set("100")
        self.quality_spinbox = ttk.Spinbox(
            self.quality_frame, from_=0, to=100, textvariable=self.quality_var, width=7)
        self.quality_spinbox.grid(row=0, column=1, padx=(0, 10), sticky="ew")

        # Button frame
        self.button_frame = ttk.Frame(parent, padding="10 5 10 5")
        self.button_frame.grid(row=4, column=0, sticky="ew")

        # Convert button
        self.convert_button = ttk.Button(
            self.button_frame, text="Convert", command=self.start_conversion, image=self.convert_icon, compound="left")
        self.convert_button.grid(row=0, column=0, padx=5)

        # Cancel button
        self.cancel_button = ttk.Button(
            self.button_frame, text="Cancel", command=self.cancel_conversion_process, image=self.cancel_icon, compound="left")
        self.cancel_button.grid(row=0, column=1, padx=5)

        # Open in Explorer button
        self.open_folder_button = ttk.Button(self.button_frame, text="Open in Explorer",
                                             command=self.open_output_folder, image=self.open_folder_icon, compound="left")
        self.open_folder_button.grid(row=0, column=2, padx=5)

        # Info label
        info_label = ttk.Label(
            parent, text="ℹ️ Check chosen directory for images", font="Helvetica 8 italic")
        info_label.grid(row=5, column=0, pady=5)

        # Conversion status labels
        self.status_label = ttk.Label(parent, text="")
        self.status_label.grid(row=6, column=0, pady=5)

        # Progress bar style
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("green.Horizontal.TProgressbar",
                        troughcolor='black', barcolor='green')

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            parent, variable=self.progress_var, mode="determinate", style="green.Horizontal.TProgressbar")
        self.progress_bar.grid(row=7, column=0, sticky="ew", pady=5)

    def browse_file(self):
        file_path = filedialog.askopenfilename(title="Select a video file", filetypes=[
                                               ("Video Files", "*.mp4;*.avi")])
        self.file_path_entry.config(state="normal")
        self.file_path_entry.delete(0, tk.END)
        self.file_path_entry.insert(tk.END, file_path)
        self.file_path_entry.config(state="disabled")

    def browse_output_directory(self):
        output_directory = filedialog.askdirectory(
            title="Select an output directory")
        self.output_path_entry.config(state="normal")
        self.output_path_entry.delete(0, tk.END)
        self.output_path_entry.insert(tk.END, output_directory)
        self.output_path_entry.config(state="disabled")

        # Call open_output_folder to update the output_directory variable
        # self.open_output_folder()
        # CODE BY UZITRAKE

    def start_conversion(self):
        self.cancel_conversion = False
        self.status_label.config(text="Converting...")
        self.progress_var.set(0)  # Reset progress bar
        # Delayed call to start conversion
        self.root.after(100, self.convert_video_to_frames)

    def cancel_conversion_process(self):
        self.cancel_conversion = True
        self.status_label.config(text="Conversion canceled.")
        self.progress_bar.stop()

    def convert_video_to_frames(self):
        video_path = self.file_path_entry.get()
        output_directory = self.output_path_entry.get()
        quality = int(self.quality_var.get())
        output_format = self.format_var.get()

        if not video_path:
            messagebox.showerror("Error", "Please select a video file.")
            self.reset_conversion_status()
            return

        if not output_directory:
            messagebox.showerror("Error", "Please select an output directory.")
            self.reset_conversion_status()
            return

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        video_capture = cv2.VideoCapture(video_path)
        total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

        frame_count = 0

        def process_frame():
            nonlocal frame_count

            if not self.cancel_conversion:
                ret, frame = video_capture.read()
                if ret:
                    frame_filename = os.path.join(output_directory, f'frame_{
                                                  frame_count:04d}.{output_format.lower()}')

                    if output_format == "AVIF":
                        imageio.imwrite(frame_filename, frame,
                                        format='AVIF', codec='av1')
                    elif output_format == "PNG":
                        cv2.imwrite(frame_filename, frame, [
                                    cv2.IMWRITE_PNG_COMPRESSION, quality])
                    else:
                        cv2.imwrite(frame_filename, frame, [
                                    cv2.IMWRITE_WEBP_QUALITY, quality] if output_format == "WebP" else [])

                    frame_count += 1

                    # Update progress bar
                    progress_value = (frame_count + 1) / total_frames * 100
                    self.progress_var.set(progress_value)
                    self.root.update_idletasks()  # Force update of the GUI

                    # Schedule the next frame processing
                    self.root.after(10, process_frame)
                else:
                    # Release resources and finalize
                    video_capture.release()
                    cv2.destroyAllWindows()

                    if self.cancel_conversion:
                        self.status_label.config(text="Conversion canceled.")
                    else:
                        self.status_label.config(text="Conversion completed.")
                    self.progress_bar.stop()
                    self.reset_conversion_status()

        process_frame()

    def open_output_folder(self):
        output_directory = self.output_path_entry.get()

        if output_directory and os.path.exists(output_directory):
            os.startfile(output_directory)
        else:
            messagebox.showwarning(
                "Warning", "Output directory does not exist.")

    def reset_conversion_status(self):
        self.cancel_conversion = False
        self.status_label.config(text="")
        self.progress_bar.stop()


if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use("clam")
    converter = VideoToFramesConverter(root)
    root.mainloop()
