import pyttsx3
import re
import time


class TTSReader:
    def __init__(self):
        self.engine = pyttsx3.init()
        self._stop_requested = False
        self._pause_requested = False
        self._paused = False

        # defaults
        self.set_rate(180)
        # keep the current voice
        voices = self.engine.getProperty("voices")
        if voices:
            self.engine.setProperty("voice", voices[0].id)

    # ---------- Settings ----------
    def get_voice_names(self):
        return [v.name for v in self.engine.getProperty("voices")]

    def set_voice_by_name(self, name: str):
        for v in self.engine.getProperty("voices"):
            if v.name == name:
                self.engine.setProperty("voice", v.id)
                return
        # if not found, keep current

    def set_rate(self, rate: int):
        self.engine.setProperty("rate", int(rate))

    # ---------- Controls ----------
    def request_stop(self):
        self._stop_requested = True
        try:
            self.engine.stop()
        except Exception:
            pass

    def request_pause(self):
        # Pause will take effect after the current sentence finishes.
        self._pause_requested = True

    def request_resume(self):
        self._pause_requested = False
        self._paused = False

    # ---------- Reading ----------
    def chunk_text(self, text: str, max_len=300):
        # split by sentence-ish, then further chunk if very long
        sentences = re.split(r'(?<=[\.\!\?])\s+', text.strip())
        chunks = []
        for s in sentences:
            s = s.strip()
            if not s:
                continue
            if len(s) <= max_len:
                chunks.append(s)
            else:
                # split long sentences into smaller chunks
                for i in range(0, len(s), max_len):
                    chunks.append(s[i:i + max_len])
        return chunks

    def read_chunks(self, chunks, start_index=0):
        self._stop_requested = False
        idx = start_index
        while idx < len(chunks) and not self._stop_requested:
            if self._pause_requested:
                self._paused = True
                # wait until resume requested
                while self._paused and not self._stop_requested:
                    time.sleep(0.1)
                if self._stop_requested:
                    break

            utterance = chunks[idx]
            self.engine.say(utterance)
            self.engine.runAndWait()
            idx += 1
