from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from app.database.requests import user_water_intake_requests
from app.utils.utils import create_line_chart

water_intake_chart_router = Router()


@water_intake_chart_router.message(Command("water_intake_chart"))
async def log_water_intake_chart(message: Message):
    """
    Create and plot chart that shows user's water intake for all records.
    """
    # All water consumption records for selected user.
    all_water_consumption_data = \
        await user_water_intake_requests.get_list_of_water_intake(tg_id=message.from_user.id)
    n_liters_list, dates_list = zip(*map(lambda x: (x.n_liters, x.date), all_water_consumption_data))

    buffered_image = create_line_chart(x=dates_list, y=n_liters_list, x_label='dates', y_label='water intake')

    await message.answer_photo(photo=buffered_image, caption='💧 Потребление воды за все время:',
                               show_caption_above_media=True)
