// Word count for the support-feedback box
let area = document.getElementById("comment"); 

let totalChar = document.getElementById("total-container"); 

let remChar = document.getElementById("remaining-container"); 

let configureButton = document.getElementById("configure-button"); 

let modal = document.getElementById("myModal"); 

let newLimitInput = document.getElementById("new-limit"); 

let maxLength = 245; 

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
			textLength >= maxLength && event.key !== "Backspace"
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