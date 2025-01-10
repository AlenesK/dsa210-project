# DSA210 Project
Discord Sentiment Analysis

Website for presentation: <>

## Motivation
For this project I've wanted to use a source of which I could get the most data about myself. And well, in this day and age it ought to be social media, doesn't it? Except the only social media-like app I use frequently ~~is~~ used to be Discord (up until the day it was banned in our country, of course, since I'm a good citizen :) ). Luckily, my Discord data is easily accessible to me, and the diverse nature of text data is perfectly fit for an EDA project! I've wanted to make good use of said diversity, and thus decided to focus on sentiment analysis for this project. Moreover, this would provide some curious results for myself as I'd learn more about my own online behavior.

## Dataset
The data was directly obtained through a request to Discord, and includes all messages I've ever sent, with the following properties:
- Content: This is the raw text I sent
- Timestamp: Date and time of sending the message
- Attachments: Images or other media I might have included in the message
- ID: Unique message ID for each message I've sent
- Type: Either "Guild" or "DM"
  - If Guild:
    - Guild Name: Name of the server the message was sent in
    - Guild ID: Unique ID of the server the message was sent in
  - If DM:
    - Recipients: Unique user ID's of the recipients

## Data Processing
The relevant parts from the Data I've obtained for this project were the message contents, timestamps and channels the messages were sent in. So the first step was to prune the rest of the data, and combine the remaining ones into unified files that would be easier to work with (since, in the raw data package, messages were categorized by channel).
The next step was to perform the sentiment analysis on each message (almost 500k of them!) and store the results together with the messages. I've used the [TextBlob](https://textblob.readthedocs.io/en/dev/) python library to achieve this.

## Visualization
Lastly I needed to visualize the resulting dataset so that I could make sense of it and draw conclusions. I've used the [matplotlib](https://matplotlib.org/) and [seaborn](https://seaborn.pydata.org/) libraries to create graphs for the final presentation, but moreover, I've created some interactive charts on my website (link above) which you can use to explore my data yourself!





