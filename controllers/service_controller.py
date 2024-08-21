from datetime import datetime, date

def logPrinter(client, page, data):
    """
    Вывод строки с датой и необходимой информацией
    """
    with open('logs/main.log', 'a', encoding='UTF-8') as file:
        now = datetime.now().strftime("%d/%b/%Y %H:%M:%S.%f")[:-3]
        string = f'{client} - - [{now}] | {page} | {data}'
        print(string, file = file) # output to file
        print(string)

