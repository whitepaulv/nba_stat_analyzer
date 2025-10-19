import streamlit as st
from nba_api.stats.endpoints import (
playercareerstats, 
teamyearbyyearstats, 
teaminfocommon
)
import datetime as dt

# ----- Helpers ----- #

# Helpers for formatting and validating years

def format_season(year_str): # returns a year that can be searched by the nba_api
    y = int(year_str)
    return f"{y-1}-{str(y)[-2:]}"

def validate_year(year_str):
    y = int(year_str)
    return 1947 <= y <= dt.date.today().year # This ensures a date is not outside the range of the nba's history


# Helpers for formatting stats

def gp_stat_transformer(stat, gp):
    if (stat == 'STAT NOT PROVIDED' or stat == None) or (gp == 'STAT NOT PROVIDED' or gp == None):
        return '(N.A.)'
    return round(stat / gp, 1)

def stat_transformer(stat):
    if stat == 'STAT NOT PROVIDED' or stat == None:
        return '(N.A.)'
    return stat

# The rest of the functions below are used to look up players or teams with the API.

# ----- Players ----- # 


# Data is cached so look ups will be faster if repeated
@st.cache_data
def get_player_season_stats(player_id, formatted_year):
    player_career = playercareerstats.PlayerCareerStats(player_id=player_id)
    career_stats = player_career.get_data_frames()[0]
    if formatted_year not in career_stats["SEASON_ID"].values:
        return None
    return career_stats.loc[career_stats["SEASON_ID"] == formatted_year].iloc[0]
    

@st.cache_data
def get_player_career_totals(player_id):
    player_career = playercareerstats.PlayerCareerStats(player_id=player_id)
    return player_career.get_data_frames()[1]
    
    
# ----- Teams ----- #  
   
@st.cache_data
def get_team_season_stats(team_id, formatted_year):
    team_stats = teamyearbyyearstats.TeamYearByYearStats(team_id=team_id).get_data_frames()[0]
    if formatted_year not in team_stats["YEAR"].values:
        return None 
    return team_stats.loc[team_stats["YEAR"] == formatted_year].iloc[0]


@st.cache_data
def get_team_history(team_id):
    team_history = teaminfocommon.TeamInfoCommon(team_id=team_id)
    return team_history.get_data_frames()[0]
