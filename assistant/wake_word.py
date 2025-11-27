"""Wake Word Detection - Detectar 'Hey JARVIS' para activar escucha."""
import speech_recognition as sr
from pocketsphinx import Decoder, get_modelpath
import os


class WakeWordDetector:
    """Detector de palabras clave para activar JARVIS."""
    
    def __init__(self, wake_words=None):
        """
        Inicializar detector.
        
        Args:
            wake_words: lista de palabras clave ('hey jarvis', 'jarvis', etc.)
        """
        self.wake_words = wake_words or [
            "hey jarvis",
            "jarvis",
            "oye jarvis",
            "escucha jarvis"
        ]
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Intentar inicializar PocketSphinx para detección local
        try:
            modelpath = get_modelpath()
            self.decoder = Decoder(
                hmm=os.path.join(modelpath, 'en-us'),
                lm=os.path.join(modelpath, 'en-us.lm.bin'),
                dict=os.path.join(modelpath, 'cmudict-en-us.dict')
            )
            self.sphinx_available = True
            print("✓ PocketSphinx disponible para detección local")
        except Exception as e:
            print(f"⚠ PocketSphinx no disponible: {e}")
            print("  Usando Google Speech Recognition como fallback")
            self.sphinx_available = False
    
    def detect_wake_word(self, timeout=10, phrase_time_limit=5):
        """
        Detectar palabra clave del micrófono.
        
        Args:
            timeout: tiempo máximo de escucha (segundos)
            phrase_time_limit: tiempo máximo de frase (segundos)
            
        Returns:
            True si se detectó palabra clave, False si no
        """
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("🎤 Escuchando palabra clave...")
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            
            # Intentar con Google Speech Recognition
            try:
                text = self.recognizer.recognize_google(audio, language="es-ES")
                text_lower = text.lower()
                print(f"📝 Detectado: '{text}'")
                
                # Comprobar si es una palabra clave
                for wake_word in self.wake_words:
                    if wake_word in text_lower:
                        print(f"✓ Palabra clave encontrada: '{wake_word}'")
                        return True
                
                return False
            except sr.UnknownValueError:
                print("⚠ No se pudo entender el audio")
                return False
            except sr.RequestError as e:
                print(f"❌ Error de servicio Google: {e}")
                return False
        except sr.RequestError as e:
            print(f"❌ Error de micrófono: {e}")
            return False
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return False
    
    def continuous_listen(self, on_wake_word=None, timeout=None):
        """
        Escucha continua hasta detectar palabra clave.
        
        Args:
            on_wake_word: callback cuando se detecta palabra clave
            timeout: timeout total (None = infinito)
            
        Returns:
            True si se detectó palabra clave
        """
        print("🔊 Iniciando escucha continua... (di 'Hey JARVIS' o similar)")
        import time
        start_time = time.time()
        
        while True:
            if timeout and (time.time() - start_time) > timeout:
                print("⏱ Timeout alcanzado")
                return False
            
            if self.detect_wake_word(timeout=5, phrase_time_limit=3):
                if on_wake_word:
                    on_wake_word()
                return True


# Test rápido
if __name__ == "__main__":
    print("=== Test de Wake Word Detection ===\n")
    
    detector = WakeWordDetector()
    print("\nDi 'Hey JARVIS' en los próximos 10 segundos...")
    detected = detector.detect_wake_word(timeout=10, phrase_time_limit=5)
    
    if detected:
        print("✓ Palabra clave detectada correctamente")
    else:
        print("✗ No se detectó palabra clave")
