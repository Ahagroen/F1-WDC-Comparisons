import Inputs as In
import Constants
from datetime import datetime
import statistics

def getChampion(parsedWDC,parsedWCC,NoWCC):
    WDChampion = parsedWDC["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"][0]["Driver"]["driverId"]
    WDCTeam = parsedWDC["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"][0]["Constructors"][0]["constructorId"]
    if NoWCC:
        return WDChampion, WDCTeam
    else:
        WCChampion = parsedWCC["MRData"]["StandingsTable"]["StandingsLists"][0]["ConstructorStandings"][0]["Constructor"]["constructorId"]
    return WDChampion, WDCTeam, WCChampion
def getFinisher(parsedWDC,Position):
    Driver = parsedWDC["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"][Position]["Driver"]["driverId"]
    return Driver
def getModernSeasonPoints(racesList,modifier):
    RaceFinishPosition = []
    score = 0
    RaceCount = 0+modifier
    if RaceCount != 0:
        raceList= racesList[:-4] 
    else:
        raceList = racesList
    for i in raceList:
        RaceCount +=1
        if not i["Results"][0]["positionText"] == 'R' and not i["Results"][0]["positionText"] == "W":
            if i["Results"][0]["status"] == "Finished" or "Lap" in i["Results"][0]["status"]:
                RaceFinishPosition.append(int(i["Results"][0]["position"]))
        try:
            if int(i["Results"][0]["FastestLap"]["rank"]) == 1 and int(i["Results"][0]["position"])<11:
                score += 1
        except:
            pass
    for i in RaceFinishPosition:
        if i <11 and i!= 0:
            score += Constants.ModernPoints[i]
    if RaceFinishPosition:
        AvgPos = sum(RaceFinishPosition)/len(RaceFinishPosition)
        MedianPos = statistics.median(RaceFinishPosition)
        FinishRate = round(len(RaceFinishPosition)/RaceCount,3)*100
        PPRDNF = score/len(RaceFinishPosition)
        if len(RaceFinishPosition)>1:
            StandardDev = round(statistics.stdev(RaceFinishPosition),3)
        else:
            StandardDev = "N/A"
    else:
        AvgPos = "N/A"
    if RaceCount:
        pointsPerRace = score/RaceCount
        
    else: 
        return 0 , 0 , "N/A"
    return str(score), str(pointsPerRace), str(AvgPos), str(MedianPos), str(StandardDev), str(FinishRate), str(PPRDNF)

def getTeammate(WDC,DriverList):
    for j in DriverList:
        if (WDC in DriverList[j]):
            WDCteam = j
    return DriverList[WDCteam]

def Comparison(WDCPoints,teammates,year,team):
    TotalPoints = int(WDCPoints)
    for i in teammates:
        TotalPoints += int(getModernSeasonPoints(In.getRaces(i,str(year)),0)[0])
    return TotalPoints

def getWinningmargin(year, modifier,ParsedWDC,championPoints):
    RunnerUpRaces = In.getRaces(getFinisher(ParsedWDC,1),str(year))
    RaceFinishPosition = []
    score = 0
    RaceCount = 0+modifier
    if RaceCount != 0:
        raceList= RunnerUpRaces[:-4] 
    else:
        raceList = RunnerUpRaces
    for i in raceList:
        RaceCount +=1
        if not i["Results"][0]["positionText"] == 'R' and not i["Results"][0]["positionText"] == "W":
            if i["Results"][0]["status"] == "Finished" or "Lap" in i["Results"][0]["status"]:
                RaceFinishPosition.append(int(i["Results"][0]["position"]))
        try:
            if int(i["Results"][0]["FastestLap"]["rank"]) == 1 and int(i["Results"][0]["position"])<11:
                score += 1
        except:
            pass
    for i in RaceFinishPosition:
        if i <11 and i!= 0:
            score += Constants.ModernPoints[i]
    pointDif = int(championPoints[0])-score
    return str(pointDif)
    
def getWDCData(year): 
        modifier = 0
        if year <1958:
            WDC = In.getDriverStandings(str(year))
            WDCChampion = getChampion(WDC,0,True)
            Teammate = getTeammate(WDCChampion[0],In.DriversList(WDC))
            Teammate.remove(WDCChampion[0])
            WDCPoints = getModernSeasonPoints(In.getRaces(WDCChampion[0],str(year)),0)
            WDCPointsContribution = str(round(int(WDCPoints[0])/Comparison(WDCPoints[0],Teammate,year,WDCChampion[1])*100,1))
            PointGap = getWinningmargin(year,modifier,WDC,getModernSeasonPoints(In.getRaces(WDCChampion[0],str(year)),modifier))
            printing = [str(year),WDCChampion[0],WDCPoints[0],WDCPoints[1],WDCPoints[6], WDCPointsContribution,WDCPoints[2],WDCPoints[4], WDCPoints[3], WDCPoints[5], PointGap,"N/A","N/A",'',",".join(Teammate)]
            return printing
        else:
            WDC = In.getDriverStandings(str(year))  
            WCC = In.getConstructorStandings(str(year))
            WDCChampion = getChampion(WDC,WCC, False)
            Teammate = getTeammate(WDCChampion[0],In.DriversList(WDC))
            Teammate.remove(WDCChampion[0])
            WDCPoints = getModernSeasonPoints(In.getRaces(WDCChampion[0],str(year)),0)
            WDCPointsContribution = str(round(int(WDCPoints[0])/Comparison(WDCPoints[0],Teammate,year,WDCChampion[1])*100,1))
            PointGap = getWinningmargin(year,modifier,WDC,getModernSeasonPoints(In.getRaces(WDCChampion[0],str(year)),modifier))
            if WDCChampion[1] != WDCChampion[2]:
                splitWDC = 'y'
            else:
                splitWDC = ''
            printing = [str(year),WDCChampion[0],WDCPoints[0],WDCPoints[1],WDCPoints[6],WDCPointsContribution,WDCPoints[2],WDCPoints[4],WDCPoints[3],WDCPoints[5], PointGap,WDCChampion[1],WDCChampion[2], splitWDC,",".join(Teammate)]
            return printing

def getWCCData(year):
    if year <1958:
            return "N/A"
    else:
        WDC = In.getDriverStandings(str(year))  
        WCC = In.getConstructorStandings(str(year))
        WDCChampion = getChampion(WDC,WCC, False)
        Teammate = getTeammate(WDCChampion[0],In.DriversList(WDC))
        Teammate.remove(WDCChampion[0])
        WDCPoints = getModernSeasonPoints(In.getRaces(WDCChampion[0],str(year)),0)
        WDCPointsContribution = str(round(int(WDCPoints[0])/Comparison(WDCPoints[0],Teammate,year)*100,1))
        printing = [str(year),WDCChampion[0],WDCPoints[0],WDCPoints[1],WDCPoints[6],WDCPointsContribution,WDCPoints[2],WDCPoints[4], WDCPoints[3],WDCPoints[5],WDCChampion[1],WDCChampion[2],",".join(Teammate)]
        return printing
def Output():
    begin_time = datetime.now()
    year = 1950
    with open("output.csv","w") as f:
        f.write("Year, WDC, WDC Points, WDC Points Per Race, WDC Points Per Finished Race, WDC Point Contribution,WDC Average Position,Standard Deviation,WDC Median Position,Finish Rate (%), Winning Point Margin, WDC winning team, WCC winning team, split WDC?, WDC Teammates")
        f.write("\n")
    while year<datetime.now().year:
        with open("output.csv","a") as f:
            printing = getWDCData(year)
            f.write(','.join(printing))
            f.write("\n")
        year +=1
    print("Operation took: "+str(datetime.now()- begin_time))  
Output()
