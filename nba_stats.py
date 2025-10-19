import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
from openai import OpenAI
from nba_api.stats.endpoints import (
    playercareerstats,
    teaminfocommon,
    teamyearbyyearstats
)
from nba_api.stats.static import players, teams

client = OpenAI(api_key="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")

# This is the global output container that will be used for everything
output_container = st.empty()


# To run, type in 'source venv/bin/activate',
# then run like normal

# NEED TO ADD PROTECTION FROM DIVIDE BY 0 ERROR IF A PLAYER PLAYED 0 GAMES IN A SEASON

def ai_descriptions(ip):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input = ip
    )
    
    return response.output[0].content[0].text

def gp_stat_transformer(stat, gp):
    if (stat == 'STAT NOT PROVIDED' or stat == None) or (gp == 'STAT NOT PROVIDED' or gp == None):
        return '(N.A.)'
    return round(stat / gp, 1)

def stat_transformer(stat):
    if stat == 'STAT NOT PROVIDED' or stat == None:
        return '(N.A.)'
    return stat




def print_player_season(player_list, year):
    formatted_year = year
    
    if not (year.isdigit() and len(year) == 4):
        st.write("Must return a valid season!\n")
        return False
    
    if not int(year) > 0:
        st.write("Must return a valid season!\n")
        return False
    
    year_int = int(year)
    formatted_year = str(year_int - 1) + '-' + str(year_int)[-2:]
        
    if not (len(player_list) == 1):
        st.write('You must enter a valid player and season\n')
        return False
        
    player = player_list[0]
    id = player['id']
    player_career = playercareerstats.PlayerCareerStats(player_id=id)
    career_stats = player_career.get_data_frames()[0]
    
    if not (formatted_year in career_stats["SEASON_ID"].values):
        print('You must enter a valid player and season\n')
        return False
    
    row = career_stats.loc[career_stats["SEASON_ID"] == formatted_year].iloc[0]
    
    points = row['PTS'] if 'PTS' in career_stats.columns else 'STAT NOT PROVIDED'
    rebounds = row['REB'] if 'REB' in career_stats.columns else 'STAT NOT PROVIDED'
    assists = row['AST'] if 'AST' in career_stats.columns else 'STAT NOT PROVIDED'
    steals = row['STL'] if 'STL' in career_stats.columns else 'STAT NOT PROVIDED'
    blocks = row['BLK'] if 'BLK' in career_stats.columns else 'STAT NOT PROVIDED'
    games_played = row['GP'] if 'GP' in career_stats.columns else 'STAT NOT PROVIDED'
    
    description = ai_descriptions((
            f"Write a 100-word summary evaluating {player['full_name']}'s performance in the {formatted_year} season. "
            )
        )
    
    
    st.markdown(f"""
        ### {player['full_name']} — {formatted_year}

        **Averages per Game**
        - {gp_stat_transformer(points, games_played)} points  
        - {gp_stat_transformer(rebounds, games_played)} rebounds  
        - {gp_stat_transformer(assists, games_played)} assists  
        - {gp_stat_transformer(steals, games_played)} steals  
        - {gp_stat_transformer(blocks, games_played)} blocks  

        **Season Totals**
        - {stat_transformer(points)} points  
        - {stat_transformer(rebounds)} rebounds  
        - {stat_transformer(assists)} assists  
        - {stat_transformer(steals)} steals  
        - {stat_transformer(blocks)} blocks  
        - {stat_transformer(games_played)} games played  

        {description}
        """)
    
            
        

    

def print_player_career(player_list):
    if len(player_list) == 1:
        player = player_list[0]
        id = player['id']
        player_career = playercareerstats.PlayerCareerStats(player_id=id)
        career_stats = player_career.get_data_frames()[1]
        
        points = career_stats['PTS'].values[0] if 'PTS' in career_stats else 'STAT NOT PROVIDED'
        rebounds = career_stats['REB'].values[0] if 'REB' in career_stats else 'STAT NOT PROVIDED'
        assists = career_stats['AST'].values[0] if 'AST' in career_stats else 'STAT NOT PROVIDED'
        steals = career_stats['STL'].values[0] if 'STL' in career_stats else 'STAT NOT PROVIDED'
        blocks = career_stats['BLK'].values[0] if 'BLK' in career_stats else 'STAT NOT PROVIDED'
        games_played = career_stats['GP'].values[0] if 'GP' in career_stats else 'STAT NOT PROVIDED'
        
        description = ai_descriptions((
            f"Write a 100-word summary evaluating {player['full_name']}'s career"
            )
        )
        
        st.markdown(f"""
            ### {player['full_name']}

            **Averages per Game**  
            - {gp_stat_transformer(points, games_played)} points  
            - {gp_stat_transformer(rebounds, games_played)} rebounds  
            - {gp_stat_transformer(assists, games_played)} assists  
            - {gp_stat_transformer(steals, games_played)} steals  
            - {gp_stat_transformer(blocks, games_played)} blocks  

            **Career Totals**  
            - {stat_transformer(points)} points  
            - {stat_transformer(rebounds)} rebounds  
            - {stat_transformer(assists)} assists  
            - {stat_transformer(steals)} steals  
            - {stat_transformer(blocks)} blocks  
            - {stat_transformer(games_played)} career games played  

            {description}
            """)
    else:
        st.markdown('You must enter a valid player\n')





def print_team_season(team_list, year):
    formatted_year = year
    
    if not (year.isdigit() and len(year) == 4):
        st.write("Must return a valid season!\n")
        return 
    
    if not int(year) > 0:
        st.write("Must return a valid season!\n")
        return 
    
    if not (len(team_list) == 1):
        st.write('You must enter a valid team and season\n')
        return 
    
    year_int = int(year)
    formatted_year = str(year_int - 1) + '-' + str(year_int)[-2:]
    team = team_list[0]
    team_id = team['id']
    
    team_stats = teamyearbyyearstats.TeamYearByYearStats(team_id=team_id).get_data_frames()[0]
    row = team_stats.loc[team_stats["YEAR"] == formatted_year].iloc[0]
    
    wins = row['WINS'] if 'WINS' in team_stats else 'STAT NOT PROVIDED'
    losses = row['LOSSES'] if 'LOSSES' in team_stats else 'STAT NOT PROVIDED'
    win_percent = (row['WIN_PCT'] * 100) if 'WIN_PCT' in team_stats else 'STAT NOT PROVIDED'
    playoff_wins = row['PO_WINS'] if 'PO_WINS' in team_stats else 'STAT NOT PROVIDED'
    playoff_losses = row['PO_LOSSES'] if 'PO_LOSSES' in team_stats else 'STAT NOT PROVIDED'
    pts_rank = row['PTS_RANK'] if 'PTS_RANK' in team_stats else 'STAT NOT PROVIDED'
    fgm = row['FGM'] if 'WINS' in team_stats else 'STAT NOT PROVIDED'
    fga = row['FGA'] if 'WINS' in team_stats else 'STAT NOT PROVIDED'
    fg3m = row['FG3M'] if 'FG3M' in team_stats else 'STAT NOT PROVIDED'
    fg3a = row['FG3A'] if 'FG3A' in team_stats else 'STAT NOT PROVIDED'
    
    description = ai_descriptions((
            f"Write a 100-word summary evaluating {team}'s performance in the {formatted_year} season. "
            )
        )
    
    
    
    # Protect against divide by 0 errors
    for val in [fga, fg3a]:
        val = 1 if val == 0 else val
    
    fg = round((fgm / fga) * 100, 1)
    fg3 = round((fg3m / fg3a) * 100, 1)
    
    st.markdown(f"""
        ### {team['full_name']}

        **Season Overview:**  
        - {stat_transformer(wins)} wins  
        - {stat_transformer(losses)} losses  
        - {stat_transformer(win_percent)}% win rate  
        - {stat_transformer(playoff_wins)} playoff wins  
        - {stat_transformer(playoff_losses)} playoff losses  
        - #{stat_transformer(pts_rank)} ranked offense  
        - {stat_transformer(fg)} FG%  
        - {stat_transformer(fg3)} 3PT FG%  

        {description}
        """)

    

def print_team_history(team_list):
    
    if not (len(team_list) == 1):
        st.write('You must enter a valid team and season\n')
        return 

    team = team_list[0]
    team_id = team['id']
    
    team_history = teaminfocommon.TeamInfoCommon(team_id=team_id)
    history_stats = team_history.get_data_frames()[0]

    conference = history_stats['TEAM_CONFERENCE'].values[0] if 'TEAM_CONFERENCE' in history_stats else 'STAT NOT PROVIDED'
    division = history_stats['TEAM_DIVISION'].values[0] if 'TEAM_DIVISION' in history_stats else 'STAT NOT PROVIDED'
    created = history_stats['MIN_YEAR'].values[0] if 'MIN_YEAR' in history_stats else 'STAT NOT PROVIDED'
    years = (2025 - int(created)) if 'MIN_YEAR' in history_stats else 'STAT NOT PROVIDED'
        
    description = ai_descriptions((
            f"Write a 100-word summary evaluating {team}'s history."
            )
        )

    st.markdown(f"""
        ### {team['full_name']} Info

        **Franchise Details:**  
        - {conference} Conference  
        - {division} Division  
        - **Year Introduced:** {created}  
        - **Years Existed:** {years}  

        {description}
        """)

    


def main():
                    
    st.title("🏀 NBA Stats Lookup")
    selection_type = st.selectbox("Select type:", ["Player", "Team"])
    name = st.text_input("Please enter a player/team's full name:")   
    year = st.text_input("Please enter a specific year, or enter 'career' for career info:")
    
    
    if st.button("Search"):
    
        if selection_type == 'Player': #For players
            selected_player = players.find_players_by_full_name(name)

            if year.isnumeric() or year == 'career':
                if year.isnumeric():
                    st.markdown("**Loading...**")
                    print_player_season(selected_player, year)
                else:
                    print_player_career(selected_player)
                    
                    
        else: # For teams
            selected_team = teams.find_teams_by_full_name(name)
            if year.isnumeric() or year == 'career':
                if year.isnumeric():
                    print_team_season(selected_team, year)
                else:
                    print_team_history(selected_team)
                    
    
    
main()    