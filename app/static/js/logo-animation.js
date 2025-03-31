const anchor = document.getElementById('eyes')
const rekt = anchor.getBoundingClientRect();
const anchorX = rekt.left + rekt.width / 2;
const anchorY = rekt.top + rekt.height / 2;
const eyes = document.querySelectorAll('.pupil')

document.addEventListener('mousemove', (e) => {
    console.log(e)

    const mouseX = e.clientX;
    const mouseY = e.clientY;

    const angleDeg = angle(mouseX, mouseY, anchorX, anchorY);

    console.log(angleDeg)

    eyes.forEach(eye => {
        eye.style.transform = `rotate(${25 + angleDeg}deg)`;

    //     if (angleDeg >= -180 && angleDeg <= 20) {
    //         eye.style.transform += ' translateX(0.4rem) translateY(-0.8rem)';
    //     }   
    //     else if  (angleDeg >= 100 && angleDeg <= 180) {
    //         eye.style.transform += ' translateX(0.7rem) translateY(-0.6rem)';
    //     }  
    //     else if  (angleDeg >= 21 && angleDeg <= 99) {
    //         eye.style.transform += ' translateX(0.7rem) translateY(-0.6rem)';
    //     } 
    })
})

function angle(cx, cy, ex, ey) {
    const dy = ey - cy;
    const dx = ex - cx;
    const rad = Math.atan2(dy, dx); //range (-pi, pi)
    const deg = rad * 180 / Math.PI;
    return deg;
}