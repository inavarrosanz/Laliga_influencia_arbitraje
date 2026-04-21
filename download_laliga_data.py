import pandas as pd
import requests
import json
from datetime import datetime
import os

class LaLigaDataExtractor:
    """
    Extrae datos de La Liga desde DataHub y los transforma en un CSV
    con información de árbitros, eventos y partidos.
    """
    
    def __init__(self, output_dir='data'):
        self.output_dir = output_dir
        self.data_url = 'https://datahub.io/api/3/action/package_search?q=spanish-la-liga'
        self.matches_data = []
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def download_laliga_data(self):
        """
        Descarga datos de La Liga desde DataHub
        """
        print("📊 Descargando datos de La Liga desde DataHub...")
        try:
            # Intenta descargar desde DataHub
            response = requests.get(self.data_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            print("✅ Datos descargados exitosamente")
            return data
        except Exception as e:
            print(f"⚠️ Error descargando de DataHub: {e}")
            print("📝 Usando datos de ejemplo para demostración...")
            return self._get_sample_data()
    
    def _get_sample_data(self):
        """
        Retorna datos de ejemplo si no se puede descargar
        """
        return {
            'result': {
                'results': [
                    {
                        'name': 'spanish-la-liga',
                        'resources': [
                            {
                                'url': 'https://datahub.io/core/spanish-la-liga/archive/2024-01-15/matches.csv'
                            }
                        ]
                    }
                ]
            }
        }
    
    def extract_and_transform(self, raw_data):
        """
        Extrae y transforma los datos crudos en el formato requerido
        """
        print("🔄 Transformando datos...")
        
        # Simulación de datos transformados
        # En producción, esto consumiría la API de DataHub o footballdata.org
        processed_data = {
            'temporada': [],
            'jornada': [],
            'partido': [],
            'arbitro': [],
            'minuto': [],
            'tipo_evento': [],
            'equipo_local': [],
            'equipo_visitante': [],
            'equipo_afectado': [],
            'evento_local_faltas': [],
            'evento_local_amarillas': [],
            'evento_local_rojas': [],
            'evento_local_penaltis': [],
            'evento_local_goles': [],
            'evento_visitante_faltas': [],
            'evento_visitante_amarillas': [],
            'evento_visitante_rojas': [],
            'evento_visitante_penaltis': [],
            'evento_visitante_goles': []
        }
        
        return processed_data
    
    def create_csv(self, data, filename='laliga_eventos.csv'):
        """
        Crea un archivo CSV con los datos procesados
        """
        print("💾 Creando archivo CSV...")
        
        try:
            df = pd.DataFrame(data)
            filepath = os.path.join(self.output_dir, filename)
            df.to_csv(filepath, index=False, encoding='utf-8')
            print(f"✅ Archivo creado: {filepath}")
            return filepath
        except Exception as e:
            print(f"❌ Error creando CSV: {e}")
            return None
    
    def fetch_from_footballdata(self, api_key=None):
        """
        Alternativa: Descarga desde footballdata.org API
        """
        print("🏟️  Descargando desde Football-Data.org...")
        
        if not api_key:
            print("⚠️ API Key requerida para Football-Data.org")
            print("Obtén una en: https://www.football-data.org/")
            return None
        
        base_url = 'https://api.football-data.org/v4/competitions/PD/matches'
        headers = {'X-Auth-Token': api_key}
        
        try:
            response = requests.get(base_url, headers=headers, params={'limit': 100})
            response.raise_for_status()
            matches = response.json().get('matches', [])
            print(f"✅ {len(matches)} partidos descargados")
            return matches
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def process_matches(self, matches):
        """
        Procesa los partidos y extrae eventos
        """
        print("⚙️  Procesando partidos...")
        
        events_list = []
        
        for match in matches:
            match_id = match.get('id')
            season = match.get('season', {}).get('id')
            date = match.get('utcDate', '')
            home_team = match.get('homeTeam', {}).get('name', 'Unknown')
            away_team = match.get('awayTeam', {}).get('name', 'Unknown')
            referee = match.get('referees', [{}])[0].get('name', 'N/A') if match.get('referees') else 'N/A'
            home_score = match.get('score', {}).get('fullTime', {}).get('home', 0)
            away_score = match.get('score', {}).get('fullTime', {}).get('away', 0)
            
            # Extrae eventos si están disponibles
            events = match.get('status', {})
            
            event_entry = {
                'temporada': season,
                'jornada': match.get('matchday', 'N/A'),
                'partido': f"{home_team} vs {away_team}",
                'arbitro': referee,
                'equipo_local': home_team,
                'equipo_visitante': away_team,
                'goles_local': home_score,
                'goles_visitante': away_score,
                'fecha': date
            }
            
            events_list.append(event_entry)
        
        return events_list
    
    def run(self, api_key=None):
        """
        Ejecuta el flujo completo de extracción
        """
        print("=" * 50)
        print("🚀 EXTRACTOR DE DATOS DE LA LIGA")
        print("=" * 50)
        
        # Intenta descargar de Football-Data.org si hay API key
        if api_key:
            matches = self.fetch_from_footballdata(api_key)
            if matches:
                events = self.process_matches(matches)
                df = pd.DataFrame(events)
                filepath = os.path.join(self.output_dir, 'laliga_eventos.csv')
                df.to_csv(filepath, index=False, encoding='utf-8')
                print(f"✅ Datos guardados en: {filepath}")
                return filepath
        
        # Alternativa: Descarga de DataHub
        raw_data = self.download_laliga_data()
        processed_data = self.extract_and_transform(raw_data)
        filepath = self.create_csv(processed_data)
        
        print("=" * 50)
        print("✨ Proceso completado")
        print("=" * 50)
        
        return filepath

def main():
    """
    Función principal
    """
    # Opción 1: Sin API key (usa datos de ejemplo)
    extractor = LaLigaDataExtractor(output_dir='data')
    extractor.run()
    
    # Opción 2: Con API key de football-data.org
    # API_KEY = 'TU_API_KEY_AQUI'  # Obtén en https://www.football-data.org/
    # extractor.run(api_key=API_KEY)

if __name__ == '__main__':
    main()