var bigScreen = document.getElementById("bigvideo");
var tempText = document.getElementById("temporary_text");
var playButton = document.getElementById("playbutton");
var pauseButton = document.getElementById("pausebutton");
var resetButton = document.getElementById("resetbutton");
// var bigvideo = document.getElementById("bigvideo_file");
var video;


time = 0

document.querySelectorAll('.single_video').forEach(item => {
    item.addEventListener('mousedown', function() {
      //handle click
      bigScreen.style.width = "100%";
      bigScreen.style.height = "100%";
      var sourceFile = item.getElementsByTagName("source")[0].src
      tempText.style.display = "none";
      if(bigScreen.firstChild){
        bigScreen.firstChild.src = sourceFile
      }
      else {
        video = document.createElement("video");
        video.src = sourceFile
        video.className = 'bigvideo_file'
        video.id = 'bigvideo_file'
        bigScreen.appendChild(video);
      }
      time = sourceFile.split('#')[1]
      time = time.substring(2).split(',');
      console.log(time)
      document.querySelectorAll('.mediabuttons').forEach(elem => elem.style.display="inline")
    })
})


playButton.addEventListener("click", function() {
  console.log(video.currentTime);
  video.play();
  console.log(time);
  setInterval(function () {
    if (video.currentTime < parseFloat(time[0]) || video.currentTime > parseFloat(time[1])){
      video.currentTime = parseFloat(time[0]);
    }
  }, 300);
  
})

pauseButton.addEventListener("click", function() {
  console.log(video.currentTime);
  video.pause();
})

video.addEventListener("timeupdate", function() {
  console.log('skdfkjsdf')
  
})




// bigScreen.addEventListener('mousedown', function() {
  

// })



// document.querySelectorAll('.single_video').forEach(item => {
//     item.addEventListener('mouseout', function() {
//       //handle click
//       console.log(item.class)
//       this.pause()
//     })
// })