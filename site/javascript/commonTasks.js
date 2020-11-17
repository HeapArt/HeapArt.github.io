// Global variables
function blockDefinition(iDOMViewPoint, iHTMLString) {
  return {
    DOM : iDOMViewPoint,
    HTMLString : iHTMLString
  }
}
var gBlockBank = new Array();

const gClass_site_block = "class_site_block";

// Load Function
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
    wSocialLinkDiv[wi].style.visibility = "hidden";
    //  wSocialLinkDiv[wi].innerHTML += '<a href="https://www.youtube.com/c/heapart?sub_confirmation=1" class="fa fa-linkedin class_social_link"></a>';
    wSocialLinkDiv[wi].innerHTML += '<a href="https://www.youtube.com/c/heapart" class="class_social_link"><img src="/site/images/logo/logo-youtube.png"/></a>';
    wSocialLinkDiv[wi].innerHTML += '<a href="https://www.instagram.com/wlee0515/" class="class_social_link"><img src="/site/images/logo/logo-instagram.png"/></a>';
    wSocialLinkDiv[wi].innerHTML += '<a href="https://www.tiktok.com/@heapart" class="class_social_link"><img src="/site/images/logo/logo-tiktok.png"/></a>';
  }
  
  setTimeout(function() {
    var wSocialLinkDiv = document.getElementsByClassName("class_social_links_bar");
    for (var wi = 0; wi < wSocialLinkDiv.length; ++wi) {
      wSocialLinkDiv[wi].style.visibility = "visible";
    }
  }, 200);

  // Add Event listener to resize YouTube Iframe
  window.addEventListener('resize', resizeYTIFrame);
  setTimeout(resizeYTIFrame, 500);
  console.log('page is fully loaded');

  setInterval(iteration, 500);
};

// Iteration function
function iteration() {

  /*
  if (0 != gBlockBank.length) {
    for(var wi = 0; wi < gBlockBank.length; ++wi) {
      var wElementBlock = gBlockBank[wi];
      if ("" == wElementBlock.DOM.innerHTML){
        if( true == isInViewport(wElementBlock.DOM)) {
          wElementBlock.DOM.innerHTML = wElementBlock.HTMLString;
          break;
        }
      }
    }
  }
  */

  var wBlockList = document.getElementsByClassName(gClass_site_block);
  if (null != wBlockList) {
    for(var wi = 0; wi < wBlockList.length; ++wi) {
      var wElementBlock = wBlockList[wi];
      if ("visible" != wElementBlock.style.visibility)
      {
        if( true == isInViewport(wElementBlock)) {
          wElementBlock.style.visibility="visible";
          break;
        }  
      }
    }
  }
}

function isInViewport(element) {
  const rect = element.getBoundingClientRect();
  return ( rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.left <= (window.innerWidth || document.documentElement.clientWidth));
}


function resizeYTIFrame() {
  var wYTIFrame = document.getElementsByClassName("class_YouTubePlayer");
  for (var wi = 0; wi < wYTIFrame.length; ++wi) {
    wYTIFrame[wi].style.height = wYTIFrame[wi].offsetWidth * (9 / 16) + "px";
  }
}


// NavBar Generation
function generateEntryString(iJson) {

  var wTemp = "";

  if (null != iJson.siteName) {

    if (null != iJson.icon) {
      wTemp = "<img src='" + iJson.icon + "' class='class_navbar_icon_img'></img>";
    }
    wTemp = "<div class='class_navbar_icon_container'>" + wTemp + "</div>";
    wTemp += "<div class='class_navbar_label'>" + iJson.siteName + "</div>";
    wTemp = "<div class='class_navbar_label_wrapper'>" + wTemp + "</div>";
    
    if (null != iJson.link) {
      wTemp = "<a href='" + iJson.link + "' class='class_navbar_link'>" + wTemp + "</a>";
    }
    

    if (null != iJson.sub_entries) {
      for (var wj = 0; wj < iJson.sub_entries.length; ++wj) {
        wTemp += "<div class='class_navbar_subentry' onclick='navebarSubEntryExpand(this)' >" + generateEntryString(iJson.sub_entries[wj]) + "</div>";
      }   
    }
  }

  return wTemp;
}

function navebarExpand(iMenuButton) {
  iMenuButton.classList.toggle("navBarExpand");
  iMenuButton.parentElement.classList.toggle("navBarExpand");
}

function navebarSubEntryExpand(iEntry) {
  iEntry.classList.toggle("class_navbar_subentry_expand");
}


function createNavigationBar(iFetchJson) {
  fetch(iFetchJson)
    .then((response) => {
      return response.json()
    })
    .then((data) => {
      var wInnerHtml = "";

      if (null != data.siteName) {
        wInnerHtml += "<div class='class_navbar_HomePage'>" + generateEntryString(data) + "</div>";
      }
      if (null != data.entries) {
        var wEntriesStr = "";
        for (var wi = 0; wi < data.entries.length; ++wi) {
          wEntriesStr += "<div class='class_navbar_entry' onclick='navebarSubEntryExpand(this)'>" + generateEntryString(data.entries[wi]) + "</div>";
        }

        if ("" != wEntriesStr) {

          var wMenuIcon = '<div class="class_navbar_MenuIcon" onclick="navebarExpand(this)">';
          wMenuIcon += '<div class="class_navbar_MenuIcon_bar1"></div>';
          wMenuIcon += '<div class="class_navbar_MenuIcon_bar2"></div>';
          wMenuIcon += '<div class="class_navbar_MenuIcon_bar3"></div>';
          wMenuIcon += '</div>';

          wInnerHtml +="<div class='class_navbar_entries'>" +  wMenuIcon + wEntriesStr + "</div>";
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


// Block Generation

function genBlockString(iJson) {
  var wTemp = "";
  if (null != iJson.title) wTemp += "<h2>" + iJson.title + "</h2>";
  if (null != iJson.date) wTemp += "<p>" + iJson.date + "</p>";
  if (null != iJson.body) {
    wTemp += "<div class='class_site_block_body'>";
    for (var wj = 0; wj < iJson.body.length; ++wj) {
      wTemp += iJson.body[wj];
    }
    wTemp += "</div>";
  }

  if (null != iJson.caption) {
    if ("video" == iJson.caption.type) {
      if (null != iJson.caption.videoId) {
        var wVideoId = iJson.caption.videoId
        var wDOMString = '<iframe class="class_YouTubePlayer" src="https://www.youtube.com/embed/'
        wDOMString += wVideoId;
        wDOMString += '" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>';
        wTemp += wDOMString;
      }
      else if (null != iJson.caption.playlistId) {
        var wPlayListId = iJson.caption.playlistId
        var wDOMString = '<iframe class="class_YouTubePlayer" src="https://www.youtube.com/embed/videoseries?list=PL'
        wDOMString += wPlayListId;
        wDOMString += '" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>';
        wTemp += wDOMString;
      }
    }
    else if ("image" == iJson.caption.type) {
      if (null != iJson.caption.src) {
        var wDOMString = '<img class="class_block_image" src="'+ iJson.caption.src + '"/>';
        wTemp += wDOMString;
      }    
    }
  }

  if ("" != wTemp){
    return wTemp;
  }
  return "";
}

function loadSiteBlock(iElementId, iFetchJson, iReverse) {
  var wElement = document.getElementById(iElementId);
  if (null != wElement) {
    fetch(iFetchJson)
      .then((response) => {
        return response.json()
      })
      .then((data) => {
        var wCount = data.length;
        if (0 != wCount) {

          if ((null == iReverse) || (false == iReverse)) {
            for (var wi = 0; wi < wCount; ++wi) {
              var wBlockString = genBlockString(data[wi]);
              if (""!= wBlockString) {
                var wNewDiv = document.createElement("DIV");
                wNewDiv.classList.add(gClass_site_block);
                gBlockBank.push(blockDefinition(wNewDiv, wBlockString));
                wNewDiv.innerHTML = wBlockString;
                wNewDiv.style.display = "block";
                wNewDiv.style.visibility = "hidden";
                wElement.appendChild(wNewDiv);  
              }
            }  
          }
          else {
            for (var wi = wCount - 1; wi >= 0; --wi) {
              var wBlockString = genBlockString(data[wi]);
              if (""!= wBlockString) {
                var wNewDiv = document.createElement("DIV");
                wNewDiv.classList.add(gClass_site_block);
                gBlockBank.push(blockDefinition(wNewDiv, wBlockString));
                wNewDiv.innerHTML = wBlockString;
                wNewDiv.style.display = "block";
                wNewDiv.style.visibility = "hidden";
                wElement.appendChild(wNewDiv);  
              }
            }  
          }
        }
      })
      .catch((err) => {
        // Do something for an error here
      })
  }
}
