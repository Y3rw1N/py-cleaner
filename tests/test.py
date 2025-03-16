import time
import datetime

date = datetime.date.today().strftime("%y-%m-%d: %H:%M")

print("\rHola", end='', flush=True)
time.sleep(0.5)

print("\rAdios\n", end='', flush=True)
print(date)
