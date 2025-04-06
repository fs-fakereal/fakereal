// opening file: Team
document.getElementById('team-article').addEventListener('click', function() {
    const textBoxContainer = document.getElementById('team-picks');
    textBoxContainer.classList.remove('hidden');
    textBoxContainer.classList.add('open-file');
});

document.getElementById('close-btn-team').addEventListener('click', function() {
    const textBoxContainer = document.getElementById('team-picks');
    textBoxContainer.classList.add('hidden');
    textBoxContainer.classList.remove('open-file');
});

// opening file: Feb
document.getElementById('feb-article').addEventListener('click', function() {
    const textBoxContainer = document.getElementById('feb-picks');
    textBoxContainer.classList.remove('hidden');
    textBoxContainer.classList.add('open-file');
});

document.getElementById('close-btn1').addEventListener('click', function() {
    const textBoxContainer = document.getElementById('feb-picks');
    textBoxContainer.classList.add('hidden');
    textBoxContainer.classList.remove('open-file');
});
