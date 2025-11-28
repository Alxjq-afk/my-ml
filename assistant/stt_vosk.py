"""VOSK offline STT wrapper for JARVIS."""
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import queue
import json
import os


class VoskSTT:
    """Reconocimiento de voz offline usando VOSK.

    Ejemplo de uso:
        stt = VoskSTT()
        text = stt.listen_and_transcribe(duration=5)
    """

    def __init__(self, model_path=None, sample_rate=16000):
        self.model_path = model_path or os.path.join('assistant_data', 'models', 'vosk-model-small-es-0.22')
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Modelo VOSK no encontrado en: {self.model_path}")
        self.sample_rate = sample_rate
        self.model = Model(self.model_path)
        self.q = queue.Queue()

    def _callback(self, indata, frames, time, status):
        if status:
            print(f"⚠ VOSK audio status: {status}")
        # indata comes as bytes when using RawInputStream with dtype='int16'
        self.q.put(bytes(indata))

    def listen_and_transcribe(self, duration=5):
        """Escucha desde el micrófono durante `duration` segundos y retorna transcripción (str)."""
        rec = KaldiRecognizer(self.model, self.sample_rate)

        try:
            with sd.RawInputStream(samplerate=self.sample_rate, blocksize=8000, dtype='int16', channels=1, callback=self._callback):
                import time
                print(f"🎤 Escuchando (VOSK) por {duration}s...")
                start = time.time()
                text_parts = []
                while True:
                    if (time.time() - start) > duration:
                        break
                    try:
                        data = self.q.get(timeout=0.5)
                    except queue.Empty:
                        continue

                    if rec.AcceptWaveform(data):
                        res = json.loads(rec.Result())
                        if res.get('text'):
                            text_parts.append(res.get('text'))

                # Obtener resultado final
                final = json.loads(rec.FinalResult())
                if final.get('text'):
                    text_parts.append(final.get('text'))

                return " ".join(text_parts).strip()
        except Exception as e:
            print(f"❌ Error VOSK STT: {e}")
            return ""

    def transcribe_file(self, wav_path):
        """Transcribe un archivo WAV (16kHz mono int16 preferido)."""
        rec = KaldiRecognizer(self.model, self.sample_rate)
        import wave
        results = []
        try:
            wf = wave.open(wav_path, 'rb')
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    res = json.loads(rec.Result())
                    if res.get('text'):
                        results.append(res.get('text'))
            final = json.loads(rec.FinalResult())
            if final.get('text'):
                results.append(final.get('text'))
            return ' '.join(results).strip()
        except Exception as e:
            print(f"❌ Error transcribing file with VOSK: {e}")
            return ""
