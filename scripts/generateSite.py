import os
import json

gWorkingDirectory = "../"
gInputFile = "scripts/sitePageDefinition.json"

def loadJson(iFilePath):
    with open(iFilePath) as f:
        return json.load(f)
    return NULL

def generateSite(iSitePageDefinitionJSON, iSiteGenerationFile):
    #print(iSitePageDefinitionJSON);
    #print(iSiteGenerationFile);

    for wPage in iSitePageDefinitionJSON["pages"]:
        wTemp = {};
        for wItem in iSitePageDefinitionJSON.items():
          if wItem[0] != "pages":
              if wItem[0] != "siteGenerationFile":
                  wTemp[wItem[0]] = wItem[1]
        
        for wItem in wPage.items():
            wTemp[wItem[0]] = wItem[1]
        
        generatePage(wTemp, iSiteGenerationFile)
  

def save_file(iPath, iText):
    wBasedir = os.path.dirname(iPath)

    if "" != wBasedir:
        if not os.path.exists(wBasedir):
            os.makedirs(wBasedir)

    with  open(iPath, 'w') as wFile:
        wFile.write(iText)
        wFile.close()

def generatePage(iPageDefinition, iSiteGenerationFile):

    print(iPageDefinition)
    wTemplateFile = open(iPageDefinition["template"], "r")
    wFileString = wTemplateFile.read()
    
    js_scrpts = ""
    if "js_list" in iSiteGenerationFile:
        for wFile in iSiteGenerationFile["js_list"]:
          js_scrpts += '<script src="{0}"></script>'.format(wFile)
    if "js_list" in iPageDefinition:
        for wFile in iPageDefinition["js_list"]:
          js_scrpts += '<script src="{0}"></script>'.format(wFile)
    wFileString = wFileString.replace("[%js_list%]", js_scrpts)
    

    css_links = ""
    if "css_list" in iSiteGenerationFile:
        for wFile in iSiteGenerationFile["css_list"]:
          css_links += '<link rel="stylesheet" href="{0}">'.format(wFile)
    if "css_list" in iPageDefinition:
        for wFile in iPageDefinition["css_list"]:
          css_links += '<link rel="stylesheet" href="{0}">'.format(wFile)
    wFileString = wFileString.replace("[%css_list%]", css_links)

    if "tag_map" in iSiteGenerationFile:
        for wTag in iSiteGenerationFile["tag_map"]:
          wReplaceTag = wTag["tag"]
          wParameter = ""

          if "parameter" in wTag:
              wParameter = iPageDefinition[wTag["parameter"]]
          elif "file" in wTag:
              wParameter = open(wTag["file"], "r").read()

          wModifiedParameter = wParameter
          if "method" in wTag:
              wMethod = wTag["method"]
              if "parse_navbar" == wMethod:
                  wModifiedParameter = parse_navbar(wParameter, iPageDefinition)
              if "parse_block" == wMethod:
                  wModifiedParameter = parse_block(wParameter, iPageDefinition)
              if "social_links_bar" == wMethod:
                  wModifiedParameter = social_links_bar(wParameter, iPageDefinition)
                  
          wFileString = wFileString.replace("[%{0}%]".format(wReplaceTag), wModifiedParameter)

    save_file(iPageDefinition["output_path"], wFileString)
    print(wFileString)

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
            wMenuIcon += '<div class="class_navbar_MenuIcon_bar1"></div>'
            wMenuIcon += '<div class="class_navbar_MenuIcon_bar2"></div>'
            wMenuIcon += '<div class="class_navbar_MenuIcon_bar3"></div>'
            wMenuIcon += '</div>'

        wInnerHtml +="<div class='class_navbar_entries'>" +  wMenuIcon + wEntriesStr + "</div>"

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
  
    if "body" in iBlock:
        wTemp += "<div class='class_site_block_body'>"
        for wLine in  iBlock["body"]: 
            wTemp += wLine
        wTemp += "</div>"
  
  
    if "caption" in iBlock:
        wCaptionString = ""
  
        wType = iBlock["caption"]["type"]
  
        if "video" == wType:
            if "videoId" in iBlock["caption"]:
                wDOMString = '<iframe class="class_YouTubePlayer" src="https://www.youtube.com/embed/'
                wDOMString += iBlock["caption"]["videoId"]
                wDOMString += '" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
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
            wTemp += "<div class='class_site_block_caption'>{0}</div>".format(wCaptionString)
  
    if "" != wTemp:
        return "<div class='class_site_block'>{0}</div>".format(wTemp)
  
    return ""



def parse_block(iParameter, iPageDefinition):
    wBlockReverse = False
    if "block_direction" in iPageDefinition:
        if "reverse" == iPageDefinition["block_direction"]:
            wBlockReverse = True

    wBlockList = loadJson(iParameter)

    if wBlockReverse:
        wBlockList.reverse()

    wBlockString = ""
    for wBock in wBlockList:
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

    wSitePageDef = loadJson(gInputFile)
    print("Using Site Page Definition : {0}".format(gInputFile))

    wGenFile = wSitePageDef["siteGenerationFile"]
    wSiteGenDef =  loadJson(wGenFile)
    print("Using Site Generation File : {0}".format(wGenFile))

    generateSite(wSitePageDef, wSiteGenDef)
    





if __name__ == '__main__':
    main()
