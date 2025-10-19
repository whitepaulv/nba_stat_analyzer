import streamlit as st
from nba_api.stats.static import players, teams
from nba_data import (
    gp_stat_transformer, stat_transformer, get_player_season_stats, 
    get_player_career_totals, get_team_season_stats, get_team_history,
    validate_year, format_season
)
from ai_summary import ai_descriptions

# This is the file with the logic for the UI and which funcitons to call.


# To run, type in 'source venv/bin/activate',
# then run with streamlit run app.py
    


def main():

# First, get all the important data                     
    st.title("🏀 NBA Stats Lookup")
    
    selection_type = st.selectbox("Select type:", ["Player", "Team"])
    name = st.text_input("Please enter a player/team's full name:").strip() 
    year = st.text_input("Please enter a specific year, or enter 'career' for career info:").strip()
    st.markdown("Note: player's real names will need to be entered, **not nicknames!**\n"
                "Example: Steph Curry will need to be entered as **Stephen Curry**.")
        
# When the search button is pressed
    if st.button("Search"):
        st.session_state.output = st.empty()
        
# for 'Player' selection
        if selection_type == 'Player':
            selected_player = players.find_players_by_full_name(name)
            
# 'no player found'
            if len(selected_player) == 0:
                 st.session_state.output.error("No player found.")
# initiate player            
            else:
                player = selected_player[0]
                
# if year is properly formatted, get the needed info and output
                if year.isnumeric() and validate_year(year):
                    formatted_year = format_season(year)
                    row = get_player_season_stats(player['id'], formatted_year)
                    
                    if row is None:
                        st.session_state.output.warning("No data found for that season.")
                    else:
                        st.session_state.output.markdown("### **Loading...**")
                        
                        desc = ai_descriptions(f"Write a 100-word summary evaluating {player['full_name']}'s performance in the {formatted_year} season.", year)
                        # output has stat transformers to protect against None values
                        st.session_state.output.markdown(f"""
                            ### {player['full_name']} — {formatted_year}
                            **Averages per Game**  
                            - {gp_stat_transformer(row['PTS'], row['GP'])} points  
                            - {gp_stat_transformer(row['REB'], row['GP'])} rebounds  
                            - {gp_stat_transformer(row['AST'], row['GP'])} assists  
                            - {gp_stat_transformer(row['STL'], row['GP'])} steals  
                            - {gp_stat_transformer(row['BLK'], row['GP'])} blocks  

                            **Season Totals**  
                            - {stat_transformer(row['PTS'])} points  
                            - {stat_transformer(row['REB'])} rebounds  
                            - {stat_transformer(row['AST'])} assists  
                            - {stat_transformer(row['STL'])} steals  
                            - {stat_transformer(row['BLK'])} blocks  
                            - {stat_transformer(row['GP'])} games played  

                            {desc}
                        """)
                    
# If a player's career stats are looked up
                elif year.lower() == 'career':
                    df = get_player_career_totals(player['id'])
                    row = df.iloc[0]
                    if row is None:
                        st.session_state.output.warning("No data found for that season.")
                    else:
                        st.session_state.output.markdown("### **Loading...**")
                        description = ai_descriptions(f"Write a 100-word summary evaluating {player['full_name']}'s career", year)
                                            
                        st.session_state.output.markdown(f"""
                            ### {player['full_name']} Career
                            **Averages per Game**  
                            - {gp_stat_transformer(row['PTS'], row['GP'])} points  
                            - {gp_stat_transformer(row['REB'], row['GP'])} rebounds  
                            - {gp_stat_transformer(row['AST'], row['GP'])} assists  

                            **Career Totals**  
                            - {stat_transformer(row['PTS'])} points  
                            - {stat_transformer(row['REB'])} rebounds  
                            - {stat_transformer(row['AST'])} assists  
                            - {stat_transformer(row['GP'])} games played  

                            {description}
                            """)

# Handle invalid year entry
                else:
                    st.session_state.output.error("Must enter a one number valid year between 1947 and today.")
                    
                    
                    
# When a team is selected        
        else: 
            selected_team = teams.find_teams_by_full_name(name)

# Check to be sure team exists
            if len(selected_team) == 0:
                st.session_state.output.error("No team found.")
                
# If a specific year is entered
            else:
                team = selected_team[0]
                if year.isnumeric() and validate_year(year):
                    formatted_year = format_season(year)
                    
                    row = get_team_season_stats(team['id'], formatted_year)
                    if row.empty:
                        st.session_state.output.warning("No data found for that season.")
                    else:
                        st.session_state.output.markdown("### **Loading...**")
                        desc = ai_descriptions(f"Write a 100-word summary evaluating {team['full_name']}'s {formatted_year} season.", year)
                        
                        st.session_state.output.markdown(f"""
                            ### {team['full_name']} — {formatted_year}
                            - {stat_transformer(row['WINS'])} wins  
                            - {stat_transformer(row['LOSSES'])} losses  
                            - {round(row['WIN_PCT']*100, 1)}% win rate  
                            - {stat_transformer(row['PO_WINS'])} playoff wins  
                            - {stat_transformer(row['PO_LOSSES'])} playoff losses  

                            {desc}
                            """)
                    
                    
# If career stats are requested
                elif year.lower() == 'career':
                    df = get_team_history(team['id'])
                    row = df.iloc[0]
                    if row is None:
                        st.session_state.output.warning("No data found for that season.")
                    else:
                        st.session_state.output.markdown("### **Loading...**")
                        desc = ai_descriptions(f"Write a 100-word summary evaluating {team['full_name']}'s franchise history.")
                        
                        st.session_state.output.markdown(f"""
                            ### {team['full_name']} Info
                            - {row['TEAM_CONFERENCE']} Conference  
                            - {row['TEAM_DIVISION']} Division  
                            - Founded: {row['MIN_YEAR']}  

                            {desc}
                            """)
                        
# Handle invalid year entry
                else:
                    st.session_state.output.error("Must enter a valid year between 1947 and today.")
                    
                    
    
    
main()    