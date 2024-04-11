import pendulum

days_of_week_mapping = {
    "poniedziałek": "Monday",
    "wtorek": "Tuesday",
    "środa": "Wednesday",
    "czwartek": "Thursday",
    "piątek": "Friday",
    "sobota": "Saturday",
    "niedziela": "Sunday"
}


def add_task_todo_list(task_name: str) -> dict:
    '''
    Adds task to ToDo list. No date is needed.

    Parameters:
    date (str): Description of task

    Returns:
    dict: json
    '''
    return {
        "tool": "ToDo",
        "desc": task_name
    }


def add_event_to_calendar(desc: str, date_str: str) -> dict:
    '''
    Adds event to calendar. Takes as argument description of event, and calendar date.

    Parameters:
    date (str): Description of event
    date (str): Date can have a form like 'jutro', 'pojutrze', 'poniedziałek'

    Returns:
    dict: json
    '''

    now = pendulum.now()
    if date_str.lower() == "jutro":
        date = now.add(days=1)
    elif date_str.lower() == "pojutrze":
        date = now.add(days=2)
    else:
        date = pendulum.parse(days_of_week_mapping.get(date_str.lower()), strict=False)

    return {
        "tool": "Calendar",
        "desc": desc,
        "date": date.strftime("%Y-%m-%d")
    }
