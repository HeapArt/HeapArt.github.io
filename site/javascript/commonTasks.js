
window.onload = (event) => {


  // 2. This code loads the IFrame Player API code asynchronously.
  var tag = document.createElement('script');

  tag.src = "https://www.youtube.com/iframe_api";
  var firstScriptTag = document.getElementsByTagName('script')[0];
  firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);


  var wHead = document.getElementsByTagName("head")[0];
  wHead.innerHTML += '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.15.1/css/all.css">';
  wHead.innerHTML += '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.15.1/css/v4-shims.css">';
  wHead.innerHTML += '<link rel="stylesheet" href="/site/css/commonTask.css">';

  var wSocialLinkDiv = document.getElementsByClassName("class_social_links_bar");

  for (var wi = 0; wi < wSocialLinkDiv.length; ++wi) {
    //  wSocialLinkDiv[wi].innerHTML += '<a href="https://www.youtube.com/c/heapart?sub_confirmation=1" class="fa fa-linkedin class_social_link"></a>'
    wSocialLinkDiv[wi].innerHTML += '<a href="https://www.youtube.com/c/heapart" class="fab fa-youtube class_social_link"></a>'
    wSocialLinkDiv[wi].innerHTML += '<a href="https://www.instagram.com/wlee0515/" class="fab fa-instagram class_social_link"></a>'
    wSocialLinkDiv[wi].innerHTML += '<a href="https://www.tiktok.com/@heapart" class="fab fa-tiktok class_social_link"></a>'
  }

  window.addEventListener('resize', resizeYTIFrame);

  resizeYTIFrame();
  console.log('page is fully loaded');

};

function resizeYTIFrame() {
  var wYTIFrame = document.getElementsByClassName("class_YouTubePlayer");
  for (var wi = 0; wi < wYTIFrame.length; ++wi) {
    wYTIFrame[wi].style.height = wYTIFrame[wi].offsetWidth * (9 / 16) + "px";
  }

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
                if (null != wBlock.caption.videoId)
                {
                  var wVideoId = wBlock.caption.videoId
                  var wDOMString = '<iframe class="class_YouTubePlayer" src="https://www.youtube.com/embed/'
                  wDOMString += wVideoId;
                  wDOMString += '" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>';
                  wTemp += wDOMString;
                }
                else if (null != wBlock.caption.playlistId)
                {
                  var wPlayListId = wBlock.caption.playlistId
                  var wDOMString = '<iframe class="class_YouTubePlayer" src="https://www.youtube.com/embed/videoseries?list=PL'
                  wDOMString += wPlayListId;
                  wDOMString += '" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>';
                  wTemp += wDOMString;
                }
              }
            }

            wTemp += "</div>";
            wBlockString += wTemp;
          }
          wElement.innerHTML += wBlockString;
          resizeYTIFrame();
        }
      })
      .catch((err) => {
        // Do something for an error here
      })
  }
}
