import time
from periphery import GPIO
from RPLCD.i2c import CharLCD

# --- 설정 ---
# PIR 센서 핀 설정 (BCM 번호 기준)
PIR_PIN_BCM = 17
GPIO_CHIP = "/dev/gpiochip0"

# LCD 설정 (우리가 확인한 주소!)
LCD_I2C_ADDRESS = 0x27
I2C_BUS = 1
LCD_COLS = 16
LCD_ROWS = 2

# --- 하드웨어 초기화 ---
pir_pin = None
lcd = None

try:
    # 1. PIR 센서 초기화
    pir_pin = GPIO(GPIO_CHIP, PIR_PIN_BCM, "in")
    print("PIR 센서 초기화 완료.")

    # 2. LCD 초기화
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
    print("배선 및 I2C/GPIO 권한을 확인하세요.")
    # 하나라도 초기화 실패하면 프로그램 종료
    if pir_pin:
        pir_pin.close()
    if lcd:
        lcd.close(clear=True)
    exit()

# --- 메인 프로그램 ---
try:
    print("시스템 준비 완료. 센서 안정화를 시작합니다...")
    lcd.write_string("System Starting.")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("Calibrating...")
    time.sleep(10)  # 센서가 안정화될 시간 (실제로는 30초~1분 권장)

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
                # 움직임 감지됨!
                timestamp = time.strftime("%H:%M:%S")
                print(f"[{timestamp}] 움직임 감지!")

                lcd.clear()
                lcd.write_string("Status: Motion!!")
                lcd.cursor_pos = (1, 0)
                lcd.write_string(f"Time: {timestamp}")
            else:
                # 움직임 없음.
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
    # 프로그램 종료 시 모든 리소스 정리
    print("리소스 정리 중...")
    if pir_pin:
        pir_pin.close()
    if lcd:
        lcd.close(clear=True)
    print("정리 완료.")
