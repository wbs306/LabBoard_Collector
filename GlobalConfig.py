is_exit = False
is_using_battery = False

# Path to database file
db_path = "test.db"

sleep_time = "23:30"
wakeup_time = "08:00"

go_sleep = False

class UPSCollectorConfig:
    # Check battery using state per battery_checkk_interval second
    battery_check_interval = 5

    collect_interval = 3600

class FanCollectorConfig:
    # Check CPU temperature per check_interval second
    check_interval = 15

    collect_interval = 10

    # Fan GPIO Pin
    fan_gpio = 18

    # Start the fan when CPU temperature hit temp_min
    temp_min = 30

    # Full running the fan when CPU temperature hit temp_max
    temp_max = 50

    # The frequency of PWM
    pwm_freq = 75

class SensorCollectorConfig:
    collect_interval = 600
