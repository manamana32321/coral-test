import time
from periphery import GPIO
from RPLCD.i2c import CharLCD

# --- 설정 ---
# 데이터시트의 GPIO_3, 즉 라인 번호 3을 사용하도록 변경
PIR_GPIO_LINE = 6
GPIO_CHIP = "/dev/gpiochip0"

# LCD 설정 (이전과 동일)
LCD_I2C_ADDRESS = 0x27
I2C_BUS = 1
LCD_COLS = 16
LCD_ROWS = 2

# --- 하드웨어 초기화 ---
pir_pin = None
lcd = None

try:
    # 1. PIR 센서 초기화 (수정된 핀 번호 사용)
    pir_pin = GPIO(GPIO_CHIP, PIR_GPIO_LINE, "in")
    print(f"PIR 센서 초기화 완료. (GPIO Line: {PIR_GPIO_LINE})")

    # 2. LCD 초기화 (이전과 동일)
    lcd = CharLCD(
        i2c_expander="PCF8574",
        address=LCD_I2C_ADDRESS,
        port=I2C_BUS,
        cols=LCD_COLS,
        rows=LCD_ROWS,
    )
    lcd.clear()
    print("LCD 초기화 완료.")

except Exception as e:
    print(f"하드웨어 초기화 실패: {e}")
    if pir_pin:
        pir_pin.close()
    if lcd:
        lcd.close(clear=True)
    exit()

# --- 메인 프로그램 (이하 코드는 이전과 동일) ---
try:
    print("시스템 준비 완료. 센서 안정화를 시작합니다...")
    lcd.write_string("System Starting.")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("Calibrating...")
    time.sleep(10)

    last_state = False
    lcd.clear()
    lcd.write_string("Status: Normal")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("All Clear")
    print("센서 준비 완료. 움직임을 감지합니다...")

    while True:
        current_state = pir_pin.read()
        if current_state != last_state:
            if current_state:
                timestamp = time.strftime("%H:%M:%S")
                print(f"[{timestamp}] 움직임 감지!")
                lcd.clear()
                lcd.write_string("Status: Motion!!")
                lcd.cursor_pos = (1, 0)
                lcd.write_string(f"Time: {timestamp}")
            else:
                print("상태: 정상. 움직임 없음.")
                lcd.clear()
                lcd.write_string("Status: Normal")
                lcd.cursor_pos = (1, 0)
                lcd.write_string("All Clear")
            last_state = current_state
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n프로그램을 종료합니다.")
finally:
    print("리소스 정리 중...")
    if pir_pin:
        pir_pin.close()
    if lcd:
        lcd.close(clear=True)
    print("정리 완료.")
