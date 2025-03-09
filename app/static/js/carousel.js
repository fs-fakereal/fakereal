// let slideIndex = 1;
// showSlides(slideIndex);

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

// Select the necessary elements
const wrapper = document.querySelector('.example-list-wrapper');
const exampleList = document.querySelector('.example-list');
const articles = document.querySelector('.articles');
const footer = document.querySelector('.footer');

// Get the width of an individual item and the wrapper
const itemWidth = 220; // Including margin (200px + 2 * 10px)
const maxScroll = document.body.scrollHeight - window.innerHeight;

// Listen for the scroll event
window.addEventListener('scroll', () => {
  const scrollPosition = window.scrollY;

  // Calculate the scroll percentage
  const scrollPercentage = scrollPosition / maxScroll;

  // Get the total scroll width of the list
  const scrollWidth = exampleList.scrollWidth - wrapper.offsetWidth;

  // Calculate the translateX value based on scroll percentage
  const translateX = scrollPercentage * scrollWidth;

  // Apply the horizontal translation
  exampleList.style.transform = `translate3d(${translateX}%, 0, 0)`;

  // Check if the list has scrolled to the end
  if (scrollPercentage >= 1) {
    // Show the articles and footer once scrolled to the end
    articles.style.display = 'block';
    footer.style.display = 'block';
  } else {
    // Hide the articles and footer while scrolling
    articles.style.display = 'none';
    footer.style.display = 'none';
  }
});