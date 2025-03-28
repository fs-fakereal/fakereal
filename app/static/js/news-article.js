main();

async function main() {
  const articles = await getData();
  const articlesUl = document.querySelector('#article');

  // Display only the first 10 articles by default
  // const visibleArticles = articles.slice(0, 10);
  const visibleArticles = articles;

  // Loop through the visible articles and add them to the DOM
  visibleArticles.forEach(article => {
    articlesUl.innerHTML += 
    `
      <div class='article-info'>
        <img src="${article.urlToImage ? article.urlToImage : '/static/imgs/FakeReal.png'}" alt="article-img">

        <div class='content'>
          <div class='source'>
            <h3>${article.title}</h3>

            <div class='author-release'>
              <p>${article.author ? article.author.split(',').slice(0, 2).join(',') : "Anonymous"}</p>
              <p>${article.publishedAt}</p>
            </div>

            <h4>${article.description}</h4>
          </div>
          <br>
          <div class='article-button'>
            <a href='${article.url}'>
              <button>Read article</button>
            </a>
          </div>
        </div>
      </div>
    `;
  });

  // // If there are more than 10 articles, add a "Show More" button
  // if (articles.length > 10) {
  //   articlesUl.innerHTML += `
  //     <button id="show-more">Show More</button>
  //   `;

  //   // Show the remaining articles when the button is clicked
  //   const showMoreButton = document.querySelector('#show-more');
  //   showMoreButton.addEventListener('click', () => {
      
  //     // Hide the "Show More" button after showing all articles
  //     showMoreButton.style.display = 'none';
      
  //     // Display the rest of the articles
  //     const hiddenArticles = articles.slice(10);
  //     hiddenArticles.forEach(article => {
  //       articlesUl.innerHTML += 
  //       `
  //         <div class='article-info'>
  //           <img src="${article.urlToImage ? article.urlToImage : '/static/imgs/FakeReal.png'}" alt="article-img">

  //           <div class='content'>
  //             <h3>${article.title}</h3>

  //             <div class='author-release'>
  //               <p>${article.author ? article.author.split(',').slice(0, 2).join(', ') : "Anonymous"}</p>
  //               <p>${article.publishedAt}</p>
  //             </div>

  //             <h4>${article.description}</h4>
        
  //             <br>
  //             <div  class='article-button'>
  //               <a href='${article.url}'>
  //                 <button>Read article</button>
  //               </a>
  //             </div>
  //           </div>
  //         </div>
  //       `;
  //     });

  //     // Hide the "Show More" button after showing all articles
  //     showMoreButton.style.display = 'none';
  //   });
  // }
}

async function getData() {
  const respo = await fetch("../static/json/news.json");
  const data = await respo.json();

  return data;
}

// to open and close the articles
// function openPopup() {
//   document.querySelector(".hidden").style.display = 'block';
//   document.body.classList.add('no-scroll');
// }

// function closePopup() {
//   document.querySelector(".hidden").style.display = 'none';
//   document.body.classList.remove('no-scroll');
// } 