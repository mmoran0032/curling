#!/usr/bin/env python3


import csv
import re
import sys


def main():
    filename = sys.argv[1]
    data = getDataIfFileExists(filename)
    data = removePageHeaders(data)
    print(data)
    # try:
    #     with open(filename, "rU") as f:
    #         data = [line.rstrip().upper() for line in f]
    #     data = [line for line in data if line is not ""]
    #     data = [" ".join(line.split()) for line in data]
    #     print(data)
    #     # games = splitIntoGames(data)
    #     # lines = []
    #     # for game in games:
    #     #     lines.append(getGameData(game))

    #     # newname = filename.split(".")[0]
    #     # header = ["team0name", "team0scores", "team1name", "team1scores"]
    #     # with open("{}.csv".format(newname), "w") as f:
    #     #     writer = csv.writer(f, delimiter=",")
    #     #     writer.writerow(header)
    #     #     for line in lines:
    #     #         writer.writerow(line)
    # except FileNotFoundError:
    #     print("File {} not found".format(sys.argv[1]))
    #     sys.exit(1)


def getDataIfFileExists(filename):
    try:
        with open(filename, "rU") as f:
            data = [" ".join(line.upper().split()) for line in f]
            data = [line for line in data if line is not ""]
        return data
    except:
        print("File {} not found".format(filename))
        sys.exit(1)


def removePageHeaders(data):
    basicHeader = data[:2]
    newData = [entry for entry in data if entry not in basicHeader]
    return newData


def splitIntoGames(data):
    games = []
    game = []
    for line in data:
        if line.startswith("*") or line.startswith("@"):
            pass
        else:
            game.append(line)
        if line.startswith("TEAM"):
            games.append(game)
            game = []
    return games


def getGameData(data):
    if data[0].startswith("SCOR"):
        data = data[2:]
    elif data[0] == "":
        data = data[3:]
    else:
        data = data[1:]
    data[0] = " ".join(data[0].split()[1:-1])
    data[1] = " ".join(data[1].split()[:-1])
    newData = {}
    teamName = re.compile(".+\)")
    scores = re.compile("\*\d.+|\d.+")
    for i, team in enumerate(("team0", "team1")):
        newData[team] = {}
        newData[team]["name"] = re.findall(teamName, data[i])[0]
        newData[team]["scores"] = re.findall(scores, data[i])[0]
    alllines = []
    for team in newData:
        line = []
        line.append(newData[team]["name"])
        line.append(newData[team]["scores"])
        alllines.append(line)
    for i in range(0, len(alllines), 2):
        line = []
        line.extend(alllines[i])
        line.extend(alllines[i + 1])
    return line


if __name__ == "__main__":
    main()
