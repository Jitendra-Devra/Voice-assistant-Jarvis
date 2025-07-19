# gui.py
import customtkinter as ctk
import math

class JarvisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("J.A.R.V.I.S.")
        self.root.geometry("800x600")
        self.root.configure(bg="#101418")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # --- Main Frame ---
        self.main_frame = ctk.CTkFrame(root, corner_radius=15, fg_color="#1C1F23")
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # --- Status Label ---
        self.status_label = ctk.CTkLabel(self.main_frame, text="Initializing Jarvis...", font=("Roboto", 24, "bold"), text_color="#00BFFF")
        self.status_label.pack(pady=20)

        # --- Visualization Canvas ---
        self.canvas = ctk.CTkCanvas(self.main_frame, width=600, height=200, bg="#1C1F23", highlightthickness=0)
        self.canvas.pack(pady=15)
        self.is_listening = False
        self.angle = 0

        # --- Transcription Label ---
        self.transcription_label = ctk.CTkLabel(self.main_frame, text="You said: ...", font=("Roboto", 16), wraplength=700, justify="center")
        self.transcription_label.pack(pady=20, padx=10)

        self.animate()

    def update_status(self, text):
        self.status_label.configure(text=text)

    def update_transcription(self, text):
        self.transcription_label.configure(text=f"You said: \"{text}\"")

    def start_listening_animation(self):
        self.is_listening = True

    def stop_listening_animation(self):
        self.is_listening = False

    def animate(self):
        self.canvas.delete("all")
        if self.is_listening:
            # Pulsing circle animation
            radius = 10 + 5 * (1 + math.sin(self.angle))

            # --- CORRECTED CODE ---
            # This calculation now correctly keeps the blue value between 100 and 255
            blue_intensity = int(177 + 78 * math.sin(self.angle * 0.7))
            color = f'#00BFFF' # Using the theme's accent color for the pulse
            
            # We will vary the size and use a consistent color for a smoother look
            self.canvas.create_oval(300 - radius, 100 - radius, 300 + radius, 100 + radius, fill=color, outline="")
            self.angle += 0.2
        else:
            # Static "Iron Man" Arc Reactor style
            self.canvas.create_oval(250, 50, 350, 150, outline="#00BFFF", width=4)
            for i in range(12):
                rad = i * 30 * (math.pi / 180)
                x1 = 300 + 45 * math.cos(rad)
                y1 = 100 + 45 * math.sin(rad)
                x2 = 300 + 50 * math.cos(rad)
                y2 = 100 + 50 * math.sin(rad)
                self.canvas.create_line(x1, y1, x2, y2, fill="#00BFFF", width=3)
        
        self.root.after(33, self.animate) # ~30 FPS