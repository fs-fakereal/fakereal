// let slideIndex = 1;
// showSlides(slideIndex);

const { query } = require("express");

// // next-previous controls
// function plusSlides(n) {
//     showSlides(slideIndex += n);
// }

// // image controls
// function currentSlide(n) {
//     showSlides(slideIndex = n);
// }

// // show slides
// function showSlides(n) {
//     let i;
//     let slides = document.getElementsByClassName("mySlides");
//     let dots = document.getElementsByClassName("dot");

//     if (n > slides.length) {
//         slideIndex = 1;
//     }

//     if (n < 1) {
//         slideIndex = slides.length;
//     }

//     for (i=0; i<slides.length; i++) {
//         slides[i].style.display = 'none';
//     }

//     for (i=0; i<dots.length; i++) {
//         dots[i].className = dots[i].className.replace(" active", "");
//     }

//     slides[slideIndex-1].style.display = "block flex";
//     dots[slideIndex-1].className += " active";
// }


// Interactive scrolling
const wrapper = document.querySelector('.example-list'); // Wrapper of the list
const articles = document.querySelector('.articles');
const footer = document.querySelector('.footer');

// Listen for the scroll event, but only act when the section is in view
window.addEventListener('scroll', () => {
  for (let i = 0; i < wrapper.children.length; i++) {
    tranform(wrapper.children[i]);
  
    // Check if the list has scrolled to the end
    if (wrapper.scrollLeft + wrapper.offsetWidth >= wrapper.scrollWidth) {
      // Hide the articles and footer while scrolling
      articles.style.display = 'none';
      footer.s 
      // Show the articles and footer once scrolled to the end
      articles.style.display = 'block';
      footer.style.display = 'block';
    }
  }
});

function tranform(child) {
  const offsetTop = child.offsetTop;
  const scrollSection = child.querySelector('.example');
  let percentage = ((wrapper.scrollLeft - offsetLeft) / wrapper.offsetHeight) * 100;
  scrollSection.style.transform = `translateX(-${percentage}%)`;
}
