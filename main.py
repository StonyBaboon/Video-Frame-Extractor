import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
import os
import random
import threading
import json


class VideoFrameExtractor:

    def __init__(self, root):

        self.root = root

        self.video_path = ""
        self.output_folder = ""
        self.stop_requested = False

        self.languages = {}
        self.language_names = {}

        self.language = "pt"
        self.t = {}

        self.load_languages()

        self.create_interface()

        self.set_language(self.language)


    # =========================================================
    # LANGUAGES
    # =========================================================

    def load_languages(self):

        languages_folder = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "languages"
        )

        if not os.path.exists(languages_folder):
            os.makedirs(languages_folder)

        for filename in os.listdir(languages_folder):

            if not filename.endswith(".json"):
                continue

            language_code = filename[:-5]

            path = os.path.join(
                languages_folder,
                filename
            )

            try:

                with open(
                    path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    data = json.load(file)

                self.languages[language_code] = data

                self.language_names[
                    language_code
                ] = data.get(
                    "_language_name",
                    language_code
                )

            except Exception as e:

                print(
                    f"Erro ao carregar {filename}: {e}"
                )

        if "pt" not in self.languages:

            messagebox.showerror(
                "Erro",
                "O ficheiro languages/pt.json não foi encontrado."
            )

            self.languages["pt"] = {}

        self.t = self.languages.get(
            self.language,
            self.languages["pt"]
        )


    def tr(self, key, **kwargs):

        text = self.t.get(
            key,
            key
        )

        if kwargs:

            try:
                text = text.format(**kwargs)

            except Exception:
                pass

        return text


    # =========================================================
    # INTERFACE
    # =========================================================

    def create_interface(self):

        self.root.geometry("700x650")
        self.root.resizable(False, False)

        # =====================================================
        # TOPO / IDIOMA
        # =====================================================

        self.top_frame = ttk.Frame(
            self.root,
            padding=(15, 10)
        )

        self.top_frame.pack(
            fill="x"
        )

        self.language_label = ttk.Label(
            self.top_frame
        )

        self.language_label.pack(
            side="left"
        )

        self.language_var = tk.StringVar()

        self.language_combo = ttk.Combobox(
            self.top_frame,
            textvariable=self.language_var,
            state="readonly",
            width=20
        )

        self.language_combo.pack(
            side="left",
            padx=10
        )

        self.language_combo.bind(
            "<<ComboboxSelected>>",
            self.language_changed
        )


        # =====================================================
        # VÍDEO
        # =====================================================

        self.video_frame = ttk.LabelFrame(
            self.root,
            padding=10
        )

        self.video_frame.pack(
            fill="x",
            padx=15,
            pady=5
        )

        self.video_label = ttk.Label(
            self.video_frame
        )

        self.video_label.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.video_button = ttk.Button(
            self.video_frame,
            command=self.select_video
        )

        self.video_button.pack(
            side="right"
        )


        # =====================================================
        # DESTINO
        # =====================================================

        self.output_frame = ttk.LabelFrame(
            self.root,
            padding=10
        )

        self.output_frame.pack(
            fill="x",
            padx=15,
            pady=5
        )

        self.output_label = ttk.Label(
            self.output_frame
        )

        self.output_label.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.output_button = ttk.Button(
            self.output_frame,
            command=self.select_output
        )

        self.output_button.pack(
            side="right"
        )


        # =====================================================
        # INFORMAÇÕES
        # =====================================================

        self.info_frame = ttk.LabelFrame(
            self.root,
            padding=10
        )

        self.info_frame.pack(
            fill="x",
            padx=15,
            pady=5
        )

        self.info_label = ttk.Label(
            self.info_frame
        )

        self.info_label.pack(
            anchor="w"
        )


        # =====================================================
        # CONFIGURAÇÃO
        # =====================================================

        self.settings_frame = ttk.LabelFrame(
            self.root,
            padding=10
        )

        self.settings_frame.pack(
            fill="x",
            padx=15,
            pady=5
        )


        # Intervalo

        self.interval_label = ttk.Label(
            self.settings_frame
        )

        self.interval_label.grid(
            row=0,
            column=0,
            sticky="w",
            pady=5
        )

        self.interval_var = tk.StringVar(
            value="2"
        )

        self.interval_entry = ttk.Entry(
            self.settings_frame,
            textvariable=self.interval_var,
            width=10
        )

        self.interval_entry.grid(
            row=0,
            column=1,
            sticky="w",
            padx=10
        )


        # Modo

        self.mode_label = ttk.Label(
            self.settings_frame
        )

        self.mode_label.grid(
            row=1,
            column=0,
            sticky="w",
            pady=5
        )

        self.mode_var = tk.StringVar(
            value="random"
        )

        self.random_radio = ttk.Radiobutton(
            self.settings_frame,
            variable=self.mode_var,
            value="random",
            command=self.update_mode
        )

        self.random_radio.grid(
            row=1,
            column=1,
            sticky="w"
        )

        self.specific_radio = ttk.Radiobutton(
            self.settings_frame,
            variable=self.mode_var,
            value="specific",
            command=self.update_mode
        )

        self.specific_radio.grid(
            row=2,
            column=1,
            sticky="w"
        )


        # Frame específico

        self.frame_label = ttk.Label(
            self.settings_frame
        )

        self.frame_label.grid(
            row=3,
            column=0,
            sticky="w",
            pady=5
        )

        self.frame_var = tk.StringVar(
            value="0"
        )

        self.frame_entry = ttk.Entry(
            self.settings_frame,
            textvariable=self.frame_var,
            width=10
        )

        self.frame_entry.grid(
            row=3,
            column=1,
            sticky="w",
            padx=10
        )


        # Quantidade

        self.quantity_label = ttk.Label(
            self.settings_frame
        )

        self.quantity_label.grid(
            row=4,
            column=0,
            sticky="w",
            pady=5
        )

        self.quantity_var = tk.StringVar()

        self.quantity_combo = ttk.Combobox(
            self.settings_frame,
            textvariable=self.quantity_var,
            state="readonly",
            width=15
        )

        self.quantity_combo.grid(
            row=4,
            column=1,
            sticky="w",
            padx=10
        )

        self.quantity_combo.bind(
            "<<ComboboxSelected>>",
            self.quantity_changed
        )

        self.custom_quantity_var = tk.StringVar(
            value="100"
        )

        self.custom_quantity_entry = ttk.Entry(
            self.settings_frame,
            textvariable=self.custom_quantity_var,
            width=10
        )

        self.custom_quantity_entry.grid(
            row=4,
            column=2,
            padx=5
        )


        # =====================================================
        # PROGRESSO
        # =====================================================

        self.progress_frame = ttk.LabelFrame(
            self.root,
            padding=10
        )

        self.progress_frame.pack(
            fill="x",
            padx=15,
            pady=10
        )

        self.progress = ttk.Progressbar(
            self.progress_frame,
            orient="horizontal",
            length=630,
            mode="determinate"
        )

        self.progress.pack()

        self.status_label = ttk.Label(
            self.progress_frame
        )

        self.status_label.pack(
            anchor="w",
            pady=5
        )


        # =====================================================
        # BOTÕES
        # =====================================================

        self.button_frame = ttk.Frame(
            self.root
        )

        self.button_frame.pack(
            pady=10
        )

        self.start_button = ttk.Button(
            self.button_frame,
            command=self.start_extraction
        )

        self.start_button.pack(
            side="left",
            padx=5
        )

        self.stop_button = ttk.Button(
            self.button_frame,
            command=self.stop_extraction,
            state="disabled"
        )

        self.stop_button.pack(
            side="left",
            padx=5
        )


    # =========================================================
    # ALTERAR IDIOMA
    # =========================================================

    def language_changed(self, event=None):

        selected_name = self.language_var.get()

        for code, name in self.language_names.items():

            if name == selected_name:

                self.set_language(code)
                break


    def set_language(self, language_code):

        if language_code not in self.languages:
            return

        self.language = language_code

        self.t = self.languages[
            language_code
        ]

        self.update_interface_text()


    def update_interface_text(self):

        self.root.title(
            self.tr("app_title")
        )

        # Idioma

        self.language_label.config(
            text=self.tr("language") + ":"
        )

        language_values = [
            self.language_names[code]
            for code in self.languages
        ]

        self.language_combo["values"] = (
            language_values
        )

        self.language_var.set(
            self.language_names.get(
                self.language,
                self.language
            )
        )


        # Vídeo

        self.video_frame.config(
            text=self.tr("video")
        )

        self.video_button.config(
            text=self.tr("select_video")
        )

        if not self.video_path:

            self.video_label.config(
                text=self.tr("no_video")
            )


        # Destino

        self.output_frame.config(
            text=self.tr("destination")
        )

        self.output_button.config(
            text=self.tr("select_folder")
        )

        if not self.output_folder:

            self.output_label.config(
                text=self.tr("no_folder")
            )


        # Informação

        self.info_frame.config(
            text=self.tr("information")
        )

        if not self.video_path:

            self.info_label.config(
                text=self.tr("select_video_info")
            )


        # Configuração

        self.settings_frame.config(
            text=self.tr("configuration")
        )

        self.interval_label.config(
            text=self.tr("interval")
        )

        self.mode_label.config(
            text=self.tr("mode")
        )

        self.random_radio.config(
            text=self.tr("random_frame")
        )

        self.specific_radio.config(
            text=self.tr("specific_frame")
        )

        self.frame_label.config(
            text=self.tr("frame_inside_interval")
        )

        self.quantity_label.config(
            text=self.tr("quantity")
        )


        # Quantidade

        current_quantity = self.quantity_var.get()

        self.quantity_combo["values"] = [
            self.tr("all"),
            self.tr("custom")
        ]

        if current_quantity:
            pass
        else:
            self.quantity_var.set(
                self.tr("all")
            )


        # Progresso

        self.progress_frame.config(
            text=self.tr("progress")
        )

        if not self.stop_requested:

            self.status_label.config(
                text=self.tr("ready")
            )


        # Botões

        self.start_button.config(
            text=self.tr("start")
        )

        self.stop_button.config(
            text=self.tr("stop")


        )


    # =========================================================
    # SELECIONAR VÍDEO
    # =========================================================

    def select_video(self):

        path = filedialog.askopenfilename(
            title=self.tr("select_video"),
            filetypes=[
                (
                    "Videos",
                    "*.mp4 *.avi *.mkv *.mov *.webm"
                ),
                (
                    "All files",
                    "*.*"
                )
            ]
        )

        if not path:
            return

        self.video_path = path

        self.video_label.config(
            text=os.path.basename(path)
        )

        self.load_video_info()


    # =========================================================
    # INFORMAÇÕES DO VÍDEO
    # =========================================================

    def load_video_info(self):

        cap = cv2.VideoCapture(
            self.video_path
        )

        if not cap.isOpened():

            messagebox.showerror(
                self.tr("error"),
                self.tr("cannot_open_video")
            )

            return

        fps = cap.get(
            cv2.CAP_PROP_FPS
        )

        total_frames = int(
            cap.get(
                cv2.CAP_PROP_FRAME_COUNT
            )
        )

        width = int(
            cap.get(
                cv2.CAP_PROP_FRAME_WIDTH
            )
        )

        height = int(
            cap.get(
                cv2.CAP_PROP_FRAME_HEIGHT
            )
        )

        duration = (
            total_frames / fps
            if fps > 0
            else 0
        )

        minutes = int(
            duration // 60
        )

        seconds = int(
            duration % 60
        )

        duration_text = (
            f"{minutes:02d}:{seconds:02d}"
        )

        self.info_label.config(
            text=self.tr(
                "video_info",
                fps=fps,
                frames=total_frames,
                width=width,
                height=height,
                duration=duration_text
            )
        )

        cap.release()


    # =========================================================
    # SELECIONAR DESTINO
    # =========================================================

    def select_output(self):

        folder = filedialog.askdirectory(
            title=self.tr("select_folder")
        )

        if not folder:
            return

        self.output_folder = folder

        self.output_label.config(
            text=folder
        )


    # =========================================================
    # MODO
    # =========================================================

    def update_mode(self):

        if self.mode_var.get() == "random":

            self.frame_entry.config(
                state="disabled"
            )

        else:

            self.frame_entry.config(
                state="normal"
            )


    # =========================================================
    # QUANTIDADE
    # =========================================================

    def quantity_changed(self, event=None):

        if self.quantity_var.get() == self.tr("custom"):

            self.custom_quantity_entry.config(
                state="normal"
            )

        else:

            self.custom_quantity_entry.config(
                state="disabled"
            )


    # =========================================================
    # INICIAR EXTRAÇÃO
    # =========================================================

    def start_extraction(self):

        if not self.video_path:

            messagebox.showwarning(
                self.tr("warning"),
                self.tr("select_video_first")
            )

            return


        if not self.output_folder:

            messagebox.showwarning(
                self.tr("warning"),
                self.tr("select_folder_first")
            )

            return


        try:

            interval = float(
                self.interval_var.get()
            )

            if interval <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                self.tr("error"),
                self.tr("invalid_interval")
            )

            return


        if self.mode_var.get() == "specific":

            try:

                frame_number = int(
                    self.frame_var.get()
                )

                if frame_number < 0:
                    raise ValueError

            except ValueError:

                messagebox.showerror(
                    self.tr("error"),
                    self.tr("invalid_frame")
                )

                return


        if self.quantity_var.get() == self.tr("custom"):

            try:

                quantity = int(
                    self.custom_quantity_var.get()
                )

                if quantity <= 0:
                    raise ValueError

            except ValueError:

                messagebox.showerror(
                    self.tr("error"),
                    self.tr("invalid_quantity")
                )

                return


        self.stop_requested = False

        self.start_button.config(
            state="disabled"
        )

        self.stop_button.config(
            state="normal"
        )

        thread = threading.Thread(
            target=self.extract_frames,
            daemon=True
        )

        thread.start()


    # =========================================================
    # EXTRAÇÃO
    # =========================================================

    def extract_frames(self):

        try:

            interval = float(
                self.interval_var.get()
            )

            cap = cv2.VideoCapture(
                self.video_path
            )

            if not cap.isOpened():

                self.root.after(
                    0,
                    self.show_error,
                    self.tr("cannot_open_video")
                )

                return


            fps = cap.get(
                cv2.CAP_PROP_FPS
            )

            total_frames = int(
                cap.get(
                    cv2.CAP_PROP_FRAME_COUNT
                )
            )

            if fps <= 0:

                cap.release()

                self.root.after(
                    0,
                    self.show_error,
                    self.tr("cannot_open_video")
                )

                return


            duration = (
                total_frames / fps
            )

            total_intervals = int(
                duration / interval
            )


            # Quantidade

            if self.quantity_var.get() == self.tr("all"):

                max_frames = total_intervals

            else:

                max_frames = min(
                    total_intervals,
                    int(
                        self.custom_quantity_var.get()
                    )
                )


            saved = 0


            # =================================================
            # PERCORRER INTERVALOS
            # =================================================

            for interval_index in range(
                max_frames
            ):

                if self.stop_requested:
                    break


                start_time = (
                    interval_index * interval
                )

                end_time = min(
                    start_time + interval,
                    duration
                )


                start_frame = int(
                    start_time * fps
                )

                end_frame = int(
                    end_time * fps
                ) - 1


                if end_frame < start_frame:
                    continue


                # =============================================
                # FRAME ALEATÓRIO
                # =============================================

                if self.mode_var.get() == "random":

                    selected_frame = random.randint(
                        start_frame,
                        end_frame
                    )


                # =============================================
                # FRAME ESPECÍFICO
                # =============================================

                else:

                    relative_frame = int(
                        self.frame_var.get()
                    )

                    selected_frame = (
                        start_frame +
                        relative_frame
                    )

                    if selected_frame > end_frame:

                        selected_frame = end_frame


                # =============================================
                # LER FRAME
                # =============================================

                cap.set(
                    cv2.CAP_PROP_POS_FRAMES,
                    selected_frame
                )

                success, frame = cap.read()


                if not success:
                    continue


                # =============================================
                # GUARDAR
                # =============================================

                filename = os.path.join(
                    self.output_folder,
                    f"frame_{saved + 1:06d}.jpg"
                )

                cv2.imwrite(
                    filename,
                    frame,
                    [
                        cv2.IMWRITE_JPEG_QUALITY,
                        95
                    ]
                )


                saved += 1


                # =============================================
                # PROGRESSO
                # =============================================

                progress = (
                    saved / max_frames
                ) * 100


                self.root.after(
                    0,
                    self.update_progress,
                    progress,
                    saved,
                    max_frames
                )


            cap.release()


            self.root.after(
                0,
                self.extraction_finished,
                saved
            )


        except Exception as e:

            self.root.after(
                0,
                self.show_error,
                str(e)
            )


    # =========================================================
    # PROGRESSO
    # =========================================================

    def update_progress(
        self,
        progress,
        saved,
        total
    ):

        self.progress["value"] = progress

        self.status_label.config(
            text=self.tr(
                "frames_extracted",
                current=saved,
                total=total
            )
        )


    # =========================================================
    # PARAR
    # =========================================================

    def stop_extraction(self):

        self.stop_requested = True

        self.status_label.config(
            text=self.tr("stopping")
        )


    # =========================================================
    # TERMINOU
    # =========================================================

    def extraction_finished(self, saved):

        self.start_button.config(
            state="normal"
        )

        self.stop_button.config(
            state="disabled"
        )


        if self.stop_requested:

            self.status_label.config(
                text=self.tr(
                    "stopped",
                    count=saved
                )
            )

        else:

            self.progress["value"] = 100

            self.status_label.config(
                text=self.tr(
                    "finished",
                    count=saved
                )
            )

            messagebox.showinfo(
                self.tr("success"),
                self.tr(
                    "finished",
                    count=saved
                )
            )


    # =========================================================
    # ERRO
    # =========================================================

    def show_error(self, message):

        self.start_button.config(
            state="normal"
        )

        self.stop_button.config(
            state="disabled"
        )

        messagebox.showerror(
            self.tr("error"),
            message
        )


# =============================================================
# MAIN
# =============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = VideoFrameExtractor(root)

    root.mainloop()