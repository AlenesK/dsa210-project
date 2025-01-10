# DSA210 Project
Discord Usage Data Analysis

## Motivation
For this project I've wanted to use a source of which I could get the most data about myself. And well, in this day and age it ought to be social media, doesn't it? Except the only social media-like app I use frequently ~~is~~ used to be Discord (up until the day it was banned in our country, of course, since I'm a good citizen :) ). Luckily for me, my Discord data is easily accessible to me, and the diverse nature of text data is perfectly fit for an EDA project! Moreover, by analying how frequently I use Discord, the contents of my messages etc. I could gain insights on my own online behavior.

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

## Project Idea and Plan
The dataset, comprising of text messages and their respective timestamps, is very rich in information, and could be used in many ways. For this project, a simple yet interesting analysis could be in counting and plotting the number of messages in specific intervals of time, i.e. daily, weekly, or monthly. Or based on specific weekdays etc. etc. My null hypothesis would be that there's no significant difference overall.

Something more interesting however, which I'm not sure if it would fall under the scope of this course, thus I'll need to consult with this course's advisors first, would be performing a sentiment analysis over time. This I could then try to relate with bigger events in real life, both global issues, such as major elections, and personal ones, such as the death of loved ones, or the last 2 semesters, in which I had decided to quit university for personal reasons, and as such was on leave for a year. I'd be curious to see how such events reflect on my online behavior. My null hypothis would be the believe I personally hold, which is that there's no significant relation between my online behavior and real life events, as I try not to show much of it.

This concludes the project proposal, I wish you a great day :)
