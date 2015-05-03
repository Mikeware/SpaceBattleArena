$(document).ready(function() {
  elementtop = Math.round($('nav').position().top);
  
  $(window).scroll(function () {
    if ($(window).scrollTop() > elementtop) {
      $('nav').addClass('navbar-fixed');
    }
    if ($(window).scrollTop() < elementtop) {
      $('nav').removeClass('navbar-fixed');
    }
  });
});