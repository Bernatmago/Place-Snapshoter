
function getPlaceCanvas() {
   // does not always work, idk what does it deppend on
   var canvas = document
   .querySelector("mona-lisa-embed")
   .shadowRoot.querySelector("mona-lisa-canvas")
   .shadowRoot.querySelector("canvas")
   return canvas
 }
 
 function getCanvasData(canvas) {
   var context = canvas.getContext('2d')
   return context.getImageData(0, 0, 2000, 2000)
 }

 function getCanvasImage(canvas) {
    return canvas.toDataURL("image/png").replace("data:image/png;base64,", "")
 }

var place_canvas = getPlaceCanvas()
// Decoded string results in r place screenshot
var final_img = getCanvasImage(place_canvas)