// scroll
let animation = {
    revealDistance: 150,
    initialOpacity: 0,
    transitionDelay: 0,
    transitionDuration: '2s',
    transitionProperty: 'all',
    transitionTimingFunction: 'ease'
};

const revealableContainers = document.querySelectorAll('.revealable');

function reveal() {
    for (i=0; i<revealableContainers.length; i++) {
        let windowHeight = window.innerHeight;
        let topOfRevealableContainer = revealableContainers[i].getBoundingClientRect().top;

        if (topOfRevealableContainer < windowHeight - animation.revealDistance) {
            revealableContainers[i].classList.add('active');
        } else {
            revealableContainers[i].classList.remove('active');
        }
    }
}

window.addEventListener('scroll', reveal);
window.addEventListener('load', reveal);