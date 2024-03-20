import asyncio
import subprocess

async def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = 'Next run in {:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')  # Use '\r' to return to the start of the line
        await asyncio.sleep(1)
        t -= 1
    print("Restarting task...                              ")  # Clear the countdown line

async def run_sendimg_every_interval(interval):
    while True:
        print("Running sendimg.py...")
        subprocess.run(["python", "sendimg.py"])
        print("Finished running sendimg.py.")
        await countdown(interval)

async def main():
    interval = 300  # Interval in seconds (300 seconds = 5 minutes)
    await run_sendimg_every_interval(interval)

if __name__ == "__main__":
    asyncio.run(main())
