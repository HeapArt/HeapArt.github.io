
window.onload = (event) => {

  var wHead = document.getElementsByTagName("head")[0];
  wHead.innerHTML += '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">';
  wHead.innerHTML += '<link rel="stylesheet" href="/site/css/commonTask.css">';
  

  var wSocialLinkDiv = document.getElementsByClassName("class_social_links");

  for(var wi = 0; wi < wSocialLinkDiv.length; ++wi){
  //  wSocialLinkDiv[wi].innerHTML += '<a href="https://www.youtube.com/c/heapart?sub_confirmation=1" class="fa fa-linkedin"></a>'
    wSocialLinkDiv[wi].innerHTML += '<a href="https://www.youtube.com/c/heapart?sub_confirmation=1" class="fa fa-youtube"></a>'
    wSocialLinkDiv[wi].innerHTML += '<a href="https://www.instagram.com/wlee0515/" class="fa fa-instagram"></a>'
    wSocialLinkDiv[wi].innerHTML += '<a href="https://www.tiktok.com/@heapart" >TikTok</a>'


  }

  console.log('page is fully loaded');

}; 