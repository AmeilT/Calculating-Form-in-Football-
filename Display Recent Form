form_history=pd.DataFrame()

for season in seasons:
    results_season=results[results["Season"]==season]
    teams=list(results_season["Home"].unique())
    teams=teams*38

    #Make a list of Gameweek X * Number of team in the league (20)
    gameweek_numbers=[]

    for i in np.arange(1,39):
        gameweek_numbers.append(i)
    gameweek_numbers=gameweek_numbers*20
    gameweek_numbers
    gameweek_numbers.sort()

    gameweek=[]
    for i in gameweek_numbers:
        gameweek.append(f"Gameweek {i}")
    gameweek

    #create a form DF
    form_table=pd.DataFrame()
    form_table["Team"]=teams
    form_table["Gameweek"]=gameweek
    form_table["Season"]=season
    form_table["Form"]=""
    form_table.sort_values("Gameweek",ascending=False)


    form_table["GW ID"]=form_table["Gameweek"].apply(get_GW_ID)
    form_table["Last N games"]=""
    form_table

    
    
    #Assign a W,L,D to the form table based on the results table 
    for i in np.arange(0,len(results_season)):
        outcome=results_season["Outcome"].iloc[i]
        home_team=results_season["Home"].iloc[i]
        away_team=results_season["Away"].iloc[i]
        gameweek=results_season["Gameweek"].iloc[i]


        row=form_table[(form_table["Team"]==home_team)&(form_table["Gameweek"]==gameweek)].index[0]

        column="Form"

        if outcome==home_team:
            form_table.at[row,column]="W"

        elif outcome=="Draw":
            form_table.at[row,column]="D"
        else:
            form_table.at[row,column]="L"

        row=form_table[(form_table["Team"]==away_team)&(form_table["Gameweek"]==gameweek)].index[0]

        if outcome==away_team:
            form_table.at[row,column]="W"

        elif outcome=="Draw":
            form_table.at[row,column]="D"
        else:

            form_table.at[row,column]="L"

    form_table
    
    #Aggregate form over a 4 week period. The first 3 weeks will just use the longest trackrecord available
    for i in np.arange(0,760):
        form=form_table["Form"].iloc[i]
        gwid=form_table["GW ID"].iloc[i] 
        team=form_table["Team"].iloc[i]
        GWID=list(form_table["GW ID"].unique())

        rows=form_table[(form_table["Team"]==team)].index

        column="Last N games"

        if gwid==1:
            
            form_table.at[rows[0],column]=""
            
        elif gwid==2:
            
            trackrecord=form_table.at[rows[gwid-2],"Form"]
            form_table.at[rows[gwid-1],column]=trackrecord


        elif gwid==3:
            
            trackrecord=form_table.at[rows[gwid-2],"Form"]+form_table.at[rows[gwid-3],"Form"]
            form_table.at[rows[gwid-1],column]=trackrecord
 
        else:
            
            trackrecord=form_table.at[rows[gwid-2],"Form"]+form_table.at[rows[gwid-2],column]

            if len(trackrecord)>4:
            
                trackrecord=trackrecord[:4]

            form_table.at[rows[gwid-1],column]=trackrecord
   
    form_table=form_table[form_table["Form"]!=""]
    
    form_history=form_history.append(form_table) 
    
    form_history["numbers"]=form_history["Last N games"].apply(form_to_numbers)
    form_history["Form Measure"]=form_history["numbers"].apply(number_to_measure)
    form_history.drop(columns=['numbers'],inplace=True)
    
print("DONE!")
