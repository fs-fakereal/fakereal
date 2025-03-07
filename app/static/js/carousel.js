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

// show slides
function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    let dots = document.getElementsByClassName("dot");

    if (n > slides.length) {
        slideIndex = 1;
    }

    if (n < 1) {
        slideIndex = slides.length;
    }

    for (i=0; i<slides.length; i++) {
        slides[i].style.display = 'none';
    }

    for (i=0; i<dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }

    slides[slideIndex-1].style.display = "block flex";
    dots[slideIndex-1].className += " active";
}

// select the example list
const wrapper = document.querySelector('.example-list');

window.addEventListener('scroll', ()=> {
    const scrollPosition = window.scrollY;

    const maxScroll = document.body.scrollHeight - window.innerHeight;

    // calculates the percentage of scrolling relative
    const scrollPercentage = scrollPosition / maxScroll;

    const translateX = scrollPercentage * 100;

    wrapper.style.transform = `translate3d(${translateX}%, 0, 0)`;
})