import time
import requests

# RPLCD.i2c의 CharLCD만 필요해
from RPLCD.i2c import CharLCD

# smbus2는 RPLCD 라이브러리가 내부적으로 사용하므로 직접 import 할 필요가 없어

# --- 설정 부분 ---
LCD_I2C_ADDRESS = 0x27
I2C_BUS = 1
LCD_COLS = 16
LCD_ROWS = 2
API_URL = "https://api.ipify.org"


# --- 메인 프로그램 ---
def main():
    # LCD 초기화
    try:
        # 'bus=' 인자를 제거하고 더 간단하게 초기화
        lcd = CharLCD(
            i2c_expander="PCF8574",
            address=LCD_I2C_ADDRESS,
            port=I2C_BUS,
            cols=LCD_COLS,
            rows=LCD_ROWS,
        )
        lcd.clear()
        print("LCD 초기화 성공!")
        lcd.write_string("LCD Test Ready..")
        time.sleep(2)
    except Exception as e:
        print(f"LCD 초기화 또는 I2C 통신 실패: {e}")
        # ... (이하 에러 메시지는 동일)
        return

    # 메인 루프 (이하 코드는 이전과 동일)
    try:
        while True:
            lcd.clear()
            lcd.write_string("Fetching IP...")
            print("네트워크를 통해 공인 IP 주소를 요청합니다...")

            try:
                response = requests.get(API_URL, timeout=10)
                response.raise_for_status()
                ip_address = response.text.strip()
                print(f"성공! IP 주소: {ip_address}")

                lcd.clear()
                lcd.write_string("My Public IP:")
                lcd.cursor_pos = (1, 0)
                lcd.write_string(ip_address)

            except requests.exceptions.RequestException as e:
                print(f"네트워크 에러 발생: {e}")
                lcd.clear()
                lcd.write_string("Network Error!")
                lcd.cursor_pos = (1, 0)
                lcd.write_string("Check Connect")

            print("60초 후 다시 시도합니다...")
            time.sleep(60)

    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")
        if lcd:
            lcd.clear()
            lcd.write_string("Test Finished.")
            time.sleep(2)
            lcd.close(clear=True)


if __name__ == "__main__":
    main()
