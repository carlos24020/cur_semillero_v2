import httpx
from app.core.config import settings


async def get_leader(leader_id: int):
    """Obtiene información de un líder desde el ms-leaders"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.leaders_service_url}/leaders/{leader_id}",
                timeout=5.0
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error al conectar con ms-leaders: {e}")
            return None


async def get_all_leaders():
    """Obtiene todos los líderes desde ms-leaders"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.leaders_service_url}/leaders/",
                timeout=5.0
            )
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error al conectar con ms-leaders: {e}")
            return []
