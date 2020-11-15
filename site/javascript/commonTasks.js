
window.onload = (event) => {


  // 2. This code loads the IFrame Player API code asynchronously.
  var tag = document.createElement('script');

  tag.src = "https://www.youtube.com/iframe_api";
  var firstScriptTag = document.getElementsByTagName('script')[0];
  firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);


  var wHead = document.getElementsByTagName("head")[0];
  wHead.innerHTML += '<script src="https://www.youtube.com/iframe_api"></script>';
  wHead.innerHTML += '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.15.1/css/all.css">';
  wHead.innerHTML += '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.15.1/css/v4-shims.css">';
  wHead.innerHTML += '<link rel="stylesheet" href="/site/css/commonTask.css">';

  var wSocialLinkDiv = document.getElementsByClassName("class_social_links_bar");

  for (var wi = 0; wi < wSocialLinkDiv.length; ++wi) {
    //  wSocialLinkDiv[wi].innerHTML += '<a href="https://www.youtube.com/c/heapart?sub_confirmation=1" class="fa fa-linkedin class_social_link"></a>'
    wSocialLinkDiv[wi].innerHTML += '<a href="https://www.youtube.com/c/heapart?sub_confirmation=1" class="fab fa-youtube class_social_link"></a>'
    wSocialLinkDiv[wi].innerHTML += '<a href="https://www.instagram.com/wlee0515/" class="fab fa-instagram class_social_link"></a>'
    wSocialLinkDiv[wi].innerHTML += '<a href="https://www.tiktok.com/@heapart" class="fab fa-tiktok class_social_link"></a>'
  }

  window.addEventListener('resize', resizeYTIFrame);

  resizeYTIFrame();
  console.log('page is fully loaded');

};

function resizeYTIFrame() {
  var wYTIFrame = document.getElementsByClassName("class_youtube_iframe");
  for (var wi = 0; wi < wYTIFrame.length; ++wi) {
    wYTIFrame[wi].style.height = wYTIFrame[wi].offsetWidth * (9 / 16) + "px";
  }

}

var gYTPlayerList = new Array();
var gIFrameApiReady = false;
var wPendingYouTubePlayers = new Array();

function createYouTubePlayers() {
  if (true == gIFrameApiReady)
  {
    for(var wi = 0; wi < wPendingYouTubePlayers.length; ++wi)
    {
      var wPlayer = new YT.Player(wPendingYouTubePlayers[wi].containerId, {
        height: '390',
        width: '640',
        videoId: wPendingYouTubePlayers[wi].videoId,
        events: {
          'onReady': onPlayerReady,
          'onStateChange': onPlayerStateChange
        }
      });

      gYTPlayerList.push(wPlayer);
    }

    wPendingYouTubePlayers.length = 0;
  }
}

function addPlayer(iContainerId, iVideoId) {
  wPendingYouTubePlayers.push({containerId : iContainerId, videoId : iVideoId});
  createYouTubePlayers();
}

function onYouTubeIframeAPIReady() {
  gIFrameApiReady = true;
  createYouTubePlayers();
  player = new YT.Player('player', {
    height: '390',
    width: '640',
    videoId: 'M7lc1UVf-VE',
    events: {
      'onReady': onPlayerReady,
      'onStateChange': onPlayerStateChange
    }
  });
}

// 4. The API will call this function when the video player is ready.
function onPlayerReady(event) {
  event.target.playVideo();
}
// 4. The API will call this function when the video player is ready.
function onPlayerReady(event) {
  event.target.playVideo();
}

// 5. The API calls this function when the player's state changes.
//    The function indicates that when playing a video (state=1),
//    the player should play for six seconds and then stop.
function onPlayerStateChange(event) {
}


function loadSiteBlock(iElementId, iFetchJson) {
  var wElement = document.getElementById(iElementId);
  if (null != wElement) {
    fetch(iFetchJson)
      .then((response) => {
        return response.json()
      })
      .then((data) => {
        var wCount = data.length;
        if (0 != wCount) {
          var wBlockString = "";
          for (var wi = wCount - 1; wi >= 0; --wi) {
            var wBlock = data[wi];
            var wTemp = "<div class='class_site_block'>";
            if (null != wBlock.title) wTemp += "<h2>" + wBlock.title + "</h2>";
            if (null != wBlock.date) wTemp += "<p>" + wBlock.date + "</p>";
            if (null != wBlock.body) {
              wTemp += "<div>";
              for (var wj = 0; wj < wBlock.body.length; ++wj) {
                wTemp += wBlock.body[wj];
              }
              wTemp += "</div>";
            }

            if (null != wBlock.caption) {
              if ("video" == wBlock.caption.type) {
                addPlayer(wBlock.caption.containerId, wBlock.caption.videoId);
              }
            }
            
            wTemp += "</div>";
            wBlockString += wTemp;
          }
          wElement.innerHTML += wBlockString;
        }
      })
      .catch((err) => {
        // Do something for an error here
      })
  }
}
