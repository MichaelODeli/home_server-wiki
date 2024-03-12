import requests


def get_torrent_status(BASE_URL):
    """
    Получает статус торрентов из qBittorrent API.

    Параметры:
    BASE_URL (str): Базовый URL для доступа к qBittorrent API.

    Вывод:
    tuple: Кортеж с тремя строками, представляющими информацию о статусе торрентов.
           Первая строка - количество активных торрентов.
           Вторая строка - количество торрентов, скачиваемых в данный момент.
           Третья строка - количество торрентов, которые раздаются.

    Примечание:
    Если возникает ошибка при получении данных от qBittorrent API,
    возвращается кортеж с тремя строками, содержащими сообщение "qbittorrent не отвечает.".
    """
    try:
        response = requests.get(f"{BASE_URL}/api/v2/auth/login", timeout=10)
        # print(response.json())
        if response.status_code == 200:
            count_all = len(
                requests.get(f"{BASE_URL}/api/v2/torrents/info").json()
            )  # всего
            count_downloading = len(
                requests.get(f"{BASE_URL}/api/v2/torrents/info?filter=downloading").json()
            )  # скачивается
            count_down_av = len(
                requests.get(
                    f"{BASE_URL}/api/v2/torrents/info?filter=stalled_downloading"
                ).json()
            )  # доступны к раздаче
            count_active = len(
                requests.get(f"{BASE_URL}/api/v2/torrents/info?filter=active").json()
            )  # активны
            count_completed = len(
                requests.get(f"{BASE_URL}/api/v2/torrents/info?filter=completed").json()
            )  # активны

            count_upl = count_active - count_downloading  # раздаются
            return (
                f"Активных торрентов: {count_all}",
                f"Скачивается: {count_downloading}",
                f"Раздается: {count_upl}",
            )
        else:
            raise ConnectionError
    except:
        return ['qbittorrent не отвечает.']*3
