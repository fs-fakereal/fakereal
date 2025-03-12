const stickySections = [...document.querySelectorAll('.deepfake-examples')]

window.addEventListener('scroll', (e) => {
  for (let i=0; i < stickySections.length; i++){
    transform(stickySections[i])
  }
})

// function transform(section){
//   const offsetTop = section.parentElement.offsetTop;
//   const scrollSection = section.querySelector('.example-list');
  
//   let percentage = ((window.scrollY - offsetTop) / window.innerHeight) * 100;
//   // percentage = percentage < 0 ? 0 : percentage > 340 ? 340 : percentage;
//   percentage = percentage < 0 ? 0 : percentage > scrollSection.offsetWidth ? scrollSection.offsetWidth : percentage;
  
//   // const maxTranslation = scrollSection.offsetWidth - window.innerWidth;
//   // const translation = -(percentage / 100) * maxTranslation;

//   // scrollSection.style.transform = `translate3d(${translation}px, 0, 0)`
//   scrollSection.style.transform = `translate3d(${-(percentage)}vw, 0, 0)`;
// }

function transform(section) {
  const offsetTop = section.parentElement.offsetTop;
  const scrollSection = section.querySelector('.example-list');
  
  let percentage = ((window.scrollY - offsetTop) / window.innerHeight) * 100;
  
  // Ensure the percentage is capped based on the scrollSection's width
  const maxScroll = scrollSection.offsetWidth;  // Maximum scroll value = scrollSection width in pixels
  
  // If percentage exceeds the scrollSection width, stop it
  percentage = percentage < 0 ? 0 : (percentage > maxScroll ? maxScroll : percentage);

  // Apply the transform based on the percentage
  scrollSection.style.transform = `translate3d(${-(percentage)}vw, 0, 0)`;
}


// Initial javaScript code
// let slideIndex = 1;
// showSlides(slideIndex);

// const { query } = require("express");

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
