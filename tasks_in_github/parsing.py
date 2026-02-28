import json
import os

def print_interface_status(json_obj):

    print("Interface Status")
    print("=" * 85)

    header = f"{'DN':<50} {'Description':<20} {'Speed':<10} {'MTU'}"
    print(header)
    print(f"{'-' * 49} {'-' * 20} {'-' * 10} {'-' * 6}")

    for item in json_obj.get("imdata", []):
        attr = item.get("l1PhysIf", {}).get("attributes", {})

        dn = attr.get("dn", "")
        descr = attr.get("descr", "")
        speed = attr.get("speed", "")
        mtu = attr.get("mtu", "")

        print(f"{dn:<50} {descr:<20} {speed:<10} {mtu}")

def main():
    file_name = 'sample-data.json'

    if not os.path.exists(file_name):
        print(f"Ошибка: Файл {file_name} не найден в текущей директории.")
        return

    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)

            print_interface_status(data)
            

    except Exception as e:
        print(f"Произошла ошибка: {e}")


main()