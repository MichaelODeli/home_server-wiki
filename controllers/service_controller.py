from datetime import datetime, timedelta, date
import dash_mantine_components as dmc
from dash_iconify import DashIconify

# import datetime


def logPrinter(client, page, data):
    """
    Вывод строки с датой и необходимой информацией
    """
    with open("logs/main.log", "a", encoding="UTF-8") as file:
        now = datetime.now().strftime("%d/%b/%Y %H:%M:%S.%f")[:-3]
        string = f"{client} - - [{now}] | {page} | {data}"
        print(string, file=file)  # output to file
        print(string)


def numeral_noun_declension(
    number, nominative_singular, genetive_singular, nominative_plural
):
    return (
        (number in range(5, 20))
        and nominative_plural
        or (1 in (number, (diglast := number % 10)))
        and nominative_singular
        or ({number, diglast} & {2, 3, 4})
        and genetive_singular
        or nominative_plural
    )


def get_date_difference(date):
    # Получаем текущую дату
    today = date.today()

    # Вычисляем количество дней между сегодняшней датой и заданной
    days_diff = (today - date).days
    if days_diff < 0:
        raise ValueError("Заданная дата больше текущей")

    if days_diff == 0:
        return "сегодня"
    elif days_diff == 1:
        return "вчера"
    elif days_diff <= 7:
        return (
            str(days_diff)
            + " "
            + numeral_noun_declension(days_diff, "день", "дня", "дней")
            + " назад"
        )
    elif days_diff > 7 and days_diff <= 30:
        weeks_diff = days_diff // 7
        return (
            str(weeks_diff)
            + " "
            + numeral_noun_declension(weeks_diff, "неделя", "недели", "недель")
            + " назад"
        )
    else:
        years_diff = int((today - date) / timedelta(days=365))
        months_diff = int(round((today - date) / timedelta(days=30)))
        if years_diff > 0:
            return (
                str(years_diff)
                + " "
                + numeral_noun_declension(years_diff, "год", "года", "лет")
                + " назад"
            )
        elif months_diff > 0:
            return (
                str(months_diff)
                + " "
                + numeral_noun_declension(months_diff, "месяц", "месяца", "месяцев")
                + " назад"
            )
        else:
            return "более месяца назад"


# function for generating Dash Iconify content
def getIcon(
    icon, size=18, background=True, icon_color="white", background_color="black"
):
    """
    Функция getIcon возвращает иконку с заданными параметрами.

    :param icon: имя иконки
    :param size: размер иконки
    :param background: флаг, указывающий на необходимость отображения фона у иконки
    :param icon_color: цвет иконки
    :return: иконка с заданными параметрами
    """

    if icon_color == "primary":
        icon_color = "var(--bs-primary)"
    return (
        dmc.ThemeIcon(
            DashIconify(icon=icon, width=size, color=icon_color),
            size=size,
            radius=size + 7,
            # variant="subtle",
            color=background_color,
            m="5px",
        )
        if background == True
        else DashIconify(icon=icon, width=size, color=icon_color)
    )
