"""Speech-to-Text con OpenAI Whisper - Transcripción en tiempo real."""
import whisper
import sounddevice as sd
import numpy as np
import tempfile
import os
from pathlib import Path


class WhisperSTT:
    """Transcriptor de voz usando OpenAI Whisper."""
    
    def __init__(self, model_name="base", language="es"):
        """
        Inicializar Whisper.
        
        Args:
            model_name: 'tiny', 'base', 'small', 'medium', 'large'
            language: código ISO 639-1 ('es' español, 'en' inglés, etc.)
        """
        self.model_name = model_name
        self.language = language
        print(f"Cargando modelo Whisper {model_name}...")
        self.model = whisper.load_model(model_name)
        print(f"✓ Whisper {model_name} cargado")
    
    def record_audio(self, duration=5, sample_rate=16000):
        """
        Grabar audio del micrófono.
        
        Args:
            duration: segundos de grabación
            sample_rate: muestras por segundo
            
        Returns:
            numpy array con audio
        """
        print(f"🎤 Grabando {duration} segundos... (presiona Ctrl+C para parar)")
        try:
            audio = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=1,
                dtype=np.float32
            )
            sd.wait()
            return audio.flatten()
        except Exception as e:
            print(f"❌ Error al grabar: {e}")
            return None
    
    def transcribe(self, audio_path=None, audio_data=None, duration=5):
        """
        Transcribir audio a texto.
        
        Args:
            audio_path: ruta a archivo de audio
            audio_data: numpy array con audio en bruto
            duration: duración en segundos si es audio_data
            
        Returns:
            texto transcrito
        """
        try:
            if audio_path:
                # Transcribir archivo existente
                result = self.model.transcribe(
                    audio_path,
                    language=self.language,
                    verbose=False
                )
                return result["text"].strip()
            elif audio_data is not None:
                # Transcribir audio en memoria
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                    import scipy.io.wavfile as wavfile
                    sample_rate = 16000
                    wavfile.write(tmp.name, sample_rate, (audio_data * 32767).astype(np.int16))
                    tmp_path = tmp.name
                
                result = self.model.transcribe(
                    tmp_path,
                    language=self.language,
                    verbose=False
                )
                os.unlink(tmp_path)
                return result["text"].strip()
            else:
                # Grabar y transcribir en tiempo real
                print("🎤 Iniciando grabación...")
                audio_data = self.record_audio(duration=duration)
                if audio_data is None:
                    return ""
                return self.transcribe(audio_data=audio_data, duration=duration)
        except Exception as e:
            print(f"❌ Error al transcribir: {e}")
            return ""
    
    def listen_and_transcribe(self, duration=5, timeout=10):
        """
        Escuchar y transcribir automáticamente.
        
        Args:
            duration: segundos de grabación
            timeout: timeout total
            
        Returns:
            texto transcrito
        """
        audio_data = self.record_audio(duration=duration)
        if audio_data is None:
            return ""
        
        text = self.transcribe(audio_data=audio_data, duration=duration)
        if text:
            print(f"📝 Transcrito: {text}")
        return text


# Test rápido
if __name__ == "__main__":
    print("=== Test de STT con Whisper ===\n")
    
    stt = WhisperSTT(model_name="base", language="es")
    print("\n1. Grabando 5 segundos...")
    text = stt.listen_and_transcribe(duration=5)
    print(f"Resultado: '{text}'")
