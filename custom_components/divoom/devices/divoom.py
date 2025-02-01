import requests
import logging

_LOGGER = logging.getLogger(__name__)

class TimeGateDevice:
    """Time Gate 기기와 통신하는 클래스"""

    def __init__(self, ip_address):
        """Time Gate의 IP 주소를 설정"""
        self.ip = ip_address
        self.base_url = f"http://{self.ip}:80/post"

    def send_message(self, text, color="#FFFFFF", font_size=16):
        """Time Gate 기기로 메시지를 전송하는 함수"""
        data = {
            "Command": "TimeGate/SendText",
            "Text": text,
            "Color": color,  # HEX 색상 코드
            "FontSize": font_size  # 폰트 크기
        }
        try:
            response = requests.post(self.base_url, json=data, timeout=5)
            response.raise_for_status()  # HTTP 오류 발생 시 예외 처리
            return response.json()
        except requests.exceptions.RequestException as e:
            _LOGGER.error(f"Time Gate 메시지 전송 실패: {e}")
            return {"status": "error", "message": str(e)}

    def set_brightness(self, brightness: int):
        """Time Gate 화면 밝기 조절 (0~100)"""
        if not (0 <= brightness <= 100):
            _LOGGER.error("밝기는 0~100 사이 값이어야 합니다.")
            return {"status": "error", "message": "Brightness must be between 0 and 100"}

        data = {
            "Command": "TimeGate/SetBrightness",
            "Brightness": brightness
        }
        try:
            response = requests.post(self.base_url, json=data, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            _LOGGER.error(f"밝기 설정 실패: {e}")
            return {"status": "error", "message": str(e)}

    def display_image(self, image_url: str):
        """Time Gate 화면에 이미지 표시"""
        data = {
            "Command": "TimeGate/ShowImage",
            "ImageURL": image_url
        }
        try:
            response = requests.post(self.base_url, json=data, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            _LOGGER.error(f"이미지 표시 실패: {e}")
            return {"status": "error", "message": str(e)}

    def clear_screen(self):
        """Time Gate 화면 초기화 (화면을 비우는 기능)"""
        data = {
            "Command": "TimeGate/ClearScreen"
        }
        try:
            response = requests.post(self.base_url, json=data, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            _LOGGER.error(f"화면 초기화 실패: {e}")
            return {"status": "error", "message": str(e)}
