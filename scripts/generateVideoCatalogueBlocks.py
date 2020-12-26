import os
import json


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

    for wVideoEntry in iVideoDataFile["Video List"]:
        if "(100 Exotic Paper Airplanes" in wVideoEntry["Video title"]:
            wStrList = wVideoEntry["Video title"].split(" ");
            PaperPlaneList[wStrList[2]] = wVideoEntry
            
        if "Quickie Origami - " in wVideoEntry["Video title"]:
            QuickieOrigamiList.extend(wVideoEntry)
        
        if "Moderato Origami - " in wVideoEntry["Video title"]:
            ModeratoOrigamiList.extend(wVideoEntry)
    
    print (PaperPlaneList)
    print (QuickieOrigamiList)
    print (ModeratoOrigamiList)


    paperPlaneLinkList = "<ol>"
    for wKey in sorted(PaperPlaneList.keys()):
        wVideoEntry = PaperPlaneList[wKey]
        wTitle = wVideoEntry["Video title"].replace("  ", " ")
        wTitle = wTitle.replace("Paper Plane " + wKey + " : ", "")
        wTitle = wTitle.replace("Paper Plane " + wKey + " : ", "")
        wTitle = wTitle.replace(" (100 Exotic Paper Airplanes Challenge)", "")
        wTitle = wTitle.replace(" (100 Exotic Paper Airplanes)", "")

        wVideoEntry["Clean Title"] = wTitle
        print(wTitle)

        wlink = "<li>"
        wlink += "<a href=\"./" + wKey + ".html\">" + wTitle + "</a>"
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
