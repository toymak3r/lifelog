/**
 * Fetches data from a web service and dynamically creates a grid of podcast images with their titles.
 * Implements lazy loading for the images using the IntersectionObserver API.
 */
function load_covers() {
    // Fetch data from the web service
    fetch('http://localhost:5000/podcasts', {
        headers: new Headers({
            'Accept': 'application/json; charset=utf-8'
        })
    })
        .then(response => response.json())
        .then(data => {
            const gridContainer = document.getElementById('podcasts');

            data.forEach(podcast => {
                const cardContainer = createCardContainer(decodeURIComponent(podcast.url));
                const imageContainer = createImageContainer();
                const imageContainerBody = createImageContainerBody();
                const podcastDeleteBtn = createBtn('del', podcast.url);
                const title = createTitle(podcast.title);
                const img = createImage(podcast.imageUrl, podcast.title);

                img.addEventListener('load', function () {
                    appendElements(imageContainer, img, imageContainerBody, title, podcastDeleteBtn);
                    appendElements(cardContainer, imageContainer);
                    appendElements(gridContainer, cardContainer);
                });

                img.addEventListener('error', function () {
                    img.src = '../assets/imgs/podcasts/not_found.jpg';
                    appendElements(imageContainer, img, imageContainerBody, title, podcastDeleteBtn);
                    appendElements(imageContainerBody, imageContainer);
                    appendElements(gridContainer, cardContainer);
                });
            });

            // Lazy load images with IntersectionObserver
            const observer = new IntersectionObserver(entries => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target.querySelector('img');
                        img.src = img.dataset.src;
                        observer.unobserve(entry.target);
                    }
                });
            }, { rootMargin: '0px 0px 100px 0px' });

            document.querySelectorAll('.image-container img').forEach(img => {
                observer.observe(img.parentElement);
            });
        })
        .catch(error => console.error('Error fetching data from web service:', error));
}

/**
 * Creates a card container element.
 * @param {string} id - The text to be used as id.
 * @returns {HTMLDivElement} The created card container element.
 */
function createCardContainer(id) {
    const cardContainer = document.createElement('div');
    cardContainer.id = encodeURI(id);
    cardContainer.classList.add('col-auto', 'mb3', 'cardContainer');
    return cardContainer;
}

/**
 * Creates an image container element.
 * @returns {HTMLDivElement} The created image container element.
 */
function createImageContainer() {
    const imageContainer = document.createElement('div');
    imageContainer.classList.add('card', 'imageContainer', 'text-white', 'bg-dark');
    return imageContainer;
}

/**
 * Creates an image container body element.
 * @returns {HTMLDivElement} The created image container body element.
 */
function createImageContainerBody() {
    const imageContainerBody = document.createElement('div');
    imageContainerBody.classList.add('card-body');
    return imageContainerBody;
}

/**
 * Creates a title element with the given text content.
 * @param {string} text - The text content of the title.
 * @returns {HTMLHeadingElement} The created title element.
 */
function createTitle(text) {
    const title = document.createElement('h8');
    title.classList.add('card-title');
    title.textContent = text;
    return title;
}

/**
 * Creates an image element with the given source and alternate text.
 * @param {string} src - The source of the image.
 * @param {string} alt - The alternate text of the image.
 * @returns {HTMLImageElement} The created image element.
 */
function createImage(src, alt) {
    const img = document.createElement('img');
    img.classList.add('card-img-top');
    img.src = src;
    img.alt = alt;
    img.dataset.src = src; // for lazy loading
    return img;
}


function createBtn(type, id, url) {
    const btn = document.createElement('a');
    btn.classList.add('btn', 'card-link');

    if (type == 'del') {
        btn.classList.add('btn-danger');
        btn.innerHTML = "Delete";
        btn.onclick = function() { deletePodcast(id) };
    };

    if (type == 'edit') {
        btn.classList.add('btn-warning');
        btn.innerHTML = "Delete"

    };

    return btn;
}

/**
 * Appends multiple elements to a parent element.
 * @param {HTMLElement} parent - The parent element to append the elements to.
 * @param {...HTMLElement} elements - The elements to append.
 */
function appendElements(parent, ...elements) {
    elements.forEach(element => {
        parent.appendChild(element);
    });
}

/**
 * Deleting Podcast from Playlist
 * @param {id} id - The id used on playlist (usually url)
 */
function deletePodcast(id) {
    const url = 'http://localhost:5000/podcasts/delete?podcast_id='+encodeURI(id);
    const requestOptions = {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Charset': 'utf-8',
        }
    };

    fetch(url, requestOptions)
        .then(response => {
            if (response.ok) {
                // The DELETE request was successful (status code 2xx)
                console.log('DELETE request successful');
                const object = document.getElementById(id);
                object.remove();
            } else {
                // The DELETE request failed (status code not in the 2xx range)
                console.error(`DELETE request failed with status ${response.status}`);
            }
        })
        .catch(error => {
            // An error occurred during the fetch
            console.error('Error during DELETE request:', error);
        });
    return false;
}

function addPodcast()
{
    modal = document.getElementById("addPodcast");
    modal.style.display = "block";
}
/**
 * Add Podcast from Rss To Playlist (OPML)
 * @param {rss} rss - The id used on playlist (usually url)
 */
function addPodcastByRss(rss) {
    const url = 'http://localhost:5000/podcasts/add?podcast_rss='+encodeURI(rss);
    const requestOptions = {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Charset': 'utf-8',
        }
    };

    fetch(url, requestOptions)
        .then(response => {
            if (response.ok) {
                // The PUT request was successful (status code 2xx)
                console.log('PUT request successful');
                modal = document.getElementById("addPodcast");
                modal.style.display = "none";
                loadhtml('podcasts/_body.html', 'content');
                load_covers();                
                // reload list
            } else {
                // The PUT request failed (status code not in the 2xx range)
                console.error(`PUT request failed with status ${response.status}`);
            }
        })
        .catch(error => {
            // An error occurred during the fetch
            console.error('Error during PUR request:', error);
        });
    return false;
}

window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  } 