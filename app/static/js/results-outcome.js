main();

async function main() {
    const score = result.score;
    const explanation = result.explanation;

    const verdict = document.querySelector('.verdict');

    if (score <= 0) {
      verdict.innerHTML += `
        <p>This is not an AI-generateed image.</p>
      `;
    }
    if (score > 0) {
      verdict.innerHTML += `
        <p>This is an AI-generateed image.</p>
      `;
    }
}