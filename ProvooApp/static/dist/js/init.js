/*----------------------------------------------------*/
/*-------------------Carousel-------------------------*/
/*----------------------------------------------------*/
    $('.carousel').carousel(
        {
            fullWidth: true,
            indicators: true,
            duration: 100
        }
    );

    $('.carousel.carousel-slider').carousel({
        fullWidth: true,
        indicators: true,
        duration: 100,

    });

$(document).ready(function () {
  $('select').material_select();
    /*----------------------------------------------------*/
    /*  Video
     ------------------------------------------------------*/
    var vid = document.getElementById("bgvid");
    var pauseButton = document.querySelector("#polina button");
    if (window.matchMedia('(prefers-reduced-motion)').matches) {
        vid.removeAttribute("autoplay");
        vid.pause();
        pauseButton.innerHTML = "Paused";
    }

    function vidFade() {
        vid.classList.add("stopfade");
    }

    vid.addEventListener('ended', function () {
        // only functional if "loop" is removed
        vid.pause();
        // to capture IE10
        vidFade();
    });
});