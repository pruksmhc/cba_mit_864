 function instant() {
    var wavesurfer = WaveSurfer.create({
    container: '#waveform',
    waveColor: '#D2EDD4',
    progressColor: 'red'
    progressColor: '#46B54D'
});

wavesurfer.on('ready', function () {
// code that runs after wavesurfer is ready
console.log('Success');
});

      wavesurfer.load('final-project-front.wav');
  }
