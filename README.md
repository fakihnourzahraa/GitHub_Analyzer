# GitHub Analyzer 🔍

A CLI tool that analyzes any GitHub profile and gives you AI-powered feedback based on job requirements. Enter a username, copy paste the job requirements, and get an honest breakdown of how strong the profile is, and what to improve.

## Features
- 📊 Displays top repositories sorted by stars
- 🏆 Shows language breakdown across all repos
- 🤖 AI analysis powered by Groq (Llama 3.3)
- ⚡ Fast and runs entirely in your terminal

## Requirements
- Python 3.8+
- A free Groq API key → https://console.groq.com

## Installation

1. Clone the repo:
   git clone https://github.com/fakihnourzahraa/GitHub_Analyzer.git
   cd GitHub-Analyzer

2. Install dependencies:
   pip install -r requirements.txt

3. Create an .env file

4. Add your Groq API key to .env:
   API_KEY=your-groq-key-here

## Usage
   python3 main.py

Then enter any GitHub username and a job description when prompted.

## Example
   Enter GitHub username: torvalds
   Enter job requirements: Linux kernel development, C, low level systems

## Tech Stack
- Python
- Groq API (Llama 3.3 70B)
- Rich — terminal formatting(fun colors)
- GitHub REST API

*Made with lots coffee and debugging*