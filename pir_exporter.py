import time
from periphery import GPIO
from prometheus_client import start_http_server, Gauge, Counter

# --- 설정 ---
# 네가 선택한 GPIO 라인 번호 6 사용
PIR_GPIO_LINE = 6
GPIO_CHIP = "/dev/gpiochip0"
METRICS_PORT = 8000  # 메트릭을 외부에 보여줄 웹 서버 포트

# --- Prometheus 메트릭 정의 ---
# 1. 현재 움직임 상태를 나타내는 Gauge 메트릭 (값이 1 또는 0으로 변함)
MOTION_DETECTED = Gauge(
    "motion_detected",
    "Shows if motion is currently detected (1 for motion, 0 for no motion)",
)

# 2. 총 움직임 감지 횟수를 세는 Counter 메트릭 (값은 계속 증가만 함)
MOTION_EVENTS_TOTAL = Counter(
    "motion_events_total", "Total number of motion detection events"
)


# --- 메인 프로그램 ---
def main():
    pir_pin = None
    try:
        # GPIO 핀을 입력(in)으로 열기
        pir_pin = GPIO(GPIO_CHIP, PIR_GPIO_LINE, "in")
        print(f"PIR 센서(GPIO Line: {PIR_GPIO_LINE}) 초기화 완료.")

        # PIR 센서는 전원 인가 후 내부 회로가 안정화될 시간이 필요함
        print("센서 안정화를 위해 10초간 대기합니다...")
        time.sleep(10)

        # Prometheus 메트릭을 제공할 HTTP 서버 시작
        start_http_server(METRICS_PORT)
        print(f"센서 준비 완료. 포트 {METRICS_PORT}에서 메트릭 노출을 시작합니다.")
        print("=" * 40)

        last_state = False
        MOTION_DETECTED.set(0)  # 초기 상태는 '움직임 없음(0)'으로 설정

        # 메인 루프 시작
        while True:
            current_state = pir_pin.read()

            # 상태가 이전과 다를 때만 동작 (터미널 도배 방지)
            if current_state != last_state:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                if current_state:
                    # 움직임 감지됨!
                    print(f"✅ [{timestamp}] 움직임 감지됨!")
                    MOTION_DETECTED.set(1)  # Gauge 값을 1로 설정
                    MOTION_EVENTS_TOTAL.inc()  # Counter 값을 1 증가
                else:
                    # 움직임 없음.
                    print(f"⚪️ [{timestamp}] 상태: 정상 (움직임 없음)")
                    MOTION_DETECTED.set(0)  # Gauge 값을 0으로 설정

                last_state = current_state

            # 0.1초마다 상태를 확인하여 CPU 사용률을 낮춤
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")
    except Exception as e:
        print(f"\n에러 발생: {e}")
    finally:
        # 프로그램 종료 시 GPIO 리소스 정리
        if pir_pin:
            pir_pin.close()
        print("GPIO 리소스가 정리되었습니다.")


if __name__ == "__main__":
    main()
