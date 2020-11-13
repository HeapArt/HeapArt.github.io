
window.onload = (event) => {

  var wHead = document.getElementsByTagName("head")[0];
  wHead.innerHTML += '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">';
  wHead.innerHTML += '<link rel="stylesheet" href="/site/css/commonTask.css">';
  

  var wSocialLinkDiv = document.getElementsByClassName("class_social_links");

  for(var wi = 0; wi < wSocialLinkDiv.length; ++wi){
  //  wSocialLinkDiv[wi].innerHTML += '<a href="https://www.youtube.com/c/heapart?sub_confirmation=1" class="fa fa-linkedin class_social_link"></a>'
    wSocialLinkDiv[wi].innerHTML += '<a href="https://www.youtube.com/c/heapart?sub_confirmation=1" class="fa fa-youtube class_social_link"></a>'
    wSocialLinkDiv[wi].innerHTML += '<a href="https://www.instagram.com/wlee0515/" class="fa fa-instagram class_social_link"></a>'
    wSocialLinkDiv[wi].innerHTML += '<a href="https://www.tiktok.com/@heapart" class="class_tiktok class_social_link"><img class="class_tiktok_logo" src="/site/images/logo-tiktok.png" alt="Tik Tok"/></img> </a>'
  }

  window.addEventListener("resize", resizeYTIFrame);

  resizeYTIFrame();
  console.log('page is fully loaded');

}; 

function resizeYTIFrame() {
  var wYTIFrame = document.getElementsByClassName("class_youtube_iframe");
  for (var wi = 0; wi < wYTIFrame.length; ++wYTIFrame) {
    wYTIFrame[wi].style.height = wYTIFrame[wi].offsetWidth * (9/16) + "px";
  }

}