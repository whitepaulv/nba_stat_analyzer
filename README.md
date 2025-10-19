## NBA STAT ANALYZER - Stats + AI summaries for NBA players & teams

Welcome to my NBA stat analysis project! This is a project I made to gain experience working with data and the OpenAI API.

In this project, the user is able to enter a team / player, as well as a specific year, and get information about the selected
palyer / team. This is done through data lookup from the NBA API, as well as OpenAI generated pplayer descriptions.

This project greatly challenged me at first. I had no experience using APIs, so I had to learn how to access data from an API
accurately and without danger of my program generating syntax errors. I also had to learn how to generate responses with a specific
prompt and API key for the OpenAI API.

I am currently a junior majoring in Computer Science at the University of Alabama, developing my skills to hopefully land an
internship in the Computer Science field this summer. Any feedback on this project would be greatly appreciated. I am always
trying to improve wherever I can.

Thank you so much for ckecking my project out!

## Tech Stack  
- Python  
- Streamlit (UI)  
- nba_api (stat retrieval)  
- OpenAI API (summary generation) 

# How to run:
1. Clone the repository  
-bash
-git clone https://github.com/whitepaulv/nba_stat_analyzer.git
-cd nba_stat_analyzer

2. Create a virtual environment
-python3 -m venv venv
-source venv/bin/activate on Mac. On Windows: venv\Scripts\activate
-pip install -r requirements.txt

3. Add your own API key to ai_summary.py

4. Run
-streamlit run app.py



