import requests
import folium
import os

ip_address = input("Введите IP-адрес для OSINT-анализа: ")

print(f"[+] Сбор геоданных для {ip_address}...")
try:
    response = requests.get(f"http://ip-api.com/json/{ip_address}").json()
    
    if response['status'] == 'fail':
        print("[-] Ошибка: Неверный IP или данные не найдены.")
        exit()

    lat = response['lat']
    lon = response['lon']
    country = response['country']
    city = response['city']
    org = response.get('org', 'Неизвестно')

    print(f"[!] Найдено! Страна: {country}, Город: {city}, Провайдер: {org}")
    print(f"[!] Координаты: {lat}, {lon}")

    print("[+] Генерация HTML-карты...")
    my_map = folium.Map(location=[lat, lon], zoom_start=12, tiles='CartoDB positron')
    
    folium.Marker(
        [lat, lon], 
        popup=f"<b>IP:</b> {ip_address}<br><b>Город:</b> {city}<br><b>Орг:</b> {org}",
        tooltip="Кликни для инфо"
    ).add_to(my_map)

    map_file = "osint_result_map.html"
    my_map.save(map_file)
    print(f"[===] Успех! Карта создана и сохранена в файл: {map_file}")
    
except Exception as e:
    print(f"[-] Произошла ошибка: {e}")
