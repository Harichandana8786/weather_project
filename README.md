# 🌦️ Weather Data Pipeline (AWS + Snowflake)

## 📌 Project Overview
This project builds a real-time data pipeline using AWS and Snowflake.

## 🔧 Architecture
EventBridge → Lambda → DynamoDB → Stream → Lambda → S3 → Snowpipe → Snowflake

## ⚙️ Technologies Used
- AWS Lambda
- DynamoDB
- S3
- EventBridge
- Snowflake
- Python

## 🚀 Features
- Fetches weather data every 10 minutes
- Stores data in S3
- Automatically loads into Snowflake
- Fully automated pipeline

## 📊 Output
Weather data (city, time, temperature, humidity, weather)

## 👩‍💻 Author
Harichandana Tk