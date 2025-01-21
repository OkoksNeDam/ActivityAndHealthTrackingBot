from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from app.database.requests import user_food_intake_requests
from app.utils.utils import create_line_chart

food_intake_chart_router = Router()


@food_intake_chart_router.message(Command("food_intake_chart"))
async def log_food_intake_chart(message: Message):
    """
    Create and plot chart that shows user's food intake for all records.
    """
    # All food consumption records for selected user.
    all_food_consumption_data = \
        await user_food_intake_requests.get_list_of_food_intake(tg_id=message.from_user.id)
    all_food_consumption_data = list(all_food_consumption_data)
    if not all_food_consumption_data:
        await message.answer("😞 К сожалению, данные о потребленных калориях отстствуют :(")
        return
    n_calories_eaten_list, dates_list = zip(*map(lambda x: (x.n_calories_consumed, x.date), all_food_consumption_data))

    buffered_image = create_line_chart(x=dates_list, y=n_calories_eaten_list, x_label='dates', y_label='food intake')

    await message.answer_photo(photo=buffered_image, caption='🍫 Количество употребленных калорий за все время:',
                               show_caption_above_media=True)
