import json


with open("sample-data.json") as f:
    data = json.load(f)

print("Interface Status")
print("=" * 80)
print(f"{'DN':50} {'Description':20} {'Speed':10} {'MTU'}")
print("-" * 80)


interfaces = data["imdata"]

for item in interfaces:
    attrs = item["l1PhysIf"]["attributes"]

    dn = attrs["dn"]
    descr = attrs.get("descr", "")
    speed = attrs["speed"]
    mtu = attrs["mtu"]

    print(f"{dn:50} {descr:20} {speed:10} {mtu}")
