"""Wake Word Detection - Detectar 'Hey JARVIS' para activar escucha."""
import speech_recognition as sr
import os


class WakeWordDetector:
    """Detector de palabras clave para activar JARVIS."""
    
    def __init__(self, wake_words=None):
        """
        Inicializar detector.
        
        Args:
            wake_words: lista de palabras clave ('jarvis', 'oye jarvis')
        """
        self.wake_words = wake_words or [
            "jarvis",
            "oye jarvis"
        ]
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Intentar inicializar VOSK como detector offline (mejor precisión que pocketsphinx)
        self.vosk_available = False
        try:
            from assistant.stt_vosk import VoskSTT
            vosk_model_dir = os.path.join('assistant_data', 'models', 'vosk-model-small-es-0.22')
            if os.path.exists(vosk_model_dir):
                try:
                    self.vosk = VoskSTT(model_path=vosk_model_dir)
                    self.vosk_available = True
                    print("✓ VOSK disponible para detección de palabra clave (offline)")
                except Exception as e:
                    print(f"⚠ No se pudo inicializar VOSK para wake word: {e}")
        except Exception:
            self.vosk_available = False

        # Si VOSK no está disponible, usaremos SpeechRecognition con Google como fallback
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
        # Si VOSK está disponible, usarlo para detección offline
        if getattr(self, 'vosk_available', False):
            try:
                text = self.vosk.listen_and_transcribe(duration=phrase_time_limit)
                text_lower = (text or "").lower()
                print(f"📝 (VOSK) Detectado: '{text}'")
                for wake_word in self.wake_words:
                    if wake_word in text_lower:
                        print(f"✓ Palabra clave encontrada: '{wake_word}' (VOSK)")
                        return True
                return False
            except Exception as e:
                print(f"⚠ Error VOSK durante wake-word: {e}")
                # continuar al fallback

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
        print("🔊 Iniciando escucha continua... (di 'JARVIS' u 'Oye JARVIS')")
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
    print("\nDi 'JARVIS' u 'Oye JARVIS' en los próximos 10 segundos...")
    detected = detector.detect_wake_word(timeout=10, phrase_time_limit=5)
    
    if detected:
        print("✓ Palabra clave detectada correctamente")
    else:
        print("✗ No se detectó palabra clave")
