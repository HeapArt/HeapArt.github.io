
window.onload = (event) => {

  // External Style Links
  var wHead = document.getElementsByTagName("head")[0];
  wHead.innerHTML += '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.15.1/css/all.css">';
  wHead.innerHTML += '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.15.1/css/v4-shims.css">';
  wHead.innerHTML += '<link rel="stylesheet" href="/site/css/commonTask.css">';

  // Create Navigation Bar
  createNavigationBar("/site/database/navigation.json")

  // Fill in Social media Links
  var wSocialLinkDiv = document.getElementsByClassName("class_social_links_bar");
  for (var wi = 0; wi < wSocialLinkDiv.length; ++wi) {
    //  wSocialLinkDiv[wi].innerHTML += '<a href="https://www.youtube.com/c/heapart?sub_confirmation=1" class="fa fa-linkedin class_social_link"></a>'
    wSocialLinkDiv[wi].innerHTML += '<a href="https://www.youtube.com/c/heapart" class="class_social_link"><img src="/site/images/logo/logo-youtube.png"/></a>'
    wSocialLinkDiv[wi].innerHTML += '<a href="https://www.instagram.com/wlee0515/" class="class_social_link"><img src="/site/images/logo/logo-instagram.png"/></a>'
    wSocialLinkDiv[wi].innerHTML += '<a href="https://www.tiktok.com/@heapart" class="class_social_link"><img src="/site/images/logo/logo-tiktok.png"/></a>'
  }

  // Add Event listener to resize YouTube Iframe
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

function createNavigationBar(iFetchJson) {
  fetch(iFetchJson)
    .then((response) => {
      return response.json()
    })
    .then((data) => {
      var wInnerHtml = "";

      if (null != data.siteName) {

        var wTemp = "";
        if (null != data.icon) {
          wTemp = "<img src='" + data.icon + "' class='class_navbar_icon_img'></img>";
        }
        wTemp = "<div class='class_navbar_icon_container'>" + wTemp + "</div>";
        wTemp += "<div class='class_navbar_label'>" + data.siteName + "</div>";
        if (null != data.link) {
          wTemp = "<a href='" + data.link + "' class='class_navbar_link'>" + wTemp + "</a>";
        }
        wInnerHtml += "<div class='class_navbar_HomePage'>" + wTemp + "</div>";
      }
      if (null != data.entries) {
        var wEntriesStr = "";
        for (var wi = 0; wi < data.entries.length; ++wi) {
          var wEntry = data.entries[wi];
          if (null != wEntry.siteName) {

            var wTemp = "";
            if (null != wEntry.icon) {
              wTemp = "<img src='" + wEntry.icon + "' class='class_navbar_icon_img'></img>";
            }
            wTemp = "<div class='class_navbar_icon_container'>" + wTemp + "</div>";
            wTemp += "<div class='class_navbar_label' class='class_navbar_link'>" + wEntry.siteName + "</div>";
            if (null != wEntry.link) {
              wTemp = "<a href='" + wEntry.link + "'>" + wTemp + "</a>";
            }
            else if (null != wEntry.sub_entries) {
              for (var wj = 0; wj < wEntry.sub_entries.length; ++wj) {
                var wSubEntry = wEntry.sub_entries[wj];
                if (null != wSubEntry.siteName) {

                  var wSubTemp = "";
                  if (null != wSubEntry.icon) {
                    wSubTemp = "<img src='" + wSubEntry.icon + "' class='class_navbar_icon_img'></img>";
                  }
                  wSubTemp = "<div class='class_navbar_icon_container'>" + wSubTemp + "</div>";
                  wSubTemp += "<div class='class_navbar_label'>" + wSubEntry.siteName + "</div>";
                  if (null != wSubEntry.link) {
                    wSubTemp = "<a href='" + wSubEntry.link + "' class='class_navbar_link'>" + wSubTemp + "</a>";
                  }
                  wTemp += "<div class='class_navbar_subentry'>" + wSubTemp + "</div>"
                }
              }
            }
            wEntriesStr += "<div class='class_navbar_entry'>" + wTemp + "</div>";
          }
        }
        if ("" != wEntriesStr) {
          wInnerHtml += "<div class='class_navbar_entries'>" + wEntriesStr + "</div>";
        }
      }

      if ("" != wInnerHtml) {
        var wNavBar = "<div class='class_navbar'>" + wInnerHtml + "</div>";
        document.body.innerHTML = "<div class='class_navbar_gap'>' + '</div>" +  document.body.innerHTML + wNavBar;
      }
    })
    .catch((err) => {
      // Do something for an error here
    })
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
                if (null != wBlock.caption.videoId) {
                  var wVideoId = wBlock.caption.videoId
                  var wDOMString = '<iframe class="class_YouTubePlayer" src="https://www.youtube.com/embed/'
                  wDOMString += wVideoId;
                  wDOMString += '" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>';
                  wTemp += wDOMString;
                }
                else if (null != wBlock.caption.playlistId) {
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
