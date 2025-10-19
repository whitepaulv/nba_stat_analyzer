import streamlit as st
from nba_api.stats.static import players, teams
from nba_data import gp_stat_transformer, stat_transformer, get_player_season_stats, get_player_career_totals, get_team_season_stats, get_team_history
from ai_summary import ai_descriptions

# This is the global output container that will be used for everything


# To run, type in 'source venv/bin/activate',
# then run with streamlit run app.py
    


def main():
                    
    st.title("🏀 NBA Stats Lookup")
    
    selection_type = st.selectbox("Select type:", ["Player", "Team"])
    name = st.text_input("Please enter a player/team's full name:")   
    year = st.text_input("Please enter a specific year, or enter 'career' for career info:")
        
    if st.button("Search"):
        st.session_state.output = st.empty()
        
        if selection_type == 'Player': #For players
            selected_player = players.find_players_by_full_name(name)
            if len(selected_player) == 0:
                 st.session_state.output.error("No player found.")
            else:
                player = selected_player[0]
                if year.isnumeric():
                    year_int = int(year)
                    formatted_year = str(year_int - 1) + '-' + str(year_int)[-2:]
                    row = get_player_season_stats(player['id'], formatted_year)
                    
                    if row is None:
                        st.session_state.output.warning("No data found for that season.")
                    else:
                        st.session_state.output.markdown("### **Loading...**")
                        
                        desc = ai_descriptions(f"Write a 100-word summary evaluating {player['full_name']}'s performance in the {formatted_year} season.")
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
                    
                elif year.lower() == 'career':
                    df = get_player_career_totals(player['id'])
                    row = df.iloc[0]
                    if row is None:
                        st.session_state.output.warning("No data found for that season.")
                    else:
                        st.session_state.output.markdown("### **Loading...**")
                        description = ai_descriptions(f"Write a 100-word summary evaluating {player['full_name']}'s career")
                                            
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
                    
                    
                    
                    
        else: # For teams
            selected_team = teams.find_teams_by_full_name(name)
            if len(selected_team) == 0:
                st.session_state.output.error("No team found.")
            else:
                team = selected_team[0]
                if year.isnumeric():
                    year_int = int(year)
                    formatted_year = str(year_int - 1) + '-' + str(year_int)[-2:]
                    
                    row = get_team_season_stats(team['id'], formatted_year)
                    if row.empty:
                        st.session_state.output.warning("No data found for that season.")
                    else:
                        st.session_state.output.markdown("### **Loading...**")
                        desc = ai_descriptions(f"Write a 100-word summary evaluating {team['full_name']}'s {formatted_year} season.")
                        
                        st.session_state.output.markdown(f"""
                            ### {team['full_name']} — {formatted_year}
                            - {stat_transformer(row['WINS'])} wins  
                            - {stat_transformer(row['LOSSES'])} losses  
                            - {round(row['WIN_PCT']*100, 1)}% win rate  
                            - {stat_transformer(row['PO_WINS'])} playoff wins  
                            - {stat_transformer(row['PO_LOSSES'])} playoff losses  

                            {desc}
                            """)
                    
                    
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
                    
                    
    
    
main()    