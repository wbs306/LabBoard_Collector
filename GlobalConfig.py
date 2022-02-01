is_exit = False

# LBCollector
# Collect data per collect_interval second
collect_interval = 10

# Path to database file
db_path = "test.db"


# UPSCollector
is_using_battery = False

# Check battery using state per battery_checkk_interval second
battery_check_interval = 5


# FanCollector
# Check CPU temperature per check_interval second
check_interval = 15

# Fan GPIO Pin
fan_gpio = 12

# Start the fan when CPU temperature hit temp_min
temp_min = 30

# Full running the fan when CPU temperature hit temp_max
temp_max = 50

# The frequency of PWM
pwm_freq = 75