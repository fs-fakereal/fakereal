var input = document.querySelector('input[type="file"]');
var data = new FormData(); 

data.append('file', input.files[0])

const response = await fetch('/upload', {
  method: 'POST',
  body: data
})

console.log(response.status);
