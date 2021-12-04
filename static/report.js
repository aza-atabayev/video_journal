document.querySelectorAll('.single_video').forEach(item => {
    item.addEventListener('mousedown', function() {
      //handle click
      console.log(item.class)
      this.play()
    })
})

// document.querySelectorAll('.single_video').forEach(item => {
//     item.addEventListener('mouseout', function() {
//       //handle click
//       console.log(item.class)
//       this.pause()
//     })
// })