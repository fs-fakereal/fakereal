// scroll
let animation = {
    revealDistance: 25,
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

// team scroll
const revealableTeamContainers = document.querySelectorAll('.revealable-team');

function teamReveal() {
    for (i=0; i<revealableTeamContainers.length; i++) {
        let windowHeight = window.innerHeight;
        let topOfRevealableContainer = revealableTeamContainers[i].getBoundingClientRect().top;

        if (topOfRevealableContainer < windowHeight - animation.revealDistance) {
            revealableTeamContainers[i].classList.add('active');
        } else {
            revealableTeamContainers[i].classList.remove('active');
        }
    }
}

window.addEventListener('scroll', teamReveal);
window.addEventListener('load', teamReveal);

// for scaling
const scaleContainers = document.querySelectorAll('.scale');

function scalable() {
    for (i=0; i<scaleContainers.length; i++) {
        let windowHeight = window.innerHeight;
        let topOfScaleContainer = scaleContainers[i].getBoundingClientRect().top;

        if (topOfScaleContainer < windowHeight - animation.revealDistance) {
            scaleContainers[i].classList.add('active');
        } else {
            scaleContainers[i].classList.remove('active');
        }
    }
}

window.addEventListener('scroll', scalable);
window.addEventListener('load', scalable);

// nav scale
const navScaleContainers = document.querySelectorAll('.nav-scale');

function navScale(index) {
    if (index < navScaleContainers.length) {
        navScaleContainers[index].style.opacity = 1;
        navScaleContainers[index].classList.add('active');

        setTimeout(() => {
            navScale(index + 1);
        }, 400); 
    }
    // for (i=0; i<navScaleContainers.length; i++) {
    //     let windowHeight = window.innerHeight;
    //     let topOfScaleContainer = navScaleContainers[i].getBoundingClientRect().top;

    //     if (topOfScaleContainer < windowHeight - animation.revealDistance) {
    //         navScaleContainers[i].classList.add('active');
    //     } else {
    //         navScaleContainers[i].classList.remove('active');
    //     }
    // }
}

// navScale(0);
// window.addEventListener('scroll', navScale(0));
window.addEventListener('load', navScale(0));

// examples scale
const exampleScaleContainers = document.querySelectorAll('.ex-scale');

function exScale() {
    for (i=0; i<exampleScaleContainers.length; i++) {
        let windowHeight = window.innerHeight;
        let topOfScaleContainer = exampleScaleContainers[i].getBoundingClientRect().top;

        if (topOfScaleContainer < windowHeight - animation.revealDistance) {
            exampleScaleContainers[i].classList.add('active');
        } else {
            exampleScaleContainers[i].classList.remove('active');
        }
    }
}

window.addEventListener('scroll', exScale);
window.addEventListener('load', exScale);