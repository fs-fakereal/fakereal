// Word count for the support-feedback box
let area = 
	document.getElementById("textarea"); 
let totalChar = document.getElementById( 
	"total-container"
); 
let remChar = document.getElementById( 
	"remaining-container"
); 
let configureButton = 
	document.getElementById( 
		"configure-button"
	); 
let modal = 
	document.getElementById("myModal"); 
let closeButton = 
	document.getElementsByClassName( 
		"close"
	)[0]; 
let applyButton = 
	document.getElementById( 
		"apply-limit-button"
	); 
let newLimitInput = 
	document.getElementById( 
		"new-limit"
	); 
let maxLength = 50; 
updateCount(); 
area.addEventListener("input", () => { 
	updateCount(); 
}); 
area.addEventListener( 
	"keydown", 
	(event) => { 
		let textLength = 
			area.value.length; 
		if ( 
			textLength >= maxLength && 
			event.key !== "Backspace"
		) { 
			event.preventDefault(); 
			remChar.classList.add( 
				"limit-exceeded"
			); 
			alert( 
				"Character Limit Exceeded"
			); 
		} else { 
			remChar.classList.remove( 
				"limit-exceeded"
			); 
		} 
	} 
); 
configureButton.addEventListener( 
	"click", 
	() => { 
		newLimitInput.value = maxLength; 
		modal.style.display = "block"; 
	} 
); 
closeButton.addEventListener( 
	"click", 
	() => { 
		modal.style.display = "none"; 
	} 
); 
applyButton.addEventListener( 
	"click", 
	() => { 
		const newLimit = parseInt( 
			newLimitInput.value, 
			10 
		); 
		if (!isNaN(newLimit)) { 
			maxLength = newLimit; 
			modal.style.display = 
				"none"; 

			area.maxLength = maxLength; 
			updateCount(); 
		} 
	} 
); 
window.addEventListener( 
	"click", 
	(event) => { 
		if (event.target === modal) { 
			modal.style.display = 
				"none"; 
		} 
	} 
); 
function updateCount() { 
	let length = area.value.length; 
	totalChar.textContent = length; 
	remChar.textContent = 
		maxLength - length; 
} 