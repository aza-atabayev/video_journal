const files = ["data/video/test.mp4", "data/video/test.mp4", "data/video/test.mp4", "data/video/test.mp4"]
files.forEach(displayFile)

function displayFile(value, index, array) {
    console.log(value)
    var container = document.createElement('div')
    container.setAttribute("id", value)
    container.className = "container"
    var video = document.createElement('video')
    var date = document.createElement('p')
    video.className = "video_file"
    date.innerHTML = value
    video.src = value+"#t=3,5"
    // video.setAttribute("controls","controls")
    container.appendChild(video)
    container.appendChild(date)
    document.getElementById("list_container").appendChild(container)
}

var container = document.addEventListener("click", loadFIle);

function loadFIle() {
    window.location.href ='/report'
}