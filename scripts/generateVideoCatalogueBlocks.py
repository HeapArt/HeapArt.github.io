import os
import json
import re

gWorkingDirectory = "../"
gInputVideoDataFiles = ["site/database/HeapArtVideoData.json"]
gCatalogueOutputDirectory = "site/database/CatalogPageDefinition"


def loadJson(iFilePath):
    with open(iFilePath, encoding="utf-8") as f:
        return json.load(f)
    return None


def save_file(iPath, iText):
    wPath = os.path.join(gCatalogueOutputDirectory, iPath)
    wBasedir = os.path.dirname(wPath)

    if "" != wBasedir:
        if not os.path.exists(wBasedir):
            os.makedirs(wBasedir)

    with  open(wPath, 'w') as wFile:
        wFile.write(iText)
        wFile.close()


def createPageDefinition(iTitle, iBlockList):
    wNewPage = {}
    wNewPage["site_title"] = iTitle
    wNewPage["block_list"] = iBlockList
    return wNewPage


def createBlockDefinition(iTitle, iDate,  iBody, iCaption):
    wNewBlock = {}
    if None != iTitle:
        wNewBlock["title"] = iTitle
    if None != iDate:
        wNewBlock["date"] = iDate
    if None != iBody:
        wNewBlock["body"] = iBody
    if None != iCaption:
        wNewBlock["caption"] = iCaption
    return wNewBlock


def generatePageDefinitions(iVideoDataFile):

    PaperPlaneList = {}
    QuickieOrigamiList = []
    ModeratoOrigamiList = []

    TutorialByDesignerList = {}
    FullTutorialList = []

    for wVideoEntry in iVideoDataFile["Video List"]:
        isTutorial = False
        wTitle = wVideoEntry["Video title"].replace("  ", " ")

        if "(100 Exotic Paper Airplanes" in wVideoEntry["Video title"]:
            wStrList = wVideoEntry["Video title"].split(" ");
            wTitle = wTitle.replace("Paper Plane " + wStrList[2] + " : ", "")
            wTitle = wTitle.replace(" (100 Exotic Paper Airplanes Challenge)", "")
            wTitle = wTitle.replace(" (100 Exotic Paper Airplanes)", "")

            PaperPlaneList[wStrList[2]] = wVideoEntry
            isTutorial = True
            
        if "Quickie Origami - " in wVideoEntry["Video title"]:
            wTitle = wTitle.replace("Quickie Origami - ", "")
            wTitle = wTitle.replace("Origami ", "")
            QuickieOrigamiList.append(wVideoEntry)
            isTutorial = True
        
        if "Moderato Origami - " in wVideoEntry["Video title"]:
            wTitle = wTitle.replace("Moderato Origami - ", "")
            wTitle = wTitle.replace("Origami ", "")
            ModeratoOrigamiList.append(wVideoEntry)
            isTutorial = True

        if True == isTutorial:
          
            wTitle = re.sub("^a ", "", wTitle)
            wTitle = re.sub("^A ", "", wTitle)
            wTitle = re.sub("^the ", "", wTitle)
            wTitle = re.sub("^The ", "", wTitle)
            wTitle = re.sub("^an ", "", wTitle)
            wTitle = re.sub("^An ", "", wTitle)
            wTitle = wTitle.replace(" (No Glue, No Scissors)", "")
            wTitle = wTitle.replace("@HeapArt", "")
            wVideoEntry["Clean Title"] = wTitle

            wSearchTitle = wTitle.lower()
            wVideoEntry["Search Title"] = wSearchTitle
            FullTutorialList.append(wVideoEntry)

        if "Designer" in wVideoEntry:
            if wVideoEntry["Designer"] not in TutorialByDesignerList:
                TutorialByDesignerList[wVideoEntry["Designer"]] = []
            
            TutorialByDesignerList[wVideoEntry["Designer"]].append(wVideoEntry)
    
    
#    print (PaperPlaneList)
#    print (QuickieOrigamiList)
#    print (ModeratoOrigamiList)
#    print (TutorialByDesignerList)

    # Paper Airplane Catalog

    paperPlaneLinkList = "<ol>"
    for wKey in sorted(PaperPlaneList.keys()):
        wVideoEntry = PaperPlaneList[wKey]
        wlink = "<li>"
        wlink += "<a href=\"./" + wKey + ".html\">" + wVideoEntry["Clean Title"] + "</a>"
        wlink += "</li>"
        paperPlaneLinkList += wlink    
    paperPlaneLinkList += "</ol>"

    print(paperPlaneLinkList)

    wPaperAirplaneContentBlock = createBlockDefinition("Paper Airplane List", None,  [paperPlaneLinkList], None )

    wChallengeDefinition = createBlockDefinition("Challenge Definition", None,  [
      "<p>This is our \"100 Exotic Paper Airplanes Challenge\" Page.</p>"
      "<p>Our \"100 Exotic Paper Airplane Challenge\" is where I make 100 Paper Airplane Tutorials, ideally not so well known, and have them all in one mega playlist.",
      "This project started on May 12, 2019. The project schedule is one Tutorial per week. Without any delays, and if I am able to maintain this schedule, this project is forseen to finish in April 2022.</p>"
      "<p>Click <a href=\"https://youtube.com/playlist?list=PL3Ct47F8enQGnkKDOOC3hZbBQPgVKYmIN\">here</a> to see the YouTube Playlist</p>"
      "<p>I hope you will enjoy this collection of Paper Airplanes</p>"
      "<p>Wilson Lee @HeapArt</p>"      
    ], None )

    w100ExoticPaperAirplanesChallengePageDefintion = createPageDefinition("100 Exotic Paper Airplane Challenge", [wChallengeDefinition, wPaperAirplaneContentBlock])
    save_file("paperairplanes/index.json", json.dumps(w100ExoticPaperAirplanesChallengePageDefintion, indent=2))

    for wKey in sorted(PaperPlaneList.keys()):
        wVideoEntry = PaperPlaneList[wKey]

        wCaptionDef = {}
        wCaptionDef["type"] = "video"
        wCaptionDef["videoId"] = wVideoEntry["Video"]
        
        wVideoBlock = createBlockDefinition("Video Tutorial", wVideoEntry["Video publish time"], None, wCaptionDef )
        wPaperPlanePage = createPageDefinition(wVideoEntry["Clean Title"], [wVideoBlock, wPaperAirplaneContentBlock])
        save_file("paperairplanes/{0}.json".format(wKey), json.dumps(wPaperPlanePage, indent=2))

    # Tutorial catalog by A-Z
    wSortedTutorialList = sorted(FullTutorialList, key=lambda x: x["Search Title"])


    #Create Link List
    wAZlinkList = {}
    for wVideoEntry in wSortedTutorialList:
        wLetter = wVideoEntry["Search Title"][0]
        if wLetter.isdigit():
            wLetter = "#"
        else:
            wLetter = wLetter.upper()

        if wLetter not in wAZlinkList:
            wAZlinkList[wLetter] = "<ul>"
        wlink = "<li>"
        wlink += "<a href=\"./" + wVideoEntry["Video"] + ".html\">" + wVideoEntry["Clean Title"] + "</a>"
        wlink += "</li>"
        wAZlinkList[wLetter] += wlink

    for wLetterLinks in wAZlinkList:
        wLetterLinks += "</ul>"

    #Create Block List
    wAZBlockList = []
    for wLinkListKey in sorted(wAZlinkList.keys()):
        wVideoBlock = createBlockDefinition(wLinkListKey, None, wAZlinkList[wLinkListKey], None )
        wAZBlockList.append(wVideoBlock)

    wAZList = createPageDefinition("Origami Tutorials from A to Z", wAZBlockList)
    save_file("azlist/index.json", json.dumps(wAZList, indent=2))

    for wVideoEntry in wSortedTutorialList:

        wCaptionDef = {}
        wCaptionDef["type"] = "video"
        wCaptionDef["videoId"] = wVideoEntry["Video"]
        
        wVideoBlock = createBlockDefinition("Video Tutorial", wVideoEntry["Video publish time"], None, wCaptionDef )
        wAZVideoPage = createPageDefinition(wVideoEntry["Clean Title"], [wVideoBlock] + wAZBlockList)
        save_file("azlist/{0}.json".format(wVideoEntry["Video"]), json.dumps(wAZVideoPage, indent=2))


    print(wAZlinkList)

    # Tutorial catalog by A-Z
    
    pass




def main():
    os.chdir(gWorkingDirectory)

    print(os.getcwd())

    for wInputVideoData in gInputVideoDataFiles:
        print (wInputVideoData)
        wVideoData = loadJson(wInputVideoData)
        generatePageDefinitions(wVideoData)
    

if __name__ == '__main__':
    main()
