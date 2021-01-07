// Global variables
const gClass_YouTubePlayer = "class_YouTubePlayer";
const gClass_RandomYTVideo = "class_randomYTVideo"; 
const gClass_site_block = "class_site_block";

var gRandomSeed = Math.random();
function seededRandom(iMax, iMin) {

    gRandomSeed = (gRandomSeed * 9301 + 49297) % 233280;
    var wRandom = gRandomSeed / 233280;
 
    return iMin + wRandom * (iMax - iMin);
}

const gVideoListJsonPath = "/site/database/HeapArtVideoData.json";
var gVideoData =null;
function loadVideoList(iFunction){
  if (null == gVideoData) {
    fetch(gVideoListJsonPath)
      .then((response) => {
        return response.json()
      })
      .then((data) => {
        gVideoData = data;
        if (null != iFunction) iFunction(data);
        fillRandomYTVideoPlayers(data["Video List"]);
      })
      .catch((err) => {
        // Do something for an error here
      })
  }
  else {
    if (null != iFunction) iFunction(gVideoData["Video List"]);
  }
}

// Load Function
window.onload = (event) => {


  // Add Event listener to resize YouTube Iframe
  window.addEventListener('resize', resizeYTIFrame);
  setTimeout(resizeYTIFrame, 100);

  
  var wYTIFrame = document.getElementsByClassName(gClass_RandomYTVideo);
  if (wYTIFrame.length > 0)
  {
    loadVideoList();
  }

  console.log('page is fully loaded');
};


function getVideoWithTags(iTagList, iVideoList) {
  var wNewVideoList = new Array();

  for (var wi =0; wi < iVideoList.length; ++wi) {
    var wTagList = iVideoList[wi]["Video Tags"];
    if (null != wTagList) {
      var wMatch = true;
      for (var wj = 0; wj < iTagList.length; ++wj) {
        var wFound = false;
        for (var wk = 0; wk < wTagList.length; ++wk) {
          if (iTagList[wj] == wTagList[wk]) {
            wFound = true;
            break;
          }
        }
        if (false == wFound){
          wMatch = false;
          break;
        }
      }
      if (true == wMatch) {
        wNewVideoList.push(iVideoList[wi]);
      }
    }
  }
  return wNewVideoList;
} 

function fillRandomYTVideoPlayers(iVideoList)
{
  var wYTIFrame = document.getElementsByClassName(gClass_RandomYTVideo);
  for (var wi = 0; wi < wYTIFrame.length; ++wi) {
    var wDom = wYTIFrame[wi];
    var wList = iVideoList;
    var wTags = wDom.getAttribute("videoTags");
    if (null != wTags) {
      wList = getVideoWithTags(wTags.split(","),iVideoList);
    }
    var wSeed = wDom.getAttribute("randomSeed");
    var wRandom = Math.random()*wList.length;
    if (null != wSeed) {
      if ("date" == wSeed) {
        gRandomSeed = getDayCount();
      }
      wRandom = seededRandom(wList.length,0);
    }
    
    var wRandomVideoIndex = Math.floor(wRandom);

    wYTIFrame[wi].src = "https://www.youtube.com/embed/" + wList[wRandomVideoIndex]["Video"] + "?version=3&loop=1&playlist=" + wList[wRandomVideoIndex]["Video"];
  }

}

function resizeYTIFrame() {
  var wYTIFrame = document.getElementsByClassName(gClass_YouTubePlayer);
  for (var wi = 0; wi < wYTIFrame.length; ++wi) {
    wYTIFrame[wi].style.height = wYTIFrame[wi].offsetWidth * (9 / 16) + "px";
  }
}

function getDayCount() {
  var d = new Date();
  var n = d.getTime(); //milli seconds
  return Math.floor(n/(1000*3600*24));
}
