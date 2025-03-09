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

const wrapper = document.querySelector('.example-list-wrapper'); // Wrapper of the list
const exampleList = document.querySelector('.example-list'); // The list itself
const articles = document.querySelector('.articles');
const footer = document.querySelector('.footer');

// Get the width of an individual item and the wrapper
const itemWidth = 220; // Including margin (200px + 2 * 10px)
const maxScroll = document.body.scrollHeight - window.innerHeight; // Maximum scrollable height

let isSectionInView = false; // Flag to track if the section is in the viewport

// Create an IntersectionObserver to detect when the wrapper enters the viewport
const observer = new IntersectionObserver((entries, observer) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      isSectionInView = true; // The section has entered the viewport
    } else {
      isSectionInView = false; // The section has exited the viewport
    }
  });
}, {
  threshold: 0.5 // Trigger when 50% of the section is in view
});

// Observe the wrapper section
observer.observe(wrapper);

// Listen for the scroll event, but only act when the section is in view
window.addEventListener('scroll', () => {
  if (!isSectionInView) {
    return; // Do nothing if the section isn't in view
  }

  const scrollPosition = window.scrollY;

  // Calculate the scroll percentage
  const scrollPercentage = scrollPosition / maxScroll;

  // Get the total scroll width of the list
  const scrollWidth = exampleList.scrollWidth - wrapper.offsetWidth;

  // Calculate the translateX value based on scroll percentage
  const translateX = scrollPercentage * scrollWidth;

  // Apply the horizontal translation using pixels (not percentage)
  exampleList.style.transform = `translate3d(-${translateX}px, 0, 0)`; // Moving leftwards

  // Check if the list has scrolled to the end
  // if (scrollPercentage >= 1) {
  //   // Show the articles and footer once scrolled to the end
  //   articles.style.display = 'block';
  //   footer.style.display = 'block';
  // } else {
  //   // Hide the articles and footer while scrolling
  //   articles.style.display = 'none';
  //   footer.style.display = 'none';
  // }
});
