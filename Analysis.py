#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
df=pd.read_csv('Results updates.csv')



# In[5]:


st.set_page_config(page_title='Formations',
                  layout='wide')
st.title('Formations')
formations1=df[df['Match Result']=='Home']
formations1=formations1.loc[:,
                            ['H Formation','A Formation','H Center','H Right','H Left','H Goals','A Goals','H Overall','A Overall','Match Result']]
formations1['Winning Formation']=formations1['H Formation']
formations1['Losing Formation']=formations1['A Formation']
formations1=formations1.rename(columns={'H Center':'CenterZone','H Overall':'Winner Overall','A Overall':'Loser Overall','H Goals':'Winner Goals','A Goals':'Loser Goals',
                                        'H Right':'RightZone','H Left':'LeftZone'})
formations2=df[df['Match Result']=='Away']
formations2=formations2.loc[:,['H Formation','A Formation','A Center','A Right','A Left','H Goals','A Goals','H Overall','A Overall','Match Result']]
formations2['Winning Formation']=formations2['A Formation']
formations2['Losing Formation']=formations2['H Formation']
formations2=formations2.rename(columns={'A Center':'CenterZone','H Overall':'Loser Overall','A Overall':'Winner Overall','H Goals':'Loser Goals','A Goals':'Winner Goals',
                                        'A Right':'RightZone','A Left':'LeftZone'})
formations3=df[df['Match Result']=='Draw']
formations3=formations3.loc[:,['H Formation','A Formation','H Center','H Right','H Left','H Goals','A Goals','H Overall','A Overall','Match Result']]
formations3['Winning Formation']='None'
formations3['Losing Formation']='None'
formations3=formations3.rename(columns={'H Center':'CenterZone','H Goals':'Loser Goals','A Goals':'Winner Goals',
                                        'H Right':'RightZone','H Left':'LeftZone','H Overall':'Loser Overall','A Overall':'Winner Overall'})
Formations5=[formations1,formations2,formations3]
formations=pd.concat(Formations5)
formations.reset_index(drop=True, inplace=True)
all_formations=df['H Formation'].unique()
formation1_filter=st.selectbox("Select Formation A",all_formations,index=1)
formation2_filter=st.selectbox("Select Formation B",all_formations,index=3)
Difference_filter1=st.number_input("Formation B minimum Difference rate ")
Difference_filter2=st.number_input("Formation B maximum Difference rate ")

formations['Difference in team rating']=(formations['Winner Overall']-formations['Loser Overall'])
formations=formations.join(df['H Team'])
formations=formations.join(df['A Team'])
formations=formations.join(df['H Possession'])
formations=formations.join(df['A Possession'])
formations=formations.join(df['H Playzone'])
formations=formations.join(df['A Playzone'])
formations=formations.join(df['H Shots'])
formations=formations.join(df['H SOT'])
formations=formations.join(df['A Shots'])
formations=formations.join(df['A SOT'])
formations=formations.join(df['H Goals'])
formations=formations.join(df['A Goals'])
formations4=[formations1,formations2]
Formations=pd.concat(formations4)
Formations['Difference in team rating']=(Formations['Winner Overall']-Formations['Loser Overall'])
Formations.reset_index(drop=True, inplace=True)

draws=df[df['Match Result']=='Draw']
all_teams1=df[df['A Overall']>=60]
all_teams1=all_teams1['A Team'].unique()
all_teams2=df[df['H Overall']>=60]
all_teams2=all_teams2['H Team'].unique()
x=list(all_teams1)
y=list(all_teams2)
x.extend(y)
all_teams=tuple(x)


formations=formations[formations['Difference in team rating']>=Difference_filter1]
formations=formations[formations['Difference in team rating']<=Difference_filter2]
Formations=Formations[Formations['Difference in team rating']>=Difference_filter1]
Formations=Formations[Formations['Difference in team rating']<=Difference_filter2]
form=[]
for i in all_formations :
    for y in all_formations :
        
        
        
        q=Formations[Formations["Winning Formation"]==y]
        no_wins=q[q["Losing Formation"]==i].value_counts().sum()
        
        
        
        mask=df[df['H Formation']==y]
        mask['Difference']=mask['H Overall']-mask['A Overall']
        mask1=df[df['A Formation']==y]
        mask1['Difference']=mask1['A Overall']-mask1['H Overall']
        masks=[mask,mask1]
        mask2=pd.concat(masks)
        mask2=mask2[mask2['Difference']>=Difference_filter1]
        mask2=mask2[mask2['Difference']<=Difference_filter2]
        mask3=mask2[mask2['H Formation']==i]
        t=mask3['H Formation'].value_counts().sum()
        mask4=mask2[mask2['A Formation']==i]
        b=mask4['A Formation'].value_counts().sum()
        
        
        
        x=draws[draws['H Formation']==y]
        e=x[x['A Formation']==i]
        e['Difference']=e['H Overall'] - e['A Overall']
        x1=draws[draws['A Formation']==y]
        e1=x1[x1['H Formation']==i]
        e1['Difference']=e1['A Overall'] - e1['H Overall']
        Draws=[e,e1]
        total=pd.concat(Draws)
        total=total[total['Difference']>=Difference_filter1]
        total=total[total['Difference']<=Difference_filter2]
        total_draws=total['Difference'].value_counts().sum()
        total_matches=b+t
        
        
        
        
        
        
        winPercent=(no_wins/total_matches)*100
        winPercent= round(winPercent, 2)
        drawPercent=(total_draws/total_matches)*100
        drawPercent= round(drawPercent, 2)
        WinDrawPercent=((no_wins+total_draws)/total_matches)*100
        WinDrawPercent= round(WinDrawPercent, 2)
        
        
        
        o=mask2[mask2["H Formation"]==y]
        zone=o['H Playzone'].value_counts().idxmax()
        Average_Hshots=o["H Shots"].mean()
        Average_HshotOnTarget=o['H SOT'].mean()
        p=mask2[mask2["A Formation"]==y]
        Average_Ashots=p["A Shots"].mean()
        Average_AshotOnTarget=p['A SOT'].mean()
        Average_shots=(Average_Ashots+Average_Hshots)/2
        Average_shots= round(Average_shots, 2)
        Average_shotsOnTarget=(Average_AshotOnTarget+Average_HshotOnTarget)/2
        Average_shotsOnTarget= round(Average_shotsOnTarget, 2)
        Average_APos=p['A Possession'].mean()
        Average_HPos=o['H Possession'].mean()
        Average_Pos= (Average_APos+Average_HPos)/2
        Average_Pos= round(Average_Pos, 2)
        form.append((i,y,total_matches,no_wins,winPercent,total_draws,drawPercent,WinDrawPercent,zone,Average_shots,Average_shotsOnTarget,Average_Pos))
s=pd.DataFrame(form,columns=('Formation','counter Formation','Total Matches','Win','win %','Draws','Draw %','WinDraw %','Best Zone',"Average Shots","Average Shots On Target","Average Possession"))
s=s[s['Formation']==formation1_filter]
s=s[s['counter Formation']==formation2_filter]
st.dataframe(s.head())
form1=[]
for i in all_formations :
    for y in all_formations :
        q=Formations[Formations["Winning Formation"]==y]
        no_wins=q[q["Losing Formation"]==i].value_counts().sum()
        mask=df[df['H Formation']==y]
        mask['Difference']=mask['H Overall']-mask['A Overall']
        mask1=df[df['A Formation']==y]
        mask1['Difference']=mask1['A Overall']-mask1['H Overall']
        masks=[mask,mask1]
        mask2=pd.concat(masks)
        mask2=mask2[mask2['Difference']>=Difference_filter1]
        mask2=mask2[mask2['Difference']<=Difference_filter2]
        mask3=mask2[mask2['H Formation']==i]
        t=mask3['H Formation'].value_counts().sum()
        mask4=mask2[mask2['A Formation']==i]
        b=mask4['A Formation'].value_counts().sum()
        
        x=draws[draws['H Formation']==y]
        e=x[x['A Formation']==i]
        e['Difference']=e['H Overall'] - e['A Overall']
        x1=draws[draws['A Formation']==y]
        e1=x1[x1['H Formation']==i]
        e1['Difference']=e1['A Overall'] - e1['H Overall']
        Draws=[e,e1]
        total=pd.concat(Draws)
        total=total[total['Difference']>=Difference_filter1]
        total=total[total['Difference']<=Difference_filter2]
        total_draws=total['Difference'].value_counts().sum()
        total_matches=b+t
        winPercent=(no_wins/total_matches)*100
        winPercent= round(winPercent, 2)
        drawPercent=(total_draws/total_matches)*100
        drawPercent= round(drawPercent, 2)
        WinDrawPercent=((no_wins+total_draws)/total_matches)*100
        WinDrawPercent= round(WinDrawPercent, 2)
        
        
        o=mask2[mask2["H Formation"]==y]
        zone=o['H Playzone'].value_counts().idxmax()
        Average_Hshots=o["H Shots"].mean()
        Average_HshotOnTarget=o['H SOT'].mean()
        p=mask2[mask2["A Formation"]==y]
        Average_Ashots=p["A Shots"].mean()
        Average_AshotOnTarget=p['A SOT'].mean()
        Average_shots=(Average_Ashots+Average_Hshots)/2
        Average_shots= round(Average_shots, 2)
        Average_shotsOnTarget=(Average_AshotOnTarget+Average_HshotOnTarget)/2
        Average_shotsOnTarget= round(Average_shotsOnTarget, 2)
        Average_APos=p['A Possession'].mean()
        Average_HPos=o['H Possession'].mean()
        Average_Pos= (Average_APos+Average_HPos)/2
        Average_Pos= round(Average_Pos, 2)
        
        
        form1.append((i,y,total_matches,no_wins,winPercent,total_draws,drawPercent,WinDrawPercent,
                      zone,Average_shots,Average_shotsOnTarget,Average_Pos))
h=pd.DataFrame(form1,columns=('Formation','counter Formation','Total Matches','Win','win %','Draws','Draw %','WinDraw %','Best Zone',"Average Shots","Average Shots On Target","Average Possession"))
h=h[h['Formation']==formation2_filter]
h=h[h['counter Formation']==formation1_filter]
st.dataframe(h.head())
st.markdown('the top 3 formations to use against with the best play zone to use')
losing=[]
for i in all_formations :
    for y in all_formations :
        x=Formations[Formations['Losing Formation']==i]
        match_Losses_to_formation=x[x['Winning Formation']==y].value_counts().sum()
        
        
        mask=df[df['H Formation']==y]
        mask['Difference']=mask['H Overall']-mask['A Overall']
        mask1=df[df['A Formation']==y]
        mask1['Difference']=mask1['A Overall']-mask1['H Overall']
        masks=[mask,mask1]
        mask2=pd.concat(masks)
        mask2=mask2[mask2['Difference']>=Difference_filter1]
        mask2=mask2[mask2['Difference']<=Difference_filter2]
        mask3=mask2[mask2['H Formation']==i]
        t=mask3['H Formation'].value_counts().sum()
        mask4=mask2[mask2['A Formation']==i]
        b=mask4['A Formation'].value_counts().sum()
        total_matches=b+t
        
        x=draws[draws['H Formation']==y]
        e=x[x['A Formation']==i]
        e['Difference']=e['H Overall'] - e['A Overall']
        x1=draws[draws['A Formation']==y]
        e1=x1[x1['H Formation']==i]
        e1['Difference']=e1['A Overall'] - e1['H Overall']
        Draws=[e,e1]
        total=pd.concat(Draws)
        total=total[total['Difference']>=Difference_filter1]
        total=total[total['Difference']<=Difference_filter2]
        total_draws=total['Difference'].value_counts().sum()
        drawPercent=(total_draws/total_matches)*100
        drawPercent= round(drawPercent, 2)
        WinDrawPercent=((match_Losses_to_formation+total_draws)/total_matches)*100
        WinDrawPercent= round(WinDrawPercent, 2)
        
        
        
        n=(match_Losses_to_formation/total_matches)*100
        n= round(n, 2)
        
        
        
        o=mask2[mask2["H Formation"]==y]
        zone=o['H Playzone'].value_counts().idxmax()
        Average_Hshots=o["H Shots"].mean()
        Average_HshotOnTarget=o['H SOT'].mean()
        p=mask2[mask2["A Formation"]==y]
        Average_Ashots=p["A Shots"].mean()
        Average_AshotOnTarget=p['A SOT'].mean()
        Average_shots=(Average_Ashots+Average_Hshots)/2
        Average_shots= round(Average_shots, 2)
        Average_shotsOnTarget=(Average_AshotOnTarget+Average_HshotOnTarget)/2
        Average_shotsOnTarget= round(Average_shotsOnTarget, 2)
        Average_APos=p['A Possession'].mean()
        Average_HPos=o['H Possession'].mean()
        Average_Pos= (Average_APos+Average_HPos)/2
        Average_Pos= round(Average_Pos, 2)
        
        losing.append((i,y,match_Losses_to_formation,total_matches,n,total_draws,drawPercent,WinDrawPercent,zone,Average_shots,Average_shotsOnTarget,Average_Pos))
u=pd.DataFrame(losing,columns=('Formation','Beat','Losses to this formation','Total Matches','%','Draws','Draw %','WinDraw %','Best Zone','Average_shots','Average_shotsOnTarget','Average_Pos')).sort_values('%',ascending=False)
u=u[u['Formation']==formation1_filter]
u=u[u['Beat']!=formation1_filter]
u=u.rename(columns={'Beat':'Best Counter Formation',
                                        'Losses to this formation':'Losses to the Counter Formation',
                                        'Total Matches':'Total Matches between Formations'})
st.dataframe(u.head(3))
losing1=[]
for i in all_formations :
    for y in all_formations :
        x=Formations[Formations['Losing Formation']==i]
        match_Losses_to_formation=x[x['Winning Formation']==y].value_counts().sum()
        
        
        mask=df[df['H Formation']==y]
        mask['Difference']=mask['H Overall']-mask['A Overall']
        mask1=df[df['A Formation']==y]
        mask1['Difference']=mask1['A Overall']-mask1['H Overall']
        masks=[mask,mask1]
        mask2=pd.concat(masks)
        mask2=mask2[mask2['Difference']>=Difference_filter1]
        mask2=mask2[mask2['Difference']<=Difference_filter2]
        mask3=mask2[mask2['H Formation']==i]
        t=mask3['H Formation'].value_counts().sum()
        mask4=mask2[mask2['A Formation']==i]
        b=mask4['A Formation'].value_counts().sum()
        total_matches=b+t
        
        x=draws[draws['H Formation']==y]
        e=x[x['A Formation']==i]
        e['Difference']=e['H Overall'] - e['A Overall']
        x1=draws[draws['A Formation']==y]
        e1=x1[x1['H Formation']==i]
        e1['Difference']=e1['A Overall'] - e1['H Overall']
        Draws=[e,e1]
        total=pd.concat(Draws)
        total=total[total['Difference']>=Difference_filter1]
        total=total[total['Difference']<=Difference_filter2]
        total_draws=total['Difference'].value_counts().sum()
        drawPercent=(total_draws/total_matches)*100
        drawPercent= round(drawPercent, 2)
        WinDrawPercent=((match_Losses_to_formation+total_draws)/total_matches)*100
        WinDrawPercent= round(WinDrawPercent, 2)
        
        
        
        
        n=(match_Losses_to_formation/total_matches)*100
        n= round(n, 2)
        
        o=mask2[mask2["H Formation"]==y]
        zone=o['H Playzone'].value_counts().idxmax()
        Average_Hshots=o["H Shots"].mean()
        Average_HshotOnTarget=o['H SOT'].mean()
        p=mask2[mask2["A Formation"]==y]
        Average_Ashots=p["A Shots"].mean()
        Average_AshotOnTarget=p['A SOT'].mean()
        Average_shots=(Average_Ashots+Average_Hshots)/2
        Average_shots= round(Average_shots, 2)
        Average_shotsOnTarget=(Average_AshotOnTarget+Average_HshotOnTarget)/2
        Average_shotsOnTarget= round(Average_shotsOnTarget, 2)
        Average_APos=p['A Possession'].mean()
        Average_HPos=o['H Possession'].mean()
        Average_Pos= (Average_APos+Average_HPos)/2
        Average_Pos= round(Average_Pos, 2)
        
        
        losing1.append((i,y,match_Losses_to_formation,total_matches,n,total_draws,drawPercent,WinDrawPercent,zone,Average_shots,Average_shotsOnTarget,Average_Pos))
r=pd.DataFrame(losing1,columns=('Formation','Beat','Losses to this formation','Total Matches','%','Draws','Draw %','WinDrawPercent','Best Zone','Average_shots','Average_shotsOnTarget','Average_Pos')).sort_values('%',ascending=False)
r=r[r['Formation']==formation2_filter]
r=r[r['Beat']!=formation2_filter]
r=r.rename(columns={'Beat':'Best Counter Formation',
                                        'Losses to this formation':'Losses to the Counter Formation',
                                        'Total Matches':'Total Matches between Formations'})
st.dataframe(r.head(3))
st.markdown('Top 3 formations that produces the most goals, filtered by difference in team rating')    
goals_scored=[]
for i in all_formations :
    r=formations[formations['H Formation']==i]
    e=formations[formations['A Formation']==i]
    t=r[r['A Formation']!=i]
    z=r[r['A Formation']!=i].value_counts().sum()
    p=e[e['H Formation']!=i]
    q=e[e['H Formation']!=i].value_counts().sum()
    no_of_matches=z+q
    home_goals=t['H Goals'].sum()
    away_goals=p['A Goals'].sum()
    Goals=home_goals+away_goals
    No_of_wins1=t[t['Winning Formation']==i].value_counts().sum()
    No_of_wins2=p[p['Winning Formation']==i].value_counts().sum()
    No_of_wins=No_of_wins1+No_of_wins2
    Goal_per_match=Goals/no_of_matches
    WinPercent=(No_of_wins/no_of_matches)*100
    WinPercent= round(WinPercent, 2)
    n=t[t["Match Result"]=="Draw"].value_counts().sum()
    o=p[p["Match Result"]=="Draw"].value_counts().sum()
    Total_draws=n+o
    DrawPercent=(Total_draws/no_of_matches)*100
    DrawPercent= round(DrawPercent, 2)
    WinDraw=Total_draws+No_of_wins
    WinDrawPercent=(WinDraw/no_of_matches)*100
    WinDrawPercent= round(WinDrawPercent, 2)
    zone=r['H Playzone'].value_counts().idxmax()
    Average_Hshots=t["H Shots"].mean()
    Average_HshotOnTarget=t['H SOT'].mean()
    Average_Ashots=p["A Shots"].mean()
    Average_AshotOnTarget=p['A SOT'].mean()
    Average_shots=(Average_Ashots+Average_Hshots)/2
    Average_shots= round(Average_shots, 2)
    Average_shotsOnTarget=(Average_AshotOnTarget+Average_HshotOnTarget)/2
    Average_shotsOnTarget= round(Average_shotsOnTarget, 2)
    Average_APos=p['A Possession'].mean()
    Average_HPos=t['H Possession'].mean()
    Average_Pos= (Average_APos+Average_HPos)/2
    Average_Pos= round(Average_Pos, 2)
    
    goals_scored.append((i,Goals,no_of_matches,Goal_per_match,No_of_wins,WinPercent,
                         Total_draws,DrawPercent,WinDraw,WinDrawPercent,zone,Average_shots,Average_shotsOnTarget,Average_Pos))
goals_scored_byForamtions=pd.DataFrame(goals_scored,columns=('Formations','Goals Scored','Total matches','Goal per match','Wins','Win%',"Draw","Draw%",'WinDraw','WinDraw%','Best Zone','Average_shots','Average_shotsOnTarget','Average_Pos')).sort_values('Goal per match',ascending=False).reset_index().drop('index',axis=1)
st.dataframe(goals_scored_byForamtions.head(3))
st.markdown('Top 3 formations for conceding the least amount of goals, filtered by difference in team rating')
goals_conceded=[]
for i in all_formations :
    r=formations[formations['H Formation']==i]
    e=formations[formations['A Formation']==i]
    t=r[r['A Formation']!=i]
    z=r[r['A Formation']!=i].value_counts().sum()
    p=e[e['H Formation']!=i]
    q=e[e['H Formation']!=i].value_counts().sum()
    no_of_matches=z+q
    No_of_wins1=t[t['Winning Formation']==i].value_counts().sum()
    No_of_wins2=p[p['Winning Formation']==i].value_counts().sum()
    No_of_wins=No_of_wins1+No_of_wins2
    away_goals=t['A Goals'].sum()
    home_goals=p['H Goals'].sum()
    conceded_Goals=home_goals+away_goals
    Goal_per_match=conceded_Goals/no_of_matches
    Goal_per_match= round(Goal_per_match, 2)
    WinPercent=(No_of_wins/no_of_matches)*100
    WinPercent= round(WinPercent, 2)
    n=t[t["Match Result"]=="Draw"].value_counts().sum()
    o=p[p["Match Result"]=="Draw"].value_counts().sum()
    Total_draws=n+o
    DrawPercent=(Total_draws/no_of_matches)*100
    DrawPercent= round(DrawPercent, 2)
    WinDraw=Total_draws+No_of_wins
    WinDrawPercent=(WinDraw/no_of_matches)*100
    WinDrawPercent= round(WinDrawPercent, 2)
    zone=r['H Playzone'].value_counts().idxmax()
    Average_Hshots=t["H Shots"].mean()
    Average_HshotOnTarget=t['H SOT'].mean()
    Average_Ashots=p["A Shots"].mean()
    Average_AshotOnTarget=p['A SOT'].mean()
    Average_shots=(Average_Ashots+Average_Hshots)/2
    Average_shots= round(Average_shots, 2)
    Average_shotsOnTarget=(Average_AshotOnTarget+Average_HshotOnTarget)/2
    Average_shotsOnTarget= round(Average_shotsOnTarget, 2)
    Average_APos=p['A Possession'].mean()
    Average_HPos=t['H Possession'].mean()
    Average_Pos= (Average_APos+Average_HPos)/2
    Average_Pos= round(Average_Pos, 2)
    goals_conceded.append((i,conceded_Goals,no_of_matches,Goal_per_match,No_of_wins,
                         WinPercent,Total_draws,DrawPercent,WinDraw,WinDrawPercent,zone,Average_shots,Average_shotsOnTarget,Average_Pos))
x=pd.DataFrame(goals_conceded,columns=('Formations','Goals Conceded','Total matches','Goal per match','Wins','Win%',"Draw","Draw%",'WinDraw','WinDraw%','Best Zone','Average Shots','Average shots On Target','Average Possession')).sort_values('Goal per match').reset_index().drop('index',axis=1)  
st.dataframe(x.head(3))
st.markdown("Top 3 formations that have the highest win percentage, filtered by difference in team rating")
Highest_percentage=[]
for i in all_formations :
    r=formations[formations['H Formation']==i]
    e=formations[formations['A Formation']==i]
    t=r[r['A Formation']!=i]
    z=r[r['A Formation']!=i].value_counts().sum()
    p=e[e['H Formation']!=i]
    q=e[e['H Formation']!=i].value_counts().sum()
    no_of_matches=z+q
    No_of_wins1=t[t['Winning Formation']==i].value_counts().sum()
    No_of_wins2=p[p['Winning Formation']==i].value_counts().sum()
    No_of_wins=No_of_wins1+No_of_wins2
    WinPercent=(No_of_wins/no_of_matches)*100
    WinPercent= round(WinPercent, 2)
    zone=r['H Playzone'].value_counts().idxmax()
    Average_Hshots=t["H Shots"].mean()
    Average_HshotOnTarget=t['H SOT'].mean()
    Average_Ashots=p["A Shots"].mean()
    Average_AshotOnTarget=p['A SOT'].mean()
    Average_shots=(Average_Ashots+Average_Hshots)/2
    Average_shots= round(Average_shots, 2)
    Average_shotsOnTarget=(Average_AshotOnTarget+Average_HshotOnTarget)/2
    Average_shotsOnTarget= round(Average_shotsOnTarget, 2)
    Average_APos=p['A Possession'].mean()
    Average_HPos=t['H Possession'].mean()
    Average_Pos= (Average_APos+Average_HPos)/2
    Average_Pos= round(Average_Pos, 2)
    Highest_percentage.append((i,No_of_wins,no_of_matches,WinPercent,zone,Average_shots,Average_shotsOnTarget,Average_Pos))
p=pd.DataFrame(Highest_percentage,columns=('Formations','Wins','Total Matches','Win %','Best Zone','Average_shots','Average_shotsOnTarget','Average_Pos')).sort_values('Win %',ascending=False).reset_index().drop('index',axis=1)
st.dataframe(p.head(3)) 


team_filter=st.selectbox("Select Team",all_teams)
rate_filter1=st.number_input("Minimum Difference rate ")
rate_filter2=st.number_input("Maximum Difference rate ")

team1=df[df['H Team']==team_filter]
team1['Difference']=team1['H Overall']-team1['A Overall']
team2=df[df['A Team']==team_filter]
team2['Difference']=team2['A Overall']-team2['H Overall']
team3=[team1,team2]
team=pd.concat(team3)
team=team.dropna(axis=1)
team=team[team['Difference']>=rate_filter1]
team=team[team['Difference']<=rate_filter2]
team=team.reset_index().drop('index',axis=1)
st.markdown('Total Matches filtered by difference in Team rating')
st.dataframe(team)



Losing1=team[team['H Team']==team_filter]
Losing2=Losing1[Losing1['Match Result'] != 'Home']
Losing3=team[team['A Team']==team_filter]
Losing4=Losing3[Losing3['Match Result'] != 'Away']
Losing5=[Losing2 ,Losing4]
Losing=pd.concat(Losing5).reset_index().drop('index',axis=1)
st.markdown('Matches with losses and Draw filtered by difference in Team rating')
st.dataframe(Losing)


Team=[]
for i in all_formations :
        x=Losing[Losing['H Team']==team_filter]
        y=x[x['Match Result']=='Away']
        losses1=y[y['A Formation']==i].value_counts().sum()
        z=Losing[Losing['A Team']==team_filter]
        w=z[z['Match Result']=='Home']
        losses2=w[w['H Formation']==i].value_counts().sum()
        losses=losses1+losses2
        
        total_matches1=Losing1['H Team'].value_counts().sum()
        total_matches2=Losing3['A Team'].value_counts().sum()
        total_matches=total_matches1+total_matches2
        
        WinPercent=(losses/total_matches)*100
        WinPercent=round(WinPercent,2)
        
        c=z[z['Match Result']=='Draw']
        draw1=c[c['H Formation']==i].value_counts().sum()
        m=x[x['Match Result']=='Draw']
        draw2=m[m['A Formation']==i].value_counts().sum()
        Draw=draw1+draw2
        DrawPercent=(Draw/total_matches)*100
        DrawPercent=round(DrawPercent,2)
        
        WinDraw=losses+Draw
        WinDrawPercent=((losses+Draw)/total_matches)*100
        WinDrawPercent=round(WinDrawPercent,2)
        
        e=x[x['A Formation']==i]
        l=z[z['H Formation']==i]
        
        av_shots1=e['A Shots'].sum()
        av_shots2=l['H Shots'].sum()
        av_shots=(av_shots1+av_shots2)/WinDraw
        av_shots=round(av_shots,2)
        
        
        av_Target1=e['A SOT'].sum()
        av_Target2=l['H SOT'].sum()
        av_Target=(av_Target1+av_Target2)/WinDraw
        av_Target=round(av_Target,2)
        
        
        av_pos1=e['A Possession'].sum()
        av_pos2=l['H Possession'].sum()
        av_pos=(av_pos1+av_pos2)/WinDraw
        av_pos=round(av_pos,2)
        
        
    
    
    
    
        Team.append((team_filter,i,losses,total_matches,WinPercent,Draw,DrawPercent,WinDraw,WinDrawPercent,av_shots,av_Target,av_pos))
    
    
Counter_formation=pd.DataFrame(Team,columns=('Team','Best Counter Formation','Counter Formation Win Matches','Total Matches','Win %','Draw','Draw %','WinDraw','WinDraw %','Average Shots','Average Shots On Target','Average Possession')).sort_values('Win %',ascending=False).reset_index().drop('index',axis=1)
st.dataframe(Counter_formation.head(2))
    
    
   
   
    
    
    





