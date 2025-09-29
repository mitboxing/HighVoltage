import requests
import argparse
import numpy as np
from datetime import datetime, timedelta

def main():
    # Создаем парсер аргументов командной строки
    parser = argparse.ArgumentParser(description='Получение данных свечей из Alpaca API')
    parser.add_argument('--symbols', 
                       type=str, 
                       default= "SBET,BMNR",
                       help='Тикеры для запроса (через запятую, по умолчанию: SBET,BMNR)')
    parser.add_argument('--start-date', 
                       type=str, 
                       default='2025-07-01T00:00:00Z',
                       help='Начальная дата в формате YYYY-MM-DDTHH:MM:SSZ (по умолчанию: 2025-07-01T00:00:00Z)')
    parser.add_argument('--end-date', 
                       type=str, 
                       default='2025-09-29T09:30:00-04:00',
                       help='Конечная дата в формате YYYY-MM-DDTHH:MM:SSZ (по умолчанию: 2025-07-10T09:30:00-04:00)')
    
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
    
    # Создаем словарь для хранения результатов
    result_dict = {}
    
    if response.status_code == 200:
        data = response.json()
        
        # Обрабатываем каждый символ
        for symbol in symbols.split(','):
            symbol = symbol.strip()
            if symbol in data.get('bars', {}):
                bars = data['bars'][symbol]
                
                # Создаем объект с четырьмя массивами цен
                price_data = {
                    'o': np.array([bar['o'] for bar in bars], dtype=float),  # Open
                    'c': np.array([bar['c'] for bar in bars], dtype=float),  # Close
                    'h': np.array([bar['h'] for bar in bars], dtype=float),  # High
                    'l': np.array([bar['l'] for bar in bars], dtype=float)   # Low
                }
                
                result_dict[symbol] = price_data
                print(f"Данные для {symbol}: {len(bars)} свечей")
                
            else:
                print(f"Предупреждение: Нет данных для символа {symbol}")
                # Создаем объект с пустыми массивами если нет данных
                result_dict[symbol] = {
                    'o': np.array([]),
                    'c': np.array([]),
                    'h': np.array([]),
                    'l': np.array([])
                }
        
        print("\nРезультат:")
        for symbol, price_data in result_dict.items():
            print(f"\n{symbol}:")
            for price_type, array in price_data.items():
                print(f"  {price_type}: {array} (длина: {len(array)})")
            
    else:
        print(f"Ошибка запроса: {response.status_code}")
        print(response.text)
        return {}
    
    return result_dict

if __name__ == "__main__":
    result = main()