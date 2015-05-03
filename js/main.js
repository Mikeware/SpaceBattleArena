$(document).ready(function() {
  // Determine how far we need to scroll before we hit our navigation bar
  elementtop = Math.round($('nav').position().top);
  
  // Makes our Navigation Stick once we've scrolled so that it's at the top.
  $(window).scroll(function () {
    if ($(window).scrollTop() > elementtop) {
      $('nav').addClass('navbar-fixed');
      $('aside').addClass('aside-fixed');
    }
    if ($(window).scrollTop() < elementtop) {
      $('nav').removeClass('navbar-fixed');
      $('aside').removeClass('aside-fixed');
    }
  });
  
  // When our page loads, check to see if it contains and anchor
  scroll_if_anchor(window.location.hash);

  // Intercept all anchor clicks
  $("body").on("click", "a[href^='#']", scroll_if_anchor);
});

// Solution From: http://jsfiddle.net/ianclark001/aShQL/
/**
  * Check an href for an anchor. If exists, and in document, scroll to it.
  * If href argument omitted, assumes context (this) is HTML Element,
  * which will be the case when invoked by jQuery after an event
  */
function scroll_if_anchor(href) {
    href = typeof(href) == "string" ? href : $(this).attr("href");

    // If href missing, ignore
    if(!href) return;

    // If our Href points to a valid, non-empty anchor, and is on the same page (e.g. #foo)
    // Legacy jQuery and IE7 may have issues: http://stackoverflow.com/q/1593174
    var $target = $("a[name=" + href.substring(1) + "]");

    // Older browsers without pushState might flicker here, as they momentarily
    // jump to the wrong position (IE < 10)
    if($target.length) {
        $('html, body').animate({ scrollTop: $target.offset().top - 150 });
        if(history && "pushState" in history) {
            history.pushState({}, document.title, window.location.pathname + href);
            return false;
        }
    }
}    