import httpx
import asyncio
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class NotificationClient:
    def __init__(self):
        self.base_url = os.getenv("NOTIFICATIONS_SERVICE_URL", "http://localhost:8002")
        self.timeout = 30.0
    
    async def send_notification(self, notification_data: Dict[str, Any]) -> bool:
        """
        Envía una notificación al servicio de notificaciones
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/v1/notification/convocatoria-elegida/",
                    json=notification_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    return True
                else:
                    print(f"Error al enviar notificación: {response.status_code} - {response.text}")
                    return False
                    
        except httpx.TimeoutException:
            print("Timeout al enviar notificación")
            return False
        except Exception as e:
            print(f"Error inesperado al enviar notificación: {str(e)}")
            return False
    
    async def send_interest_confirmation_email(
        self, 
        user_email: str, 
        username: str, 
        convocatoria_data: Dict[str, Any]
    ) -> bool:
        """
        Envía un correo de confirmación de interés en una convocatoria
        """
        notification_data = {
            "user_name": username,
            "user_email": user_email,
            "convocatoria_titulo": f"Intercambio en {convocatoria_data.get('institution', 'Universidad')}",
            "convocatoria_descripcion": f"Programa de {convocatoria_data.get('agreementType', 'intercambio')} en {convocatoria_data.get('country', '')}",
            "universidad_destino": convocatoria_data.get("institution", ""),
            "fecha_inicio": convocatoria_data.get("validity", "Por definir").split(" - ")[0] if " - " in convocatoria_data.get("validity", "") else "Por definir",
            "fecha_fin": convocatoria_data.get("validity", "Por definir").split(" - ")[1] if " - " in convocatoria_data.get("validity", "") else "Por definir"
        }
        
        return await self.send_notification(notification_data)

# Instancia global del cliente
notification_client = NotificationClient()