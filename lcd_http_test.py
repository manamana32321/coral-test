import time
import requests
from RPLCD.i2c import CharLCD
from smbus2 import SMBus

# --- 설정 부분 ---
# 우리가 확인하고 기억하기로 한 LCD 주소(0x27)를 사용!
LCD_I2C_ADDRESS = 0x27
I2C_BUS = 1  # 코랄/라즈베리파이 40핀 헤더의 I2C 버스는 보통 1번
LCD_COLS = 16
LCD_ROWS = 2

# 간단한 테스트를 위한 API 주소
API_URL = "https://api.ipify.org"


# --- 메인 프로그램 ---
def main():
    # LCD 초기화
    try:
        bus = SMBus(I2C_BUS)
        lcd = CharLCD(
            i2c_expander="PCF8574",
            address=LCD_I2C_ADDRESS,
            port=I2C_BUS,
            cols=LCD_COLS,
            rows=LCD_ROWS,
            bus=bus,
        )
        lcd.clear()
        print("LCD 초기화 성공!")
        lcd.write_string("LCD Test Ready..")
        time.sleep(2)
    except Exception as e:
        print(f"LCD 초기화 또는 I2C 통신 실패: {e}")
        print("1. I2C 연결 상태 (VCC,GND,SDA,SCL) 확인")
        print("2. 'sudo i2cdetect -y 1' 명령어로 주소(0x27) 확인")
        print("3. i2c 그룹 권한 적용을 위해 재부팅했는지 확인")
        return  # LCD가 없으면 프로그램 실행 불가

    # 메인 루프 시작
    try:
        while True:
            lcd.clear()
            lcd.write_string("Fetching IP...")
            print("네트워크를 통해 공인 IP 주소를 요청합니다...")

            try:
                # HTTP GET 요청 보내기
                response = requests.get(API_URL, timeout=10)
                response.raise_for_status()  # 200 OK 응답이 아니면 에러 발생
                ip_address = response.text.strip()
                print(f"성공! 받아온 IP 주소: {ip_address}")

                # LCD에 IP 주소 표시
                lcd.clear()
                lcd.write_string("My Public IP:")
                lcd.cursor_pos = (1, 0)  # 두 번째 줄로 커서 이동
                lcd.write_string(ip_address)

            except requests.exceptions.RequestException as e:
                # 네트워크 에러 처리
                print(f"네트워크 에러 발생: {e}")
                lcd.clear()
                lcd.write_string("Network Error!")
                lcd.cursor_pos = (1, 0)
                lcd.write_string("Check Connect")

            # 1분(60초)마다 반복
            print("60초 후 다시 시도합니다...")
            time.sleep(60)

    except KeyboardInterrupt:
        # Ctrl+C를 누르면 프로그램 종료
        print("\n프로그램을 종료합니다.")
        if lcd:
            lcd.clear()
            lcd.write_string("Test Finished.")
            time.sleep(2)
            lcd.close(clear=True)  # LCD 백라이트 끄고 정리


# 이 스크립트 파일이 직접 실행될 때만 main() 함수를 호출
if __name__ == "__main__":
    main()
