from dash import html, dcc
import psutil
import platform
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc


def generateTableRow(param_name, param_value="", head=False):
    return dmc.TableTr(
        [
            (
                dmc.TableTd(
                    param_name,
                    className="min-column-width center-content-vertical",
                    style={"padding": "0.3rem" if param_value != "" else "1rem"},
                )
                if not head
                else dmc.TableTh(param_name, className="min-column-width")
            ),
            (
                dmc.TableTd(
                    param_value,
                    style={"padding": "0.3rem" if param_value != "" else "1rem"},
                )
                if not head
                else dmc.TableTh(param_value)
            ),
        ]
    )


def getReadableBytes(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def getSystemInfoRows():
    uname = platform.uname()
    return [
        generateTableRow(dmc.Title("Информация о системе", order=5)),
        generateTableRow("Операционная система", f"{uname.system}"),
        generateTableRow("Идентификатор устройства", f"{uname.node}"),
        generateTableRow("Релиз", f"{uname.release}"),
        generateTableRow("Версия ОС", f"{uname.version}"),
        generateTableRow("Архитектура", f"{uname.machine}"),
        generateTableRow("Процессор", f"{uname.processor}"),
    ]


def getCPUInfoRows():
    cpufreq = psutil.cpu_freq()
    return [
        generateTableRow(dmc.Title("Информация о процессоре", order=5)),
        generateTableRow(
            "Физических/логических ядер",
            f"{psutil.cpu_count(logical=False)}/{psutil.cpu_count(logical=True)}",
        ),
        generateTableRow(
            "Базовая частота",
            f"{cpufreq.current:.2f}Mhz",
        ),
        generateTableRow(
            "Использование ядер процессора",
            html.Div(
                [
                    dmc.Button(
                        "Показать",
                        id="show-cpu-load",
                    )
                ],
                id="cpu-ring-usage",
            ),
        ),
        generateTableRow(
            "Использование процессора",
            f"{psutil.cpu_percent(interval=0.1)}%",
        ),
    ]


def getRAMSWARInfoRows():
    svmem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return [
        generateTableRow(dmc.Title("ОЗУ", order=5)),
        generateTableRow("Всего", f"{getReadableBytes(svmem.total)}"),
        generateTableRow(
            "Доступно",
            f"{getReadableBytes(svmem.available)}",
        ),
        generateTableRow("Использовано", f"{getReadableBytes(svmem.used)}"),
        generateTableRow("Процент использования", f"{svmem.percent}%"),
        generateTableRow(dmc.Title("SWAP", order=5)),
        generateTableRow("Всего", f"{getReadableBytes(swap.total)}"),
        generateTableRow("Свободно", f"{getReadableBytes(swap.free)}"),
        generateTableRow("Использовано", f"{getReadableBytes(swap.used)}"),
        generateTableRow("Процент использования", f"{swap.percent}%"),
    ]


def getPartitionsInfoRows():
    partitions = psutil.disk_partitions()
    parts_data = []
    for partition in partitions:
        partition_data = []
        partition_data.append(dcc.Markdown(f"**Устройство**: {partition.device}"))
        partition_data.append(
            dcc.Markdown(f"**Точка монтирования**: {partition.mountpoint}")
        )
        partition_data.append(dcc.Markdown(f"**Файловая система**: {partition.fstype}"))
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            partition_data.append(
                dcc.Markdown(
                    f"**Всего доступно**: {getReadableBytes(partition_usage.total)}"
                )
            )
            partition_data.append(
                dcc.Markdown(
                    f"**Использовано**: {getReadableBytes(partition_usage.used)}"
                )
            )
            partition_data.append(
                dcc.Markdown(f"**Свободно**: {getReadableBytes(partition_usage.free)}")
            )
            partition_data.append(
                dcc.Markdown(f"**Процент использования**: {partition_usage.percent}%")
            )
        except PermissionError:
            continue
        parts_data.append(
            generateTableRow(partition.device, dmc.Stack(partition_data, gap="xs"))
        )

    return [generateTableRow(dmc.Title("Накопители и разделы", order=5))] + parts_data
