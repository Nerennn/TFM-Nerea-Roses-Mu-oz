# $env:BLUESKY_APP_PASSWORD="NereaTFM2025"
# $env:BLUESKY_IDENTIFIER="neretfm2025.bsky.social"
# python "c:\Users\nerea\Desktop\Bases de datos TFM\import asyncio.py"

from dotenv import load_dotenv
import os
import httpx
import json
from datetime import datetime
import logging

# Configurar logging para depuración
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Environment variables for authentication
load_dotenv("c:/Users/nerea/Desktop/Bases de datos TFM/.env")
BLUESKY_APP_PASSWORD = os.getenv('password')
BLUESKY_IDENTIFIER = os.getenv('username')

logger.info(f"Credenciales cargadas - Usuario: {BLUESKY_IDENTIFIER}, Contraseña: {'*' * len(BLUESKY_APP_PASSWORD) if BLUESKY_APP_PASSWORD else 'No configurada'}")

# Fechas de filtrado
START_DATE = datetime(2025, 4, 28)
END_DATE = datetime(2025, 5, 29)
logger.info(f"Filtro de fechas: {START_DATE} a {END_DATE}")

class BlueskyApiScraper:
    def __init__(self):
        self.service_endpoint = None
        self.access_token = None

    def create_session(self):                           
        """Crea una sesión con la API de Bluesky."""
        url = 'https://bsky.social/xrpc/com.atproto.server.createSession'
        headers = {'Content-Type': 'application/json'}
        
        # Usar credenciales directamente en lugar de variables de entorno (solo para depuración)
        data = {'identifier': "neretfm2025.bsky.social", 'password': "NereaTFM2025"}
        logger.info(f"Intentando crear sesión con usuario: neretfm2025.bsky.social")
        
        try:
            response = httpx.post(url, headers=headers, json=data)
            response.raise_for_status()
            session_data = response.json()
            self.service_endpoint = session_data['didDoc']['service'][0]['serviceEndpoint']
            self.access_token = session_data['accessJwt']
            logger.info(f"Sesión creada correctamente. Service endpoint: {self.service_endpoint}")
            return True
        except Exception as e:
            logger.error(f"Error al crear sesión: {str(e)}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Respuesta del servidor: {e.response.text}")
            return False

    def fetch_posts(self, handle, limit=None):
        """Obtiene todos los posts de una cuenta específica utilizando paginación.
        
        Args:
            handle: El handle de la cuenta a scrapear
            limit: Límite opcional de posts a obtener (None para todos)
        """
        url = f'{self.service_endpoint}/xrpc/app.bsky.feed.searchPosts'
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
        }
        
        all_posts = []
        cursor = None
        page = 1
        total_posts = 0
        
        logger.info(f"Buscando todos los posts de {handle}")
        
        while True:
            # Configurar parámetros con cursor si existe
            params = {'q': f'from:{handle}'}
            if cursor:
                params['cursor'] = cursor
            
            try:
                response = httpx.get(url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()
                
                # Obtener posts de esta página
                posts = data.get('posts', [])
                page_count = len(posts)
                total_posts += page_count
                
                logger.info(f"Página {page}: Obtenidos {page_count} posts de {handle}")
                
                # Añadir posts a la lista completa
                all_posts.extend(posts)
                
                # Verificar si hay más páginas
                cursor = data.get('cursor')
                
                # Si no hay cursor o hemos alcanzado el límite, salimos del bucle
                if not cursor or (limit and total_posts >= limit):
                    break
                    
                # Siguiente página
                page += 1
                
            except Exception as e:
                logger.error(f"Error al obtener posts de {handle} (página {page}): {str(e)}")
                if hasattr(e, 'response') and e.response:
                    logger.error(f"Respuesta del servidor: {e.response.text}")
                break
        
        logger.info(f"Total de posts obtenidos para {handle}: {total_posts}")
        
        # Devolver en el mismo formato que antes para compatibilidad
        return {"posts": all_posts}

    def filter_posts(self, posts):
        """Filtra los posts por fecha."""
        filtered_posts = []
        
        if not posts.get('posts'):
            logger.warning("No hay posts para filtrar")
            return filtered_posts
            
        logger.info(f"Filtrando {len(posts.get('posts', []))} posts por fecha")
        
        for post in posts.get('posts', []):
            try:
                # Verificar que los campos necesarios existen
                if 'record' not in post or 'createdAt' not in post['record']:
                    logger.warning(f"Post sin fecha de creación: {json.dumps(post, indent=2)}")
                    continue
                    
                created_at_str = post['record']['createdAt']
                logger.debug(f"Fecha del post: {created_at_str}")
                
                # El formato ISO 8601 puede tener una 'Z' al final que indica UTC
                created_at = datetime.fromisoformat(created_at_str.replace('Z', ''))
                
                # Verificar el rango de fechas
                if START_DATE <= created_at <= END_DATE:
                    logger.info(f"Post dentro del rango: {created_at_str}")
                    filtered_posts.append({
                        'uri': post.get('uri', ''),
                        'author': post.get('author', {}).get('handle', ''),
                        'created': created_at_str,
                        'text': post.get('record', {}).get('text', ''),
                    })
                else:
                    logger.debug(f"Post fuera del rango: {created_at_str}")
            except Exception as e:
                logger.error(f"Error al procesar post: {str(e)}")
                logger.error(f"Post problemático: {json.dumps(post, indent=2)}")
                
        logger.info(f"Filtrados {len(filtered_posts)} posts dentro del rango de fechas")
        return filtered_posts

    def save_posts(self, posts, filename):
        """Guarda los posts en un archivo JSON."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(posts, f, indent=4, ensure_ascii=False)
            logger.info(f"Guardados {len(posts)} posts en {filename}")
        except Exception as e:
            logger.error(f"Error al guardar posts en {filename}: {str(e)}")

    def scrape(self, handles):
        """Realiza el scraping para las cuentas especificadas."""
        all_posts = {}
        for handle in handles:
            logger.info(f"Iniciando scraping completo de {handle}...")
            
            # Obtener todos los posts con paginación
            posts = self.fetch_posts(handle)
            post_count = len(posts.get('posts', []))
            
            logger.info(f"Obtenidos {post_count} posts totales para {handle}")
            
            # Guardar datos crudos para depuración
            raw_filename = f"{handle.replace('@', '').replace('.', '_')}_raw.json"
            with open(raw_filename, 'w', encoding='utf-8') as f:
                json.dump(posts, f, indent=4, ensure_ascii=False)
            logger.info(f"Datos crudos guardados en {raw_filename}")
            
            # Filtrar por fecha
            filtered_posts = self.filter_posts(posts)
            all_posts[handle] = filtered_posts
            
            # Guardar posts filtrados
            posts_filename = f"{handle.replace('@', '').replace('.', '_')}_posts.json"
            self.save_posts(filtered_posts, posts_filename)
            
            # Verificar problemas con las fechas
            if post_count > 0 and len(filtered_posts) == 0:
                sample_post = posts.get('posts', [])[0]
                logger.warning(f"PROBLEMA DE FECHAS: Todas las fechas están fuera del rango especificado")
                if 'record' in sample_post and 'createdAt' in sample_post['record']:
                    created_at_str = sample_post['record']['createdAt']
                    logger.warning(f"Ejemplo de fecha: {created_at_str}")
                
        return all_posts

def main():
    # Verificar las credenciales
    if not BLUESKY_APP_PASSWORD or not BLUESKY_IDENTIFIER:
        logger.warning("Variables de entorno no configuradas. Usando credenciales directas.")
    
    scraper = BlueskyApiScraper()
    if not scraper.create_session():
        logger.error("No se pudo crear la sesión. Abortando.")
        return
    
    # Verificar handles
    handles = ['@yolandadiaz.bsky.social', '@movimientosumar.es']
    logger.info(f"Cuentas a scrapear: {handles}")
    
    # El problema podría estar en los handles, probar con otros conocidos
    # handles = ['@bsky.app'] # cuenta oficial de Bluesky para pruebas
    
    scraper.scrape(handles)
    logger.info("Scraping completado.")

if __name__ == '__main__':
    main()