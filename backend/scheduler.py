from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio
from datetime import datetime
import pytz

from backend.aggregator import NewsAggregator
from backend.config import DISPLAY_CONFIG


class DailyScheduler:
    """Scheduler for daily news aggregation"""

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.aggregator = NewsAggregator()

        # Get timezone and update time from config
        timezone_str = DISPLAY_CONFIG.get('timezone', 'Europe/Berlin')
        self.timezone = pytz.timezone(timezone_str)

        update_time = DISPLAY_CONFIG.get('update_time', '06:00')
        hour, minute = map(int, update_time.split(':'))

        # Schedule daily aggregation
        trigger = CronTrigger(
            hour=hour,
            minute=minute,
            timezone=self.timezone
        )

        self.scheduler.add_job(
            self.run_aggregation,
            trigger=trigger,
            id='daily_aggregation',
            name='Daily News Aggregation',
            replace_existing=True
        )

    async def run_aggregation(self):
        """Run the daily aggregation job"""
        print(f"[SCHEDULER] Running daily aggregation at {datetime.now(self.timezone)}")
        try:
            await self.aggregator.run_daily_aggregation()
            print("[SCHEDULER] Daily aggregation completed successfully")
        except Exception as e:
            print(f"[SCHEDULER] Error during aggregation: {str(e)}")

    def start(self):
        """Start the scheduler"""
        self.scheduler.start()
        print(f"[SCHEDULER] Started. Next run: {self.scheduler.get_jobs()[0].next_run_time}")

    def stop(self):
        """Stop the scheduler"""
        self.scheduler.shutdown()
        print("[SCHEDULER] Stopped")


# For running scheduler standalone
async def main():
    scheduler = DailyScheduler()
    scheduler.start()

    # Run once immediately for testing
    print("[SCHEDULER] Running initial aggregation...")
    await scheduler.run_aggregation()

    # Keep running
    try:
        while True:
            await asyncio.sleep(3600)  # Sleep for 1 hour
    except KeyboardInterrupt:
        scheduler.stop()


if __name__ == "__main__":
    asyncio.run(main())
