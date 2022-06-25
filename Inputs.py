import requests
import json

def getDriverStandings(year):
    DriverInput = requests.get("http://ergast.com/api/f1/"+year+"/driverStandings.json")
    unparsedDriver = DriverInput.text
    parsedDrivers = json.loads(unparsedDriver)
    return parsedDrivers

def getConstructorStandings(year):
    inputsWCC = requests.get("http://ergast.com/api/f1/"+year+"/constructorStandings.json")
    unparsedWCC = inputsWCC.text
    parsedWCC = json.loads(unparsedWCC)
    return parsedWCC

def getRaces(Driver,year):
    inputsRace = requests.get("http://ergast.com/api/f1/"+year+"/drivers/"+Driver+"/results.json")
    unparsedRace = inputsRace.text
    parseRace = json.loads(unparsedRace)
    return parseRace["MRData"]['RaceTable']["Races"]

def DriversList(parsedDrivers):
    DriverDict = {}
    for i in parsedDrivers["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]:
        if len(i["Constructors"]) == 1:
            if i["Constructors"][0]["constructorId"] in DriverDict:
                working = DriverDict[i["Constructors"][0]["constructorId"]]
                if isinstance(working,list):
                    working.append(i["Driver"]["driverId"])
                    updated = working
                else:
                    updated = [working, i["Driver"]["driverId"]]
                DriverDict[i["Constructors"][0]["constructorId"]] = updated
            else:
                DriverDict[i["Constructors"][0]["constructorId"]] = i["Driver"]["driverId"]
        elif len(i["Constructors"]) == 2:
            for j in i["Constructors"]:
                if j["constructorId"] in DriverDict:
                    working = DriverDict[j["constructorId"]]
                    if isinstance(working,list):
                        working.append(i["Driver"]["driverId"])
                        updated = working
                    else:
                        updated = [working, i["Driver"]["driverId"]]
                    DriverDict[j["constructorId"]] = updated
                else:
                    DriverDict[j["constructorId"]] = i["Driver"]["driverId"]
    return DriverDict

