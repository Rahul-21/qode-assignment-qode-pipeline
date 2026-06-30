# Qode Assignment - Real-Time Market Intelligence

## Overview
This project collects and analyzes tweets related to the Indian stock market
(#nifty50, #sensex, #intraday, #banknifty) to generate trading signals.

## Architecture
- collector.py → Scrapes tweets using Selenium
- processor.py → Cleans and normalizes data
- storage.py → Stores data in Parquet format
- analysis.py → Converts text into trading signals and plots
- main.py → Orchestrates the pipeline

## Setup
```bash
git clone https://github.com/your-repo/qode-assignment.git
cd qode-assignment
docker-compose build
docker-compose up
