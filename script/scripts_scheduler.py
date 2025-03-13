import os
from datetime import datetime
from rich import print
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from config import TIME_SETTINGS
import logging
import logging.config
from logging_config import LOGGING_CONFIG
from ryanair_one_way_cheap import main

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)




class ScriptScheduler:
    """
    Scheduler class to execute scripts based on predefined time settings.
    Attributes:
        scripts (tuple): Immutable tuple of callable script functions to execute.
        time_settings (tuple): Immutable tuple of (hour, minute) schedules.
        scheduler (BlockingScheduler): The APScheduler instance for scheduling jobs.
    """
    def __init__(self, scripts, time_settings):
        """
        Initialize the scheduler with scripts and time settings.
        Args:
            scripts (list): List of callable script functions to execute.
            time_settings (list): List of (hour, minute) tuples specifying run times
        Raises:
            ValueError: If scripts or time_settings are empty.
        """
        if not scripts:
            logger.error("Scripts list is empty.")
            raise ValueError("Scripts list cannot be empty.")
        if not time_settings:
            logger.error("Schedules time list is empty.")
            raise ValueError("Schedules time list cannot be empty.")

        self.scripts = tuple(scripts)
        self.time_settings = tuple(time_settings)
        self.scheduler = BlockingScheduler()

    def run_scripts(self):
        """Run all scripts in sequence."""
        for script_function in self.scripts:
            try:
                print(f"Starting '{script_function.__name__}' script...")
                script_function()
                print(f"script '{script_function.__name__}' completed successfully")
            except Exception as e:
                logger.error(f"Error: {e} in ScriptScheduler")
                print(f"Error in ScriptScheduler {script_function.__name__} script: {e}")
            logger.info("Scheduler running...")
            print("Scheduler running ...")
            print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))


    def create_trigger(self, hour, minute):
        """
        Create and return a cron-based trigger for a specific time.
        Args:
            hour (int): Hour of the day (0-23).
            minute (int): Minute of the hour (0-59).
        Returns:
            CronTrigger: An APScheduler CronTrigger object.
        """
        return CronTrigger(
            year="*", month="*", week='*', day_of_week='*', hour=hour, minute=minute
        )

    def add_job(self, job_id, trigger):
        """
        Add a new job to the scheduler.
        Args:
            job_id (str): Unique identifier for the job.
            trigger (CronTrigger): Trigger specifying when the job should run.
        """
        self.scheduler.add_job(
            self.run_scripts,
            trigger=trigger,
            id=job_id,
        )

    def schedule_jobs(self):
        """
        Schedule jobs based on the predefined time settings.
        - Iterates through time_settings and schedules each job.
        - Uses cron triggers for recurring execution.
        """
        for hour, minute in self.time_settings:
            trigger = self.create_trigger(hour, minute)
            job_id = f"job_{hour}_{minute}"
            self.add_job(job_id, trigger)

    def start(self):
        """Start the scheduler."""
        self.schedule_jobs()
        print("Starting scripts scheduler ...")
        print(f"Current time: {datetime.now().strftime('%H:%M:%S')}")
        try:
            self.scheduler.start()
        except (KeyboardInterrupt):
            logger.warning("Scheduler stopped KeyboardInterrupt")
            print("Scheduler stopped KeyboardInterrupt")
        except (SystemExit):
            logger.warning("Scheduler stopped SystemExit")
            print("Scheduler stopped SystemExit")


if __name__ == "__main__":
    SCRIPT_FUNCTIONS = [main,]
    scheduler = ScriptScheduler(SCRIPT_FUNCTIONS, TIME_SETTINGS)
    scheduler.start()
