import logging
import requests
from homeassistant.components.notify import BaseNotificationService

_LOGGER = logging.getLogger(__name__)

def get_service(hass, config, discovery_info=None):
    """Home Assistant에서 Time Gate notify 서비스 등록"""
    return TimeGateNotifyService(config.get("ip"))

class TimeGateNotifyService(BaseNotificationService):
    def __init__(self, ip_address):
        """Time Gate 기기의 IP 주소 저장"""
        self.ip_address = ip_address
        self.base_url = f"http://{self.ip_address}:80/post"

    def send_message(self, message="", **kwargs):
        """메시지를 Time Gate 기기로 전송"""
        data = {
            "Command": "TimeGate/SendText",
            "Text": message,
            "Color": "#FFFFFF",
            "FontSize": 16
        }
        try:
            response = requests.post(self.base_url, json=data, timeout=5)
            response.raise_for_status()
            _LOGGER.info(f"Time Gate 메시지 전송 성공: {message}")
        except requests.exceptions.RequestException as e:
            _LOGGER.error(f"Time Gate 메시지 전송 실패: {str(e)}")
