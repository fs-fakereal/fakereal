let slideIndex = 1;
showSlides(slideIndex);

// next-previous controls
function plusSlides(n) {
    showSlides(slideIndex += n);
}

// image controls
function currentSlide(n) {
    showSlides(slideIndex = n);
}

