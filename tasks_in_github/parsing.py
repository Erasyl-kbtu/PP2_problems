import json
import os

file_path = r"C:\Users\Erasyl\OneDrive\Desktop\PP2_problems\tasks_in_github\sample-data.json" 

with open(file_path, 'r') as f:
    data = json.load(f)

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
    

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            print_interface_status(data)
            

    except Exception as e:
        print(f"Произошла ошибка: {e}")


main()