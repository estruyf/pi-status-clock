# Raspberry Pi Status Clock

## Cron job

```
crontab -e

*/1 * * * * /usr/bin/python3 /home/pi/pi-status-clock/status-clock.py
```