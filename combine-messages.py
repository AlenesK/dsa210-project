import json
import os
from datetime import datetime

def load_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_file(filepath, data):
    # Create data/raw folder if not exists
    os.makedirs('data/raw', exist_ok=True)
    
    full_path = os.path.join('data/raw', filepath)
    
    with open(full_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def combine_messages():
    dm_messages = []
    guild_messages = []
    all_messages = []
    
    # Define cutoff date
    cutoff_date = datetime.strptime('2024-09-30 23:59:59', '%Y-%m-%d %H:%M:%S')
    
    # Walk through all folders in ./messages
    # Folder Structure:
    # ./messages/
    #   - c<channel_id>/
    #     - channel.json
    #     - messages.json
    #   - ...
    for root, dirs, files in os.walk('./messages'):
        if 'channel.json' in files and 'messages.json' in files:
            # Load channel info and messages
            channel_path = os.path.join(root, 'channel.json')
            messages_path = os.path.join(root, 'messages.json')
            
            channel_info = load_json_file(channel_path)
            messages = load_json_file(messages_path)
            
            # Filter messages before adding to lists
            filtered_messages = [
                msg for msg in messages 
                if datetime.strptime(msg['Timestamp'], '%Y-%m-%d %H:%M:%S') <= cutoff_date
            ]
            
            # Add filtered messages to lists
            if channel_info.get('type') == 'DM':
                dm_messages.extend(filtered_messages)
            else:
                guild_messages.extend(filtered_messages)
            all_messages.extend(filtered_messages)
    
    # Sort messages by timestamp
    def sort_by_timestamp(msg):
        return datetime.strptime(msg['Timestamp'], '%Y-%m-%d %H:%M:%S')
    
    dm_messages.sort(key=sort_by_timestamp)
    guild_messages.sort(key=sort_by_timestamp)
    all_messages.sort(key=sort_by_timestamp)
    
    # Save files
    save_json_file('dm_messages.json', dm_messages)
    save_json_file('guild_messages.json', guild_messages)
    save_json_file('all_messages.json', all_messages)

if __name__ == '__main__':
    combine_messages()
    print("Combined and sorted messages successfully!")