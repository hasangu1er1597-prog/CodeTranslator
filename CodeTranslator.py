import re
import threading
import tkinter as tk
from tkinter import messagebox, ttk
from deep_translator import GoogleTranslator


SUPPORTED_LANGUAGES = {
    # 1. Major Languages
    "English": "en", "Chinese (Mandarin)": "zh-CN", "Hindi": "hi", "Spanish": "es",
    "French": "fr", "Arabic": "ar", "Bengali": "bn", "Portuguese": "pt",
    "Russian": "ru", "Urdu": "ur", "Indonesian": "id", "German": "de",
    "Japanese": "ja", "Marathi": "mr", "Telugu": "te", "Turkish": "tr",
    "Tamil": "ta", "Cantonese": "zh-TW", "Vietnamese": "vi",
    
    # 2. European Languages
    "Italian": "it", "Polish": "pl", "Ukrainian": "uk", "Romanian": "ro",
    "Dutch": "nl", "Greek": "el", "Hungarian": "hu", "Czech": "cs",
    "Swedish": "sv", "Bulgarian": "bg", "Serbian": "sr", "Croatian": "hr",
    "Slovak": "sk", "Danish": "da", "Finnish": "fi", "Norwegian": "no",
    "Albanian": "sq", "Lithuanian": "lt", "Latvian": "lv", "Slovenian": "sl",
    "Estonian": "et", "Irish": "ga", "Icelandic": "is", "Maltese": "mt",
    "Catalan": "ca", "Basque": "eu", "Galician": "gl", "Welsh": "cy",
    
    # 3. Middle East and Central Asia
    "Persian": "fa", "Azerbaijani": "az", "Pashto": "ps", "Kurdish": "ku",
    "Uzbek": "uz", "Kazakh": "kk", "Turkmen": "tk", "Kyrgyz": "ky",
    "Hebrew": "iw", "Tajik": "tg", "Tatar": "tt", "Uyghur": "ug",
    "Armenian": "hy", "Georgian": "ka",
    
    # 4. Asia (East and South)
    "Korean": "ko", "Thai": "th", "Lao": "lo", "Burmese": "my",
    "Khmer": "km", "Malay": "ms", "Tagalog": "tl", "Javanese": "jw",
    "Sundanese": "su", "Punjabi": "pa", "Gujarati": "gu", "Malayalam": "ml",
    "Kannada": "kn", "Oriya": "or", "Sindhi": "sd", "Sinhala": "si",
    "Nepali": "ne", "Mongolian": "mn", "Tibetan": "bo",
    
    # 5. Africa
    "Swahili": "sw", "Amharic": "am", "Yoruba": "yo", "Igbo": "ig",
    "Hausa": "ha", "Zulu": "zu", "Shona": "sn", "Oromo": "om",
    "Somali": "so", "Berber": "ber", "Afrikaans": "af",
    "Wolof": "wo", "Kinyarwanda": "rw", "Tigrinya": "ti",
    
    # 6. Americas, Oceania, and Others
    "Quechua": "qu", "Guarani": "gn", "Aymara": "ay", "Mayan": "myn",
    "Hawaiian": "haw", "Maori": "mi", "Samoan": "sm", "Latin": "la",
    "Esperanto": "eo", "Sanskrit": "sa"
}

def translate_code_content(code, target_iso, log_widget):
    pattern = r'(["\'].*?["\']|#.*)'
    translator = GoogleTranslator(source='auto', target=target_iso)
    
    log_widget.config(state=tk.NORMAL)
    log_widget.delete("1.0", tk.END)
    log_widget.insert(tk.END, f"Target: {target_iso.upper()}\n{'='*20}\n")

    def replace_logic(match):
        original = match.group(0)
        is_comment = original.startswith('#')
        clean_text = original[1:].strip() if is_comment else original[1:-1].strip()

        if len(clean_text) < 2: return original

        try:
            translated = translator.translate(clean_text)
            if translated:
                log_widget.insert(tk.END, f"✓ {translated[:15]}...\n")
                log_widget.see(tk.END)
                if is_comment: return f"# {translated}"
                else: return f"{original[0]}{translated}{original[0]}"
            return original
        except: return original

    final_code = re.sub(pattern, replace_logic, code)
    log_widget.config(state=tk.DISABLED)
    return final_code

def process_translation():
    target_iso = SUPPORTED_LANGUAGES.get(lang_var.get(), "en")
    input_content = input_text.get("1.0", tk.END).strip()
    
    if not input_content:
        messagebox.showwarning("Warning", "Please paste your code first.")
        return

    translate_button.config(state=tk.DISABLED, text="Translating...")
    progress_bar.start(10)
    
    try:
        result = translate_code_content(input_content, target_iso, log_text)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        translate_button.config(state=tk.NORMAL, text="Translate All ↓")
        progress_bar.stop()

def run_code(widget):
    code = widget.get("1.0", tk.END).strip()
    if not code:
        messagebox.showwarning("Warning", "No code found to execute!")
        return
    try:
        print("\n--- Executing Code ---")
        exec(code)
    except Exception as e:
        messagebox.showerror("Execution Error", f"An error occurred:\n{e}")

def start_thread():
    threading.Thread(target=process_translation, daemon=True).start()

# --- UI DESIGN ---
root = tk.Tk()
root.title("CodeTranslator v4.0 - Dual Execution Mode")
root.geometry("1200x700")
root.configure(bg="#f0f2f5")

# Top Panel
top_panel = tk.Frame(root, bg="#2c3e50", pady=15)
top_panel.pack(fill=tk.X)

lang_var = tk.StringVar(root)
lang_var.set("English")
lang_combo = ttk.Combobox(top_panel, textvariable=lang_var, values=list(SUPPORTED_LANGUAGES.keys()), state="readonly", width=25)
lang_combo.pack(side=tk.LEFT, padx=20)

translate_button = tk.Button(top_panel, text="Translate All ↓", command=start_thread, bg="#3498db", fg="white", font=("Arial", 10, "bold"), relief=tk.FLAT, padx=20)
translate_button.pack(side=tk.LEFT)

progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, mode='indeterminate')
progress_bar.pack(fill=tk.X)

# Main Content Area
main_frame = tk.Frame(root, bg="#f0f2f5")
main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

# LEFT PANEL (Source)
left_container = tk.Frame(main_frame, bg="#f0f2f5")
left_container.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)

input_text = tk.Text(left_container, font=("Consolas", 10), height=25)
input_text.pack(expand=True, fill=tk.BOTH)

btn_run_left = tk.Button(left_container, text="◀ Run Source", command=lambda: run_code(input_text), bg="#95a5a6", fg="white", pady=5, font=("Arial", 9, "bold"))
btn_run_left.pack(fill=tk.X, pady=5)

# MIDDLE PANEL (Logs)
log_text = tk.Text(main_frame, width=20, bg="#1e272e", fg="#00d2d3", font=("Arial", 8), state=tk.DISABLED)
log_text.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=(0, 35))

# RIGHT PANEL (Result)
right_container = tk.Frame(main_frame, bg="#f0f2f5")
right_container.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)

output_text = tk.Text(right_container, font=("Consolas", 10), bg="#1e1e1e", fg="#d4d4d4", height=25)
output_text.pack(expand=True, fill=tk.BOTH)

btn_run_right = tk.Button(right_container, text="Run Result ▶", command=lambda: run_code(output_text), bg="#27ae60", fg="white", pady=5, font=("Arial", 10, "bold"))
btn_run_right.pack(fill=tk.X, pady=5)

root.mainloop()
