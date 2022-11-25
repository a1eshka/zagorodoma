$(document).ready(function() {
  $('.slider').slick({
    accessibility: true,
    arrows: true,
    prevArrow: '<div class="carousel-control-prev"><span class="carousel-control-prev-icon" aria-hidden="true"></span></div>',
    nextArrow: '<div class="carousel-control-next"><span class="carousel-control-next-icon" aria-hidden="true"></span></div>',
    dots: true,
    autoplay: false,
  });
  $('.price-main-card').text((i, text) => {
    const [ price, currency ] = text.split(' ');
    return `${(+price).toLocaleString()} ${currency}`;
  });
  $("#id_phone").mask("+7 (999) 999-99-99");
});
