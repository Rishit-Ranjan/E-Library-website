const quoteContent = document.getElementById('quote-content');
const quoteAuthor = document.getElementById('quote-author');

    fetch('https://api.quotable.io/random')
      .then(response => response.json())
      .then(data => {
        quoteContent.textContent = `" ${data.content}"`;
        quoteAuthor.textContent = `- ${data.author}`;
      })
      .catch(error => console.error(error));
    