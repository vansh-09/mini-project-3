import os
from pathlib import Path
from typing import Dict
from backend.config import AUDIO_DIR

class TTSService:
    def synthesize_bilingual(self, text_en: str, text_hi: str, event_id: str) -> Dict[str, str]:
        """
        Synthesizes English and Hindi text into MP3 audio files.
        Returns relative audio URLs:
        {
           "audio_en": "/storage/audio/ad_001_en.mp3",
           "audio_hi": "/storage/audio/ad_001_hi.mp3"
        }
        """
        out_en_filename = f"{event_id}_en.mp3"
        out_hi_filename = f"{event_id}_hi.mp3"

        out_en_path = AUDIO_DIR / out_en_filename
        out_hi_path = AUDIO_DIR / out_hi_filename

        self.synthesize_text(text_en, str(out_en_path), lang="en")
        self.synthesize_text(text_hi, str(out_hi_path), lang="hi")

        return {
            "audio_en": f"/storage/audio/{out_en_filename}",
            "audio_hi": f"/storage/audio/{out_hi_filename}"
        }

    def synthesize_text(self, text: str, output_path: str, lang: str = "en") -> str:
        abs_output_path = str(Path(output_path).resolve())

        # Primary engine: gTTS (Google Text-to-Speech)
        try:
            from gtts import gTTS
            tts_lang = "hi" if lang in ["hi", "hindi"] else "en"
            tts = gTTS(text=text, lang=tts_lang)
            tts.save(abs_output_path)
            return abs_output_path
        except Exception as e:
            print(f"gTTS error ({lang}): {e}. Attempting pyttsx3 fallback...")

        # Fallback engine: pyttsx3 (offline)
        try:
            import pyttsx3
            engine = pyttsx3.init()
            fallback_path = abs_output_path if abs_output_path.endswith(".mp3") else abs_output_path + ".mp3"
            engine.save_to_file(text, fallback_path)
            engine.runAndWait()
            return fallback_path
        except Exception as pyttsx3_err:
            print(f"pyttsx3 fallback error: {pyttsx3_err}")
            # Ensure dummy audio file exists if both fail so web app doesn't 404
            with open(abs_output_path, "wb") as f:
                f.write(b"AUDIO_DATA_PLACEHOLDER")
            return abs_output_path
