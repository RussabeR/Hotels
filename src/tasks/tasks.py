import asyncio
import logging
import os
from time import sleep

from logger import logger
from src.database import async_session_maker_null_pool
from src.tasks.celery_app import celery_instance
from PIL import Image
from src.utils.db_manager import DBManager


@celery_instance.task
def sleep_task():
    sleep(5)
    print("Я закончил")


@celery_instance.task
def resize_image(image_path: str):
    logger.info(f"Меняю размер картинки по пути {image_path}")
    sizes = [1000, 500, 200]
    output_folder = "src/static/images"
    img = Image.open(image_path)
    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    for size in sizes:
        img_resized = img.resize(
            (size, int(img.height * (size / img.width))), Image.Resampling.LANCZOS
        )
        new_file_name = f"{name}_{size}px{ext}"
        output_path = os.path.join(output_folder, new_file_name)
        img_resized.save(output_path)

    logger.info("Работа с изображениями завершена")


async def get_bookings_with_checkin_today_helper():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_bookings_with_today_checkin()
        logging.debug(f"{bookings}")


@celery_instance.task(name="Booking_today_checkin")
def send_email_to_users_with_today_checkin():
    asyncio.run(get_bookings_with_checkin_today_helper())
