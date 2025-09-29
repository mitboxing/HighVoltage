import requests
import argparse
from datetime import datetime, timedelta

def main():
    # Создаем парсер аргументов командной строки
    parser = argparse.ArgumentParser(description='Получение данных свечей из Alpaca API')
    parser.add_argument('--symbols', 
                       type=str, 
                       default= "SBET,BMNR",
                       help='Тикеры для запроса (через запятую, по умолчанию: AAPL)')
    parser.add_argument('--start-date', 
                       type=str, 
                       default='2025-07-01T00:00:00Z',
                       help='Начальная дата в формате YYYY-MM-DDTHH:MM:SSZ (по умолчанию: 2024-01-03T00:00:00Z)')
    parser.add_argument('--end-date', 
                       type=str, 
                       default='2025-07-10T09:30:00-04:00',
                       help='Конечная дата в формате YYYY-MM-DDTHH:MM:SSZ (по умолчанию: 2024-01-04T09:30:00-04:00)')
    
    args = parser.parse_args()
    
    # Получаем параметры из аргументов
    symbols = args.symbols
    start_date = args.start_date
    end_date = args.end_date
    
    # Формируем URL с переменными параметрами
    url = f"https://data.alpaca.markets/v2/stocks/bars?symbols={symbols}&timeframe=1D&start={start_date}&end={end_date}&limit=1000&adjustment=raw&feed=sip&sort=asc"
    
    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": "AK0E2HYUNY0VV29DRB3B",
        "APCA-API-SECRET-KEY": "NodjUjcFs0x7GNWDkxf8otDY1sqMsK9MihluX5gg"
    }
    
    print(f"Запрос данных для тикеров: {symbols}")
    print(f"Период: с {start_date} по {end_date}")
    response = requests.get(url, headers=headers)
    
    print(response.text)

if __name__ == "__main__":
    main()
