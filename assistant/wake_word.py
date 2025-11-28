"""Wake Word Detection - Detectar 'JARVIS' para activar escucha."""
import speech_recognition as sr
import os
from difflib import SequenceMatcher


def _is_similar(a, b, threshold=0.75):
    """
    Comparar similitud entre dos strings (fuzzy matching).
    
    Args:
        a, b: strings a comparar
        threshold: similitud mínima (0-1)
    
    Returns:
        True si son similares
    """
    ratio = SequenceMatcher(None, a.lower(), b.lower()).ratio()
    return ratio >= threshold


class WakeWordDetector:
    """Detector de palabras clave para activar JARVIS."""
    
    def __init__(self, wake_words=None, similarity_threshold=0.70):
        """
        Inicializar detector.
        
        Args:
            wake_words: lista de palabras clave ('jarvis', 'oye jarvis')
            similarity_threshold: umbral de similitud para fuzzy matching (0-1)
        """
        self.wake_words = wake_words or [
            "jarvis",
            "oye jarvis",
            "hey jarvis"  # Aceptar también "hey jarvis" por compatibilidad
        ]
        self.similarity_threshold = similarity_threshold
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
    
    def _contains_wake_word(self, text):
        """
        Verificar si el texto contiene alguna palabra clave.
        Usa búsqueda exacta primero, luego fuzzy matching.
        
        Args:
            text: texto a analizar
        
        Returns:
            (True, palabra_clave) si se encontró, (False, None) si no
        """
        if not text:
            return False, None
        
        text_lower = text.lower().strip()
        
        # Búsqueda exacta (rápida)
        for wake_word in self.wake_words:
            if wake_word in text_lower:
                return True, wake_word
        
        # Búsqueda fuzzy (tolera pequeños errores)
        for wake_word in self.wake_words:
            if _is_similar(text_lower, wake_word, self.similarity_threshold):
                return True, wake_word
            # Comprobar si la palabra clave está contenida en el texto
            for word in text_lower.split():
                if _is_similar(word, wake_word, self.similarity_threshold):
                    return True, wake_word
        
        return False, None
    
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
                
                found, matched_word = self._contains_wake_word(text)
                if found:
                    print(f"✓ Palabra clave encontrada: '{matched_word}' (VOSK)")
                    return True
                else:
                    print(f"⏭ No es palabra clave (esperaba: {self.wake_words})")
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
                print(f"📝 Detectado: '{text}'")
                
                # Comprobar si contiene palabra clave (con fuzzy matching)
                found, matched_word = self._contains_wake_word(text)
                if found:
                    print(f"✓ Palabra clave encontrada: '{matched_word}'")
                    return True
                else:
                    print(f"⏭ No es palabra clave (esperaba: {self.wake_words})")
                    return False
            except sr.UnknownValueValue:
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
    print("=== Test de Wake Word Detection (Mejorado) ===\n")
    
    detector = WakeWordDetector()
    print("\nDi 'JARVIS' u 'Oye JARVIS' en los próximos 10 segundos...")
    detected = detector.detect_wake_word(timeout=10, phrase_time_limit=5)
    
    if detected:
        print("✓ Palabra clave detectada correctamente")
    else:
        print("✗ No se detectó palabra clave")

