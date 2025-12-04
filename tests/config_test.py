import yaml, json, os

print("Files in config/:", os.listdir("config"))

settings_files = [
    "config/settings.yaml",
    "config/settings.json"
]

for f in settings_files:
    if os.path.exists(f):
        print(f"Found:", f)
        try:
            if f.endswith(".yaml"):
                cfg = yaml.safe_load(open(f))
            else:
                cfg = json.load(open(f))
            print("Loaded OK. Top-level keys:", list(cfg.keys()))
        except Exception as e:
            print("ERROR loading", f, e)
    else:
        print("Missing:", f)
