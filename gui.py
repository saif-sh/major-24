# gui.py
import random
import tkinter as tk
from tkinter import messagebox, ttk
import threading
from audio_handler import AudioHandler
from predictor import EmotionPredictor
from config import (
    DEFAULT_RECORDING_DURATION, BG_COLOR, TITLE_COLOR, BUTTON_COLOR, HOVER_COLOR,
    PREDICTION_COLOR, ERROR_COLOR, FOOTER_COLOR
)

class SpeechEmotionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech Emotion Recognition")
        self.root.geometry("700x600")
        self.root.configure(bg=BG_COLOR)

        # Initialize handlers
        self.audio_handler = AudioHandler()
        self.predictor = EmotionPredictor(use_random=True)
        self.recording_duration = DEFAULT_RECORDING_DURATION
        self.is_recording = False

        # Configure Styles
        self.style = ttk.Style()
        self.style.configure("Blue.TButton", background=BUTTON_COLOR, foreground="black", font=("Arial", 12))
        self.style.configure("Red.TButton", background=HOVER_COLOR, foreground="white", font=("Arial", 12))

        # Build UI
        self.build_ui()
    def predict_emotion(self):
        # Simulate emotion prediction
        emotions = ["Happiness", "Sadness", "Anger", "Surprise", "Fear"]
        predicted_emotion = random.choice(emotions)
        messagebox.showinfo("Prediction", f"Predicted emotion: {predicted_emotion}")

    def build_ui(self):
        """Constructs the GUI components."""
        # Title label
        title_label = tk.Label(
            self.root, text="Speech Emotion Recognition",
            font=("Arial", 26, "bold"), bg=BG_COLOR, fg=TITLE_COLOR
        )
        title_label.pack(pady=20)

        # Record button frame
        record_frame = tk.Frame(self.root, bg=BG_COLOR)
        record_frame.pack(pady=30)

        # Canvas for circular record button
        self.canvas = tk.Canvas(record_frame, width=180, height=180, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack()
        self.record_circle = self.canvas.create_oval(10, 10, 170, 170, fill=BUTTON_COLOR)
        self.record_button = ttk.Button(
            record_frame, text="Record", command=self.toggle_recording, style="Blue.TButton"
        )
        self.record_button.place(relx=0.5, rely=0.5, anchor="center", width=100, height=40)

        # Hover effects
        self.record_button.bind("<Enter>", self.on_record_enter)
        self.record_button.bind("<Leave>", self.on_record_leave)

        # Other buttons
        button_frame = tk.Frame(self.root, bg=BG_COLOR)
        button_frame.pack(pady=30)

        playback_button = ttk.Button(
            button_frame, text="Playback", command=self.play_back_audio, style="Blue.TButton"
        )
        playback_button.grid(row=0, column=0, padx=20, pady=10, ipadx=20, ipady=10, sticky="ew")

        predict_button = ttk.Button(
            button_frame, text="Predict", command=self.predict_emotion, style="Blue.TButton"
        )
        predict_button.grid(row=0, column=1, padx=20, pady=10, ipadx=20, ipady=10, sticky="ew")

        clear_button = ttk.Button(
            button_frame, text="Clear Recordings", command=self.clear_recordings, style="Blue.TButton"
        )
        clear_button.grid(row=1, column=0, padx=20, pady=10, ipadx=20, ipady=10, sticky="ew")

        settings_button = ttk.Button(
            button_frame, text="Settings", command=self.open_settings, style="Blue.TButton"
        )
        settings_button.grid(row=1, column=1, padx=20, pady=10, ipadx=20, ipady=10, sticky="ew")

        help_button = ttk.Button(
            button_frame, text="Help", command=self.show_help, style="Blue.TButton"
        )
        help_button.grid(row=2, column=0, columnspan=2, padx=20, pady=10, ipadx=20, ipady=10, sticky="ew")

        # Loading/prediction label
        self.loading_label = tk.Label(
            self.root, text="", font=("Arial", 14), bg=BG_COLOR, fg=TITLE_COLOR
        )
        self.loading_label.pack(pady=20)

        # Exit button
        exit_button = ttk.Button(
            self.root, text="Exit", command=self.root.quit, style="Blue.TButton"
        )
        exit_button.pack(pady=10, padx=10, ipadx=20, ipady=10)

        # Footer
        footer_label = tk.Label(
            self.root, text="Developed by Group 15",
            font=("Arial", 10), bg=BG_COLOR, fg=FOOTER_COLOR
        )
        footer_label.pack(side="bottom", pady=10)

    def on_record_enter(self, event):
        """Changes the button style on hover."""
        if not self.is_recording:
            self.record_button.config(style="Red.TButton")

    def on_record_leave(self, event):
        """Reverts the button style when not hovered."""
        if not self.is_recording:
            self.record_button.config(style="Blue.TButton")

    def toggle_recording(self):
        """Starts or stops recording based on the current state."""
        if not self.is_recording:
            self.start_recording()
        else:
            # Currently, recording stops automatically after duration
            pass

    def start_recording(self):
        """Initiates the recording process."""
        self.is_recording = True
        self.record_button.config(style="Red.TButton")
        self.canvas.itemconfig(self.record_circle, fill=HOVER_COLOR)
        self.loading_label.config(text="Recording...", fg=ERROR_COLOR)
        threading.Thread(target=self.record_audio_thread).start()

    def record_audio_thread(self):
        """Handles audio recording in a separate thread."""
        try:
            self.audio_handler.record_audio(self.recording_duration)
            self.loading_label.config(text="Input Taken", fg=BUTTON_COLOR)
            # Start prediction in a separate thread
            threading.Thread(target=self.process_prediction).start()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to record audio: {str(e)}")
            self.reset_recording_state()

    def process_prediction(self):
        """Processes emotion prediction."""
        try:
            self.loading_label.config(text="Loading...", fg=BUTTON_COLOR)
            emotion = self.predictor.predict_emotion()
            self.loading_label.config(text=f"Emotion Predicted: {emotion}", fg=PREDICTION_COLOR)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to predict emotion: {str(e)}")
        finally:
            self.reset_recording_state()

    def reset_recording_state(self):
        """Resets the recording state and button styles."""
        self.is_recording = False
        self.record_button.config(style="Blue.TButton")
        self.canvas.itemconfig(self.record_circle, fill=BUTTON_COLOR)

    def play_back_audio(self):
        """Plays back the recorded audio."""
        try:
            self.audio_handler.play_back_audio()
        except FileNotFoundError:
            messagebox.showwarning("Warning", "No audio recorded yet.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to play audio: {str(e)}")

    def clear_recordings(self):
        """Clears the recorded audio."""
        try:
            self.audio_handler.clear_recording()
            messagebox.showinfo("Info", "Previous recordings cleared.")
        except FileNotFoundError:
            messagebox.showwarning("Warning", "No recordings to clear.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear recordings: {str(e)}")

    def open_settings(self):
        """Opens the settings window to adjust recording duration."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("300x200")
        settings_window.configure(bg="#ecf0f1")

        def update_duration():
            try:
                duration = int(duration_entry.get())
                if duration <= 0:
                    raise ValueError
                self.recording_duration = duration
                messagebox.showinfo("Info", f"Recording duration updated to {self.recording_duration} seconds.")
                settings_window.destroy()
            except ValueError:
                messagebox.showwarning("Warning", "Please enter a valid positive integer.")

        duration_label = tk.Label(
            settings_window, text="Set Recording Duration (seconds):",
            font=("Arial", 12), bg="#ecf0f1"
        )
        duration_label.pack(pady=10)

        duration_entry = tk.Entry(settings_window, font=("Arial", 12))
        duration_entry.insert(0, str(self.recording_duration))
        duration_entry.pack(pady=5)

        update_button = ttk.Button(settings_window, text="Update", command=update_duration)
        update_button.pack(pady=10)

    def show_help(self):
        """Displays help information."""
        help_text = (
            "To use this application:\n\n"
            "1. Click the 'Record' button to start recording.\n"
            f"   The default recording duration is {self.recording_duration} seconds.\n"
            "2. After recording, the application will predict the emotion.\n"
            "3. Click 'Playback' to listen to your recording.\n"
            "4. Use 'Clear Recordings' to delete previous recordings.\n"
            "5. Adjust the recording duration in the 'Settings'."
        )
        messagebox.showinfo("Help", help_text)
