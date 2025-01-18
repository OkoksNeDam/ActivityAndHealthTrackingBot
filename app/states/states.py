from aiogram.fsm.state import State, StatesGroup


class HealthStatusState(StatesGroup):
    choosing_weight = State()
    choosing_height = State()
    choosing_age = State()
    choosing_activity_level = State()
    choosing_city = State()


class WorkoutInfoState(StatesGroup):
    """
    States when filling out training information.
    """
    choosing_workout_type = State()
    choosing_duration = State()
