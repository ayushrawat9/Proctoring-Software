const roomName = JSON.parse(document.getElementById('room-name').textContent);
    const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat/'
        + roomName
        + '/'
    );


const video = document.getElementById('video')
var cameraStream = null;
Promise.all([
//  faceapi.nets.ssdMobilenetv1.loadFromUri('/static/models'),
  faceapi.nets.tinyFaceDetector.loadFromUri('/static/models'),
  faceapi.nets.faceLandmark68Net.loadFromUri('/static/models'),
  faceapi.nets.faceRecognitionNet.loadFromUri('/static/models'),
  faceapi.nets.faceExpressionNet.loadFromUri('/static/models'),
  faceapi.nets.ssdMobilenetv1.loadFromUri('/static/models')
]).then(startStreaming)

function startVideo() {
  navigator.mediaDevices.getUserMedia(
    { video: {} },
    stream => video.srcObject = stream,
    err => console.error(err)
  )
}
 function startStreaming() {

      var mediaSupport = 'mediaDevices' in navigator;

      if( mediaSupport && null == cameraStream ) {

        navigator.mediaDevices.getUserMedia( { video: true } )
        .then( function( mediaStream ) {

          cameraStream = mediaStream;

          video.srcObject = mediaStream;

          video.play();
        })
        .catch( function( err ) {
          console.log( "Unable to access camera: " + err );

        });
      }
      else {
        alert( 'Your browser does not support media devices.' );
        return;
      }
    }


video.addEventListener('play', () => {
  const canvas = faceapi.createCanvas(video)
  canvas.id = "canvas";
  document.querySelector("#video").append(canvas);
  document.body.append(canvas);
  const displaySize = { width: video.width, height: video.height }
  faceapi.matchDimensions(canvas, displaySize)
  setInterval(async () => {
    const detections = await faceapi.detectAllFaces(video, new faceapi.Tin).withFaceLandmarks()
    if(detections.length == 0)
    {
                chatSocket.send(JSON.stringify({
                'message': "user not found"
            }));
    }
    const resizedDetections = faceapi.resizeResults(detections, displaySize)
    canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height)
    faceapi.draw.drawDetections(canvas, resizedDetections)
    faceapi.draw.drawFaceLandmarks(canvas, resizedDetections)
    faceapi.draw.drawFaceExpressions(canvas, resizedDetections)
  }, 100)
})