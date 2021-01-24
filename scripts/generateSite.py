import os
import json

gWorkingDirectory = "../"
gInputFile = ["scripts/sitePageDefinition.json", "scripts/sitePageDefinition_Images.json"]

def loadJson(iFilePath):
    with open(iFilePath, encoding="utf-8") as f:
        return json.load(f)
    return None

def save_file(iPath, iText):
    wBasedir = os.path.dirname(iPath)

    if "" != wBasedir:
        if not os.path.exists(wBasedir):
            os.makedirs(wBasedir)

    with  open(iPath, 'w', encoding="utf-8")  as wFile:
        wFile.write(iText)
        wFile.close()

def generateSite(iSitePageDefinitionJSON, iSiteGenerationFile):
    #print(iSitePageDefinitionJSON);
    #print(iSiteGenerationFile);

    if "pages" in iSitePageDefinitionJSON:
        for wPage in iSitePageDefinitionJSON["pages"]:
            generatePage(wPage, iSitePageDefinitionJSON, iSiteGenerationFile)

    if "catalogue_Directory" in iSitePageDefinitionJSON:
        for wCatalogueDir in iSitePageDefinitionJSON["catalogue_Directory"]:
            for (wDirpath, wDirnames, wFilenames) in os.walk(wCatalogueDir["path"]):
                for wFile in wFilenames:                    
                    wFullFileName = os.path.join(wDirpath, wFile)
                    wPageObject = loadJson(wFullFileName)
                    if None != wPageObject:                    
                        wPageObject["output_path"] = wFullFileName.replace(wCatalogueDir["path"], wCatalogueDir["output_path"]).replace(".json",".html")
                        generatePage(wPageObject, iSitePageDefinitionJSON, iSiteGenerationFile)


def generatePage(iPageDefinition, iSitePageDefinitionJSON, iSiteGenerationFile):

    wPageDefinition = {}
    for wItem in iSitePageDefinitionJSON.items():
        if wItem[0] != "pages":
            if wItem[0] != "siteGenerationFile":
                wPageDefinition[wItem[0]] = wItem[1]
        
    for wItem in iPageDefinition.items():
        wPageDefinition[wItem[0]] = wItem[1]

    #print()
    #print(wPageDefinition)
    wTemplateFile = open(wPageDefinition["template"], "r")
    wFileString = wTemplateFile.read()
    
    js_scrpts = ""
    if "js_list" in iSiteGenerationFile:
        for wFile in iSiteGenerationFile["js_list"]:
          js_scrpts += '<script src="{0}"></script>'.format(wFile)
    if "js_list" in wPageDefinition:
        for wFile in wPageDefinition["js_list"]:
          js_scrpts += '<script src="{0}"></script>'.format(wFile)
    wFileString = wFileString.replace("[%js_list%]", js_scrpts)
    

    css_links = ""
    if "css_list" in iSiteGenerationFile:
        for wFile in iSiteGenerationFile["css_list"]:
          css_links += '<link rel="stylesheet" href="{0}">'.format(wFile)
    if "css_list" in wPageDefinition:
        for wFile in wPageDefinition["css_list"]:
          css_links += '<link rel="stylesheet" href="{0}">'.format(wFile)
    wFileString = wFileString.replace("[%css_list%]", css_links)

    if "tag_map" in iSiteGenerationFile:
        for wTag in iSiteGenerationFile["tag_map"]:
          wReplaceTag = wTag["tag"]
          wParameter = ""

          if "parameter" in wTag:
              if wTag["parameter"] in wPageDefinition:
                  wParameter = wPageDefinition[wTag["parameter"]]
          elif "file" in wTag:
              wParameter = open(wTag["file"], "r").read()

          wModifiedParameter = wParameter

          if "" != wModifiedParameter:
            if "method" in wTag:
                wMethod = wTag["method"]
                if "parse_navbar" == wMethod:
                      wModifiedParameter = parse_navbar(wParameter, wPageDefinition)
                if "parse_blockfile" == wMethod:
                      wModifiedParameter = parse_blockfile(wParameter, wPageDefinition)
                if "parse_blocklist" == wMethod:
                      wModifiedParameter = parse_blocklist(wParameter, wPageDefinition)
                if "social_links_bar" == wMethod:
                      wModifiedParameter = social_links_bar(wParameter, wPageDefinition)
                  
          wFileString = wFileString.replace("[%{0}%]".format(wReplaceTag), wModifiedParameter)

    if "text_link_map" in iSiteGenerationFile:
        wFileStringPart = wFileString.split("<body>")
        wNewFileStringHead = wFileStringPart[0]
        wNewFileStringBody = ""
        for i in range (1 , len(wFileStringPart)):
            wNewFileStringBody = "<body>" + wFileStringPart[i]

        for wTextLink in iSiteGenerationFile["text_link_map"]:
            if "text" in wTextLink:
                if "link" in wTextLink:
                    wTextReplacement = "<a href=\"{0}\" target=\"_blank\" rel=\"noopener noreferrer\">{1}</a>".format(wTextLink["link"], wTextLink["text"])
                    wNewFileStringBody = wNewFileStringBody.replace( " " + "{0}".format(wTextLink["text"]), " " + wTextReplacement)
        wFileString = wNewFileStringHead + wNewFileStringBody

    save_file(wPageDefinition["output_path"], wFileString)
    print("Generated File [{0}]".format(wPageDefinition["output_path"]))


def generateNavBarEntryString(iEntry):
    wTemp = ""
    if "siteName" in iEntry:
        if "icon" in iEntry:
            wTemp += "<img src='{0}' class='class_navbar_icon_img'></img>".format(iEntry["icon"])

        wTemp = "<div class='class_navbar_icon_container'>{0}</div>".format(wTemp)
        wTemp += "<div class='class_navbar_label'>{0}</div>".format(iEntry["siteName"])
        wTemp = "<div class='class_navbar_label_wrapper'>{0}</div>".format(wTemp)
    
        if "link" in iEntry:
            wTemp = "<a href='{0}' class='class_navbar_link'>{1}</a>".format(iEntry["link"], wTemp)
    
        if "sub_entries" in iEntry:
            for wSubEntry in iEntry["sub_entries"]:
                wEntryString = generateNavBarEntryString(wSubEntry)
                if "" != wEntryString:
                    wTemp += "<div class='class_navbar_subentry' onclick='navebarSubEntryExpand(this)' style='z-index:200;'>{0}</div>".format(wEntryString)

    return wTemp


def parse_navbar(iParameter, iPageDefinition):
    wNavBar = loadJson(iParameter)

    wInnerHtml = ""

    if "siteName" in wNavBar:
        wInnerHtml += "<div class='class_navbar_HomePage'>" + generateNavBarEntryString(wNavBar) + "</div>"

    if "entries" in wNavBar:
        wEntriesStr = ""

        wEntryCount = len(wNavBar["entries"]);
        for wEntry in wNavBar["entries"]:
            wEntryString = generateNavBarEntryString(wEntry)
            if "" != wEntryString:
                wEntriesStr += "<div class='class_navbar_entry'  onclick='navebarSubEntryExpand(this)' style='z-index:{1};'>{0}</div>".format(wEntryString, 100 + wEntryCount)
            wEntryCount -= 1

        wMenuIcon = ""
        if "" != wEntriesStr:
            wMenuIcon = '<div class="class_navbar_MenuIcon" onclick="navebarExpand(this)">'
            wMenuIcon += '<div class="class_navbar_MenuIcon_inner">'
            wMenuIcon += '<div class="class_navbar_MenuIcon_bar1"></div>'
            wMenuIcon += '<div class="class_navbar_MenuIcon_bar2"></div>'
            wMenuIcon += '<div class="class_navbar_MenuIcon_bar3"></div>'
            wMenuIcon += '</div>'
            wMenuIcon += '</div>'

        wInnerHtml = wMenuIcon + wInnerHtml + "<div class='class_navbar_entries'>" + wEntriesStr + "</div>"

    if "" != wInnerHtml:

        wNavBar = "<div class='class_navbar'>" + wInnerHtml + "</div>"

        wCode = 'function navebarExpand(iMenuButton) { iMenuButton.classList.toggle("navBarExpand");iMenuButton.parentElement.classList.toggle("navBarExpand");}'
        wCode += 'function navebarSubEntryExpand(iEntry) {iEntry.classList.toggle("class_navbar_subentry_expand");}'
        wScript = '<script>{0}</script>'.format(wCode)

        return wNavBar + wScript

    return ""


def genBlockString(iBlock):
    wTemp = ""
    if "title" in iBlock:
        wTemp += "<h2>{0}</h2>".format(iBlock["title"])
  
    if "date" in iBlock:
        wTemp += "<p>{0}</p>".format(iBlock["date"])
  
    wBodyString = ""
    if "body" in iBlock:
        wBodyString += "<div class='class_site_block_body'>"
        for wLine in  iBlock["body"]:
            wBodyString += wLine.replace("\n","</br>")
        wBodyString += "</div>"
  
    wCaptionString = ""
    if "caption" in iBlock:
    
        wType = iBlock["caption"]["type"]
  
        if "video" == wType:
            if "videoId" in iBlock["caption"]:
                wDOMString = '<iframe class="class_YouTubePlayer" src="https://www.youtube.com/embed/{0}?version=3&loop=1&playlist={0}"'.format(iBlock["caption"]["videoId"])
                wDOMString += ' frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
                wCaptionString += wDOMString
  
            if "playlistId" in iBlock["caption"]:
                wDOMString = '<iframe class="class_YouTubePlayer" src="https://www.youtube.com/embed/videoseries?list=PL'
                wDOMString += iBlock["caption"]["playlistId"]
                wDOMString += '" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
                wCaptionString += wDOMString
  
            if "randomVideoId" in iBlock["caption"]:
                wDOMString = '<iframe class="class_YouTubePlayer class_randomYTVideo"'
                if "randomSeed" in iBlock["caption"]:
                    wDOMString += ' randomSeed="{0}"'.format( iBlock["caption"]["randomSeed"])
  
                wDOMString += ' videoTags="{0}"'.format(iBlock["caption"]["randomVideoId"])
                wDOMString += ' frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'

                wCaptionString += wDOMString
  
  
        if "image" == wType:
            if "src" in iBlock["caption"]:
                wCaptionString += '<img class="class_block_image" src="{0}"/>'.format(iBlock["caption"]["src"])
  
        if "" != wCaptionString:
            wCaptionString = "<div class='class_site_block_caption'>{0}</div>".format(wCaptionString)
  
    if "" != wCaptionString:
        if "beforeBody" in iBlock["caption"]:
            if True == iBlock["caption"]["beforeBody"]:
                wTemp+=wCaptionString+wBodyString
            else:
                wTemp+=wBodyString+wCaptionString    
        else:
            wTemp+=wBodyString+wCaptionString

    else:
        wTemp+=wBodyString


    if "" != wTemp:
        return "<div class='class_site_block'>{0}</div>".format(wTemp)
  
    return ""



def parse_blockfile(iParameter, iPageDefinition):
    wBlockList = loadJson(iParameter)
    return parse_blocklist(wBlockList,iPageDefinition)

def parse_blocklist(iBlockList, iPageDefinition):
    wBlockReverse = False
    if "block_direction" in iPageDefinition:
        if "reverse" == iPageDefinition["block_direction"]:
            wBlockReverse = True

    if wBlockReverse:
        iBlockList.reverse()

    wBlockString = ""
    for wBock in iBlockList:
        wBlockString += genBlockString(wBock)

    return '<div class="class_block_list">{0}</div>'.format(wBlockString)


def social_links_bar(iParameter, iPageDefinition):
    wSocialLinks = loadJson(iParameter)
    
    wLinks = ""
    for wPlateform in wSocialLinks["links"]:
        wLinks += '<a href="{0}" class="class_social_link"><img src="{1}" alt="{2}"/></a>'.format(wPlateform["link"],wPlateform["icon"],wPlateform["name"]);

    return '<div class="class_social_links_bar">{0}</div>'.format(wLinks)

def main():
    os.chdir(gWorkingDirectory)

    print(os.getcwd())

    for wInputDefinition in gInputFile:
        wSitePageDef = loadJson(wInputDefinition)
        print("Using Site Page Definition : {0}".format(wInputDefinition))

        wGenFile = wSitePageDef["siteGenerationFile"]
        wSiteGenDef =  loadJson(wGenFile)
        print("Using Site Generation File : {0}".format(wGenFile))

        generateSite(wSitePageDef, wSiteGenDef)
    

if __name__ == '__main__':
    main()
