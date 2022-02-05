# LabBoard_Collector
This project is to build a daemon which collect some data from sensor, ups, etc. in raspberry pi. The collecting data will be written into database, and show the detail in this repository: [LabBoard](https://github.com/wbs306/LabBoard)

## Description of collector
### LBCollector
Main collector, it will generate other collectors and a timer which write data into database in a specify interval.

### UPSCollector
Collecting data from UPS, and check if it is outage.

### SensorCollector
Collecting data from temperature sesnsor.

### FanCollector
Collect CPU temperature and fan speed.
