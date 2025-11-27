"""APIs integradas - Clima, noticias, hora, fecha, búsquedas."""
import requests
import json
from datetime import datetime
from typing import Dict, Optional


class IntegratedAPIs:
    """Integración de APIs públicas para enriquecer respuestas."""
    
    def __init__(self):
        """Inicializar APIs."""
        self.session = requests.Session()
        self.weather_api_key = None  # Opcional: registrarse en openweathermap.org
        self.news_api_key = None     # Opcional: registrarse en newsapi.org
    
    def set_weather_api_key(self, api_key):
        """Configurar clave API de OpenWeatherMap."""
        self.weather_api_key = api_key
    
    def set_news_api_key(self, api_key):
        """Configurar clave API de NewsAPI."""
        self.news_api_key = api_key
    
    # ==================== HORA Y FECHA ====================
    def get_time(self) -> str:
        """Obtener hora actual."""
        now = datetime.now()
        return now.strftime("%H:%M:%S")
    
    def get_date(self) -> str:
        """Obtener fecha actual."""
        now = datetime.now()
        return now.strftime("%d de %B de %Y")
    
    def get_datetime(self) -> str:
        """Obtener fecha y hora actual."""
        now = datetime.now()
        weekday = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"][now.weekday()]
        date_str = now.strftime("%d de %B de %Y")
        time_str = now.strftime("%H:%M:%S")
        return f"{weekday} {date_str} a las {time_str}"
    
    # ==================== CLIMA ====================
    def get_weather(self, city: str, lang: str = "es") -> Dict:
        """
        Obtener clima de una ciudad (requiere API key).
        
        Args:
            city: nombre de ciudad
            lang: idioma (es, en, etc.)
            
        Returns:
            dict con info de clima
        """
        if not self.weather_api_key:
            return {
                "error": "API key no configurada",
                "message": "Registrate en openweathermap.org y configura tu clave API"
            }
        
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": city,
                "appid": self.weather_api_key,
                "lang": lang,
                "units": "metric"
            }
            resp = self.session.get(url, params=params, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            
            return {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
                "wind_speed": data["wind"]["speed"]
            }
        except Exception as e:
            return {"error": str(e)}
    
    # ==================== NOTICIAS ====================
    def get_news(self, query: str = "top headlines", country: str = "es") -> Dict:
        """
        Obtener noticias (requiere API key de NewsAPI).
        
        Args:
            query: búsqueda o 'top headlines'
            country: código país (es, us, uk, etc.)
            
        Returns:
            dict con noticias
        """
        if not self.news_api_key:
            return {
                "error": "API key no configurada",
                "message": "Registrate en newsapi.org y configura tu clave API"
            }
        
        try:
            url = "https://newsapi.org/v2/top-headlines"
            params = {
                "country": country,
                "apiKey": self.news_api_key,
                "pageSize": 5
            }
            resp = self.session.get(url, params=params, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            
            articles = []
            for article in data.get("articles", [])[:3]:
                articles.append({
                    "title": article["title"],
                    "source": article["source"]["name"],
                    "url": article["url"]
                })
            
            return {"articles": articles}
        except Exception as e:
            return {"error": str(e)}
    
    # ==================== BÚSQUEDAS ====================
    def web_search(self, query: str) -> Dict:
        """
        Búsqueda web básica (usando DuckDuckGo, sin API key).
        
        Args:
            query: término de búsqueda
            
        Returns:
            dict con resultados
        """
        try:
            # DuckDuckGo instant answers (sin API key)
            url = "https://api.duckduckgo.com/"
            params = {
                "q": query,
                "format": "json",
                "pretty": 1
            }
            resp = self.session.get(url, params=params, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            
            result = {
                "query": query,
                "abstract": data.get("Abstract", ""),
                "abstract_source": data.get("AbstractSource", ""),
                "answer": data.get("Answer", "")
            }
            
            # Agregar primeros resultados
            if data.get("Results"):
                result["results"] = [
                    {"title": r.get("Text"), "url": r.get("FirstURL")}
                    for r in data["Results"][:3]
                ]
            
            return result
        except Exception as e:
            return {"error": str(e)}
    
    # ==================== UTILIDADES ====================
    def get_system_info(self) -> Dict:
        """Obtener información del sistema."""
        import platform
        import psutil
        
        return {
            "system": platform.system(),
            "version": platform.version(),
            "processor": platform.processor(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage("/").percent
        }
    
    def calculate(self, expression: str) -> Optional[float]:
        """
        Evaluar expresión matemática simple.
        
        Args:
            expression: ej. "2 + 2", "10 * 5", "sqrt(16)"
            
        Returns:
            resultado numérico
        """
        try:
            import math
            # Sólo operaciones seguras
            safe_dict = {
                "sqrt": math.sqrt,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "log": math.log,
                "exp": math.exp,
                "pi": math.pi,
                "e": math.e,
                "abs": abs,
                "pow": pow
            }
            result = eval(expression, {"__builtins__": {}}, safe_dict)
            return float(result)
        except Exception as e:
            return None


# Test rápido
if __name__ == "__main__":
    print("=== Test de APIs Integradas ===\n")
    
    api = IntegratedAPIs()
    
    print(f"Hora: {api.get_time()}")
    print(f"Fecha: {api.get_date()}")
    print(f"Fecha/Hora: {api.get_datetime()}\n")
    
    # Búsqueda web
    print("Búsqueda web (Python):")
    result = api.web_search("Python programming language")
    if "abstract" in result and result["abstract"]:
        print(f"  Resumen: {result['abstract'][:200]}...")
    if "results" in result:
        for r in result["results"][:2]:
            print(f"  - {r['title']}")
    
    # Cálculos
    print(f"\nCálculo (2 + 2): {api.calculate('2 + 2')}")
    print(f"Cálculo (sqrt(16)): {api.calculate('sqrt(16)')}")
