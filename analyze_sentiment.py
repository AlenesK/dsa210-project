from textblob import TextBlob
import json
import os
from datetime import datetime
from tqdm import tqdm
from collections import defaultdict

def load_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_file(filepath, data):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_time_period(timestamp, period='day'):
    date = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    if period == 'day':
        return date.strftime('%Y-%m-%d')
    elif period == 'month':
        return date.strftime('%Y-%m')
    elif period == 'year':
        return date.strftime('%Y')
    elif period == 'weekday':
        return date.strftime('%A')  # Full weekday name
    elif period == 'hour':
        return date.strftime('%H')  # 24-hour format
    elif period == 'day_hour':  # New period type
        return {
            'weekday': date.strftime('%A'),
            'hour': date.strftime('%H')
        }
    return date.strftime('%Y-%m-%d')

def analyze_messages(messages, period='day'):
    # Overall statistics
    overall_stats = {
        'message_count': len(messages),
        'positive_count': 0,
        'negative_count': 0,
        'neutral_count': 0,
        'total_sentiment_count': 0,
        'average_polarity': 0,
        'average_subjectivity': 0
    }
    
    # Modified time series structure for day_hour period
    if period == 'day_hour':
        time_series = defaultdict(lambda: defaultdict(lambda: {
            'message_count': 0,
            'positive_count': 0,
            'negative_count': 0,
            'neutral_count': 0,
            'total_sentiment_count': 0,
            'total_polarity': 0,
            'total_subjectivity': 0,
            'messages': []
        }))
    else:
        time_series = defaultdict(lambda: {
            'message_count': 0,
            'positive_count': 0,
            'negative_count': 0,
            'neutral_count': 0,
            'total_sentiment_count': 0,
            'total_polarity': 0,
            'total_subjectivity': 0,
            'messages': []
        })
    
    print("Analyzing messages...")
    for message in tqdm(messages):
        if not message['Contents']:  # Skip empty messages
            continue
        
        # Perform sentiment analysis
        analysis = TextBlob(message['Contents'])
        polarity = analysis.sentiment.polarity
        subjectivity = analysis.sentiment.subjectivity
        
        # Get time period
        time_key = get_time_period(message['Timestamp'], period)
        
        # Update overall statistics
        if polarity > 0:
            overall_stats['positive_count'] += 1
            overall_stats['total_sentiment_count'] += 1
        elif polarity < 0:
            overall_stats['negative_count'] += 1
            overall_stats['total_sentiment_count'] -= 1
        else:
            overall_stats['neutral_count'] += 1
        
        # Update time series data
        if period == 'day_hour':
            weekday = time_key['weekday']
            hour = time_key['hour']
            period_data = time_series[weekday][hour]
        else:
            period_data = time_series[time_key]
            
        period_data['message_count'] += 1
        period_data['total_polarity'] += polarity
        period_data['total_subjectivity'] += subjectivity
        
        if polarity > 0:
            period_data['positive_count'] += 1
            period_data['total_sentiment_count'] += 1
        elif polarity < 0:
            period_data['negative_count'] += 1
            period_data['total_sentiment_count'] -= 1
        else:
            period_data['neutral_count'] += 1
        
        # Store message with sentiment
        message_with_sentiment = message.copy()
        message_with_sentiment.update({
            'polarity': polarity,
            'subjectivity': subjectivity
        })
        period_data['messages'].append(message_with_sentiment)
    
    # Calculate averages for overall stats
    msg_count = overall_stats['message_count']
    if period == 'day_hour':
        total_polarity = sum(data['total_polarity'] 
                           for weekday in time_series.values() 
                           for data in weekday.values())
        total_subjectivity = sum(data['total_subjectivity'] 
                               for weekday in time_series.values() 
                               for data in weekday.values())
    else:
        total_polarity = sum(data['total_polarity'] for data in time_series.values())
        total_subjectivity = sum(data['total_subjectivity'] for data in time_series.values())
    
    overall_stats['average_polarity'] = total_polarity / msg_count if msg_count > 0 else 0
    overall_stats['average_subjectivity'] = total_subjectivity / msg_count if msg_count > 0 else 0
    
    # Convert time series to sorted list and calculate averages
    time_series_list = []
    if period == 'day_hour':
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        hours = [f"{h:02d}" for h in range(24)]
        
        for weekday in weekdays:
            for hour in hours:
                if weekday in time_series and hour in time_series[weekday]:
                    data = time_series[weekday][hour]
                    period_count = data['message_count']
                    if period_count > 0:
                        time_series_list.append({
                            'weekday': weekday,
                            'hour': hour,
                            'message_count': period_count,
                            'positive_count': data['positive_count'],
                            'negative_count': data['negative_count'],
                            'neutral_count': data['neutral_count'],
                            'total_sentiment_count': data['total_sentiment_count'],
                            'average_polarity': data['total_polarity'] / period_count,
                            'average_subjectivity': data['total_subjectivity'] / period_count
                        })
                else:
                    # Add empty data for missing time slots
                    time_series_list.append({
                        'weekday': weekday,
                        'hour': hour,
                        'message_count': 0,
                        'positive_count': 0,
                        'negative_count': 0,
                        'neutral_count': 0,
                        'total_sentiment_count': 0,
                        'average_polarity': 0,
                        'average_subjectivity': 0
                    })
    else:
        for date, data in sorted(time_series.items()):
            period_count = data['message_count']
            if period_count > 0:
                time_series_list.append({
                    'date': date,
                    'message_count': period_count,
                    'positive_count': data['positive_count'],
                    'negative_count': data['negative_count'],
                    'neutral_count': data['neutral_count'],
                    'total_sentiment_count': data['total_sentiment_count'],
                    'average_polarity': data['total_polarity'] / period_count,
                    'average_subjectivity': data['total_subjectivity'] / period_count
                })
    
    return {
        'overall_stats': overall_stats,
        'time_series': time_series_list
    }

def main():
    periods = ['day', 'month', 'weekday', 'hour', 'day_hour']  # Added day_hour
    file_types = ['dm_messages', 'guild_messages', 'all_messages']
    
    for file_type in file_types:
        print(f"\nAnalyzing {file_type}...")
        try:
            messages = load_json_file(f'data/raw/{file_type}.json')
            
            for period in periods:
                results = analyze_messages(messages, period)
                save_json_file(f'data/sentiment/{file_type}_sentiment_{period}.json', results)
                
                # Print summary
                stats = results['overall_stats']
                print(f"\nResults for {file_type} (by {period}):")
                print(f"Total messages: {stats['message_count']:,}")
                print(f"Positive messages: {stats['positive_count']:,}")
                print(f"Negative messages: {stats['negative_count']:,}")
                print(f"Neutral messages: {stats['neutral_count']:,}")
                print(f"Average polarity: {stats['average_polarity']:.3f}")
                print(f"Average subjectivity: {stats['average_subjectivity']:.3f}")
                
        except FileNotFoundError:
            print(f"File not found: data/raw/{file_type}.json")

if __name__ == '__main__':
    main() 