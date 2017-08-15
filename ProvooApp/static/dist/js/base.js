

  /*!
  * Preloader
  */
  !function(){
      setTimeout(function(){
          $('.preloader').css({opacity: '0'}).one('transitionend webkitTransitionEnd oTransitionEnd otransitionend MSTransitionEnd', function() {
              $(this).hide();
          });
      }, 1000);
  }();
  