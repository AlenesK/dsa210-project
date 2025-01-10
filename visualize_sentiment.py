import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from pandas._libs.tslibs.np_datetime import OutOfBoundsDatetime
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

plt.style.use('seaborn')
sns.set_palette("husl")

def load_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def ensure_dir(directory):
    os.makedirs(directory, exist_ok=True)

def create_time_series_df(data):
    df = pd.DataFrame(data['time_series'])
    
    if all(str(x).isdigit() for x in df['date'].unique()):
        df['date'] = df['date'].astype(int)
        return df
        
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    if any(day in weekdays for day in df['date'].unique()):
        df['date'] = pd.Categorical(df['date'], categories=weekdays, ordered=True)
        return df
        
    try:
        df['date'] = pd.to_datetime(df['date'])
    except Exception as e:
        raise
    
    return df

def plot_sentiment_distribution(data, period, file_type, output_dir):
    """Pie chart of positive/negative/neutral distribution"""
    stats = data['overall_stats']
    labels = ['Positive', 'Negative', 'Neutral']
    sizes = [stats['positive_count'], stats['negative_count'], stats['neutral_count']]
    
    colors = ['#2ecc71', '#e74c3c', '#bdc3c7']
    
    plt.figure(figsize=(12, 8), facecolor='white')
    
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
            startangle=90, pctdistance=0.85,
            wedgeprops=dict(width=0.7, edgecolor='white', linewidth=2))
    
    plt.title(f'Sentiment Distribution - {file_type}\n({period})', 
             pad=20, fontsize=14, fontweight='bold')
    
    total = sum(sizes)
    plt.text(0, 0, f'Total\n{total:,}', 
             ha='center', va='center', fontsize=12, fontweight='bold')
    
    plt.axis('equal')
    
    plt.legend(labels, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))
    
    plt.tight_layout()
    
    plt.savefig(f'{output_dir}/distribution/sentiment_distribution_{file_type}_{period}.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

def plot_hourly_patterns(df, file_type, output_dir):
    """Heatmap of sentiment patterns by hour"""
    if isinstance(df['date'].dtype, (np.int64, np.int32, int)):
        plt.figure(figsize=(12, 6))
        
        sns.barplot(x=df['date'], y=df['average_polarity'])
        
        plt.title(f'Average Sentiment by Hour - {file_type}')
        plt.xlabel('Hour of Day')
        plt.ylabel('Average Polarity')
        
        plt.xticks(range(24), [f'{hour:02d}:00' for hour in range(24)])
        plt.xticks(rotation=45)
        
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/patterns/hourly_sentiment_{file_type}.png')
        plt.close()

def plot_weekday_patterns(df, file_type, output_dir):
    """Weekday sentiment patterns"""
    if isinstance(df['date'].dtype, pd.CategoricalDtype):
        plt.figure(figsize=(12, 6))
        sns.boxplot(x='date', y='average_polarity', data=df)
        plt.title(f'Sentiment Distribution by Weekday - {file_type}')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/patterns/weekday_sentiment_{file_type}.png')
        plt.close()

def plot_sentiment_correlation(df, file_type, output_dir):
    """Scatter plot of polarity vs subjectivity"""
    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=df, x='average_polarity', y='average_subjectivity', 
                    size='message_count', sizes=(50, 500), alpha=0.6)
    plt.title(f'Sentiment Polarity vs Subjectivity - {file_type}')
    plt.xlabel('Average Polarity')
    plt.ylabel('Average Subjectivity')
    plt.savefig(f'{output_dir}/correlation/polarity_subjectivity_{file_type}.png')
    plt.close()

def plot_sentiment_momentum(df, file_type, output_dir):
    """Line plot showing sentiment momentum (rate of change)"""
    # Skip if data is weekday-based
    if isinstance(df['date'].dtype, pd.CategoricalDtype):
        return
        
    # Skip if data is hourly
    if isinstance(df['date'].dtype, np.int64) or isinstance(df['date'].dtype, int):
        return
        
    df['sentiment_momentum'] = df['total_sentiment_count'].diff()
    
    plt.figure(figsize=(12, 6))
    plt.plot(df['date'], df['sentiment_momentum'], color='#3498db')
    plt.title(f'Sentiment Momentum - {file_type}')
    plt.xlabel('Date')
    plt.ylabel('Sentiment Change Rate')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/momentum/sentiment_momentum_{file_type}.png')
    plt.close()

def plot_sentiment_volatility(df, file_type, output_dir):
    """Plot showing how much sentiment fluctuates over time"""
    # Skip if data is weekday-based or hourly
    if isinstance(df['date'].dtype, pd.CategoricalDtype) or \
       isinstance(df['date'].dtype, (np.int64, int)):
        return
        
    window = 7  # 7-day window
    df['sentiment_volatility'] = df['average_polarity'].rolling(window).std()
    
    plt.figure(figsize=(12, 6))
    plt.plot(df['date'], df['sentiment_volatility'], color='#9b59b6', linewidth=2)
    plt.title(f'Sentiment Volatility ({window}-day rolling) - {file_type}')
    plt.xlabel('Date')
    plt.ylabel('Sentiment Volatility')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/volatility/sentiment_volatility_{file_type}.png')
    plt.close()

def plot_volume_sentiment_relationship(df, file_type, output_dir):
    """Bubble chart showing relationship between message volume and sentiment"""
    plt.figure(figsize=(12, 8))
    
    plt.scatter(df['message_count'], 
               df['average_polarity'],
               s=df['average_subjectivity']*500,  # Size based on subjectivity
               alpha=0.6,
               c=df['total_sentiment_count'],  # Color based on net sentiment
               cmap='RdYlBu')
    
    plt.colorbar(label='Net Sentiment')
    plt.title(f'Message Volume vs Sentiment - {file_type}')
    plt.xlabel('Message Count')
    plt.ylabel('Average Polarity')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/relationship/volume_sentiment_{file_type}.png')
    plt.close()

def plot_weekly_heatmap(file_types, output_dir):
    """Create heatmap showing sentiment patterns across days and hours"""
    try:
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        hours = [f"{hour:02d}" for hour in range(24)]
        
        for file_type in file_types:
            try:
                # Load the day_hour data directly
                data = load_json_file(f'data/sentiment/{file_type}_sentiment_day_hour.json')
                df = pd.DataFrame(data['time_series'])
                
                # Create pivot table for heatmap
                heatmap_data = pd.pivot_table(
                    df,
                    values='average_polarity',
                    index='weekday',
                    columns='hour',
                    aggfunc='mean'
                ).reindex(weekday_order)
                
                # Create both adjusted and fixed-range versions
                for version in ['adjusted', 'fixed']:
                    # Set up color scheme and range based on version
                    if version == 'adjusted':
                        vmin = heatmap_data.min().min()
                        vmax = heatmap_data.max().max()
                        colors = ['#ffffff', '#e3f2fd', '#90caf9', '#42a5f5', '#1976d2', '#0d47a1']
                        title_extra = "(Darker blue indicates more positive sentiment)"
                    else:
                        vmin = -1
                        vmax = 1
                        # Stronger red and green with yellowish-green transition
                        colors = ['#ff0000', '#ff4d00', '#ffb300', '#c6e03c', '#7ab800', '#2d8600', '#004d00']
                        title_extra = "(Red = Negative, Green = Positive)"
                    
                    # Create custom colormap
                    n_bins = 100
                    custom_cmap = LinearSegmentedColormap.from_list("custom", colors, N=n_bins)
                    
                    # Create figure
                    plt.figure(figsize=(20, 10))
                    
                    # Create heatmap
                    sns.heatmap(
                        heatmap_data,
                        cmap=custom_cmap,
                        vmin=vmin,
                        vmax=vmax,
                        annot=True,
                        fmt='.3f',
                        annot_kws={'size': 8},
                        square=True,
                        cbar_kws={
                            'label': 'Average Sentiment Polarity',
                            'format': '%.3f'
                        }
                    )
                    
                    plt.title(f'Weekly Sentiment Patterns - {file_type}\n{title_extra}', 
                             pad=20)
                    plt.xlabel('Hour of Day')
                    plt.ylabel('Day of Week')
                    
                    # Add text showing the value range
                    plt.figtext(0.02, 0.02, f'Value range: {vmin:.3f} to {vmax:.3f}', 
                               fontsize=8, style='italic')
                    
                    plt.tight_layout()
                    plt.savefig(f'{output_dir}/patterns/weekly_heatmap_{file_type}_{version}.png', 
                              dpi=300, bbox_inches='tight')
                    plt.close()
                    
                    print(f"Created {version} weekly heatmap for {file_type}")
                    print(f"Value range: {vmin:.3f} to {vmax:.3f}")
                
            except Exception as e:
                print(f"Error processing {file_type}: {str(e)}")
                continue
                
    except Exception as e:
        print(f"Error creating weekly heatmap: {str(e)}")

def plot_sentiment_over_time(df, file_type, period, output_dir, include_neutral=True, as_percentage=False):
    """Stacked area chart showing sentiment over time, with options for neutral inclusion and percentage view"""
    # Skip if data is weekday-based or hourly
    if isinstance(df['date'].dtype, pd.CategoricalDtype) or \
       isinstance(df['date'].dtype, (np.int64, int)):
        return
        
    # Create figure with white background
    plt.figure(figsize=(15, 8), facecolor='white')
    
    # Modern color palette (same as distribution chart for consistency)
    colors = ['#2ecc71', '#e74c3c', '#bdc3c7']
    
    if as_percentage:
        # Calculate percentages
        total = df['positive_count'] + df['negative_count']
        data = [100 * df['positive_count'] / total, 
                100 * df['negative_count'] / total]
        labels = ['Positive %', 'Negative %']
        colors = colors[:2]  # Only use green and red
        subfolder = 'timeline_percentage'
        ylabel = 'Percentage of Messages'
    else:
        if include_neutral:
            data = [df['positive_count'], df['negative_count'], df['neutral_count']]
            labels = ['Positive', 'Negative', 'Neutral']
            subfolder = 'timeline_with_neutral'
        else:
            data = [df['positive_count'], df['negative_count']]
            labels = ['Positive', 'Negative']
            colors = colors[:2]  # Only use green and red
            subfolder = 'timeline_without_neutral'
        ylabel = 'Message Count'
    
    # Create stacked area chart
    plt.stackplot(df['date'],
                 data,
                 labels=labels,
                 colors=colors,
                 alpha=0.8)
    
    # Customize title based on version
    if as_percentage:
        title_extra = " (As Percentage)"
    else:
        title_extra = "" if include_neutral else " (Excluding Neutral)"
    
    plt.title(f'Sentiment Trends Over Time - {file_type}{title_extra}\n({period})', 
             pad=20, fontsize=14, fontweight='bold')
    plt.xlabel('Time')
    plt.ylabel(ylabel)
    
    # For percentage view, set y-axis limits to 0-100
    if as_percentage:
        plt.ylim(0, 100)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Add grid for better readability
    plt.grid(True, alpha=0.3)
    
    # Add legend
    plt.legend(loc='upper left')
    
    plt.tight_layout()
    
    # Save with high DPI for better quality
    plt.savefig(f'{output_dir}/{subfolder}/sentiment_timeline_{file_type}_{period}.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

def main():
    # Create output directories
    base_dir = 'graphs'
    subdirs = ['distribution', 'patterns', 'correlation', 'momentum',
               'volatility', 'relationship', 'timeline_with_neutral',
               'timeline_without_neutral', 'timeline_percentage']  # Added percentage subfolder
    for subdir in subdirs:
        ensure_dir(os.path.join(base_dir, subdir))

    file_types = ['dm_messages', 'guild_messages', 'all_messages']
    periods = ['day', 'month', 'weekday', 'hour']

    for file_type in file_types:
        print(f"\nProcessing visualizations for {file_type}...")
        
        # Generate distribution plot only once per file_type using day period
        try:
            data = load_json_file(f'data/sentiment/{file_type}_sentiment_day.json')
            plot_sentiment_distribution(data, "Overall", file_type, base_dir)
        except FileNotFoundError:
            print(f"File not found: data/sentiment/{file_type}_sentiment_day.json")
        
        # Continue with other visualizations for all periods
        for period in periods:
            try:
                data = load_json_file(f'data/sentiment/{file_type}_sentiment_{period}.json')
                df = create_time_series_df(data)
                
                # Generate visualizations
                plot_sentiment_correlation(df, file_type, base_dir)
                plot_sentiment_momentum(df, file_type, base_dir)
                plot_sentiment_volatility(df, file_type, base_dir)
                plot_volume_sentiment_relationship(df, file_type, base_dir)
                # Create all three versions of the timeline charts
                plot_sentiment_over_time(df, file_type, period, base_dir, include_neutral=True)
                plot_sentiment_over_time(df, file_type, period, base_dir, include_neutral=False)
                plot_sentiment_over_time(df, file_type, period, base_dir, include_neutral=False, as_percentage=True)
                
                # Period-specific visualizations
                if period == 'hour':
                    plot_hourly_patterns(df, file_type, base_dir)
                elif period == 'weekday':
                    plot_weekday_patterns(df, file_type, base_dir)

            except FileNotFoundError:
                print(f"File not found: data/sentiment/{file_type}_sentiment_{period}.json")

    # Create weekly heatmaps
    plot_weekly_heatmap(file_types, base_dir)

if __name__ == '__main__':
    main() 