# This file is to check if the messages have been combined successfully

import json

def load_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def count_messages():
    data_files = {
        'DM Messages': 'data/dm_messages.json',
        'Guild Messages': 'data/guild_messages.json',
        'All Messages': 'data/all_messages.json'
    }
    
    for name, filepath in data_files.items():
        try:
            messages = load_json_file(filepath)
            print(f"{name}: {len(messages):,} messages")
        except FileNotFoundError:
            print(f"{name}: File not found ({filepath})")
        except json.JSONDecodeError:
            print(f"{name}: Error reading file ({filepath})")

if __name__ == '__main__':
    count_messages()
