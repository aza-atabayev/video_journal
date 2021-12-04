// const files = ["data/video/test.mp4", "data/video/test.mp4", "data/video/test.mp4", "data/video/test.mp4"]
// files.forEach(displayFile)

// function displayFile(value, index, array) {
//     console.log(value)
//     var container = document.createElement('div')
//     container.setAttribute("id", value)
//     container.className = "container"
//     var video = document.createElement('video')
//     var date = document.createElement('p')
//     video.className = "video_file"
//     date.innerHTML = value
//     video.src = value+"#t=3,5"
//     // video.setAttribute("controls","controls")
//     container.appendChild(video)
//     container.appendChild(date)
//     document.getElementById("list_container").appendChild(container)
// }

// var container = document.getElementsByClassName("container")

const pos = document.createTextNode("That was a great day!");
const neg = document.createTextNode("Keep going, it's okay!");

var pos_p = document.getElementById("1");
pos_p.appendChild(pos);
pos_p.className = "positive";
var neg_p = document.getElementById("0");
neg_p.appendChild(neg);
neg_p.className = "negative";

document.querySelectorAll('.container').forEach(item => {
    item.addEventListener('mousedown', event => {
      //handle click
      console.log(item.id)
      window.location.href = "/report?video=" + item.id;
    })
  })