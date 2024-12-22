function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const questionCards = document.getElementsByClassName('card');
const answerCards = document.getElementsByClassName('answer-card');
likeBtnOnClick(questionCards, '/question/');
likeBtnOnClick(answerCards, '/answer/');
checkboxOnClick(answerCards);


function checkboxOnClick(cards) {
    for (const card of cards) {
        const checkbox = card.querySelector('.correct-checkbox');
        const objectId = card.dataset.objectId;
        const questionId = card.dataset.questionId;

        if (checkbox) {
            checkbox.addEventListener('change', () => {
                const request = new Request(`/answer/${objectId}/correct`, {
                    method: "POST",
                    headers: {'X-CSRFToken': getCookie('csrftoken')},
                    mode: 'same-origin',
                    body: JSON.stringify({ question_id: `${questionId}` }),
                });

                fetch(request).then((response) => {
                    response.json().then((data) => {
                        if (data.message)
                            alert(data.message);
                        console.log(data.is_correct)
                        checkbox.checked = data.is_correct;
                    });
                });
            });
        }
    }
}

function likeBtnOnClick(cards, urlPrefix) {
    for (const card of cards) {
        const likeBtn = card.querySelector('.like-btn');
        const dislikeBtn = card.querySelector('.dislike-btn');
        const likeCounter = card.querySelector('.like-counter');
        const objectId = card.dataset.objectId;

        if (likeBtn && dislikeBtn) {
            const toggleButtons = (clickedBtn, oppositeBtn) => {
                if (!oppositeBtn.classList.contains('disabled'))
                    clickedBtn.classList.add('disabled');
                oppositeBtn.classList.remove('disabled');
            };

            likeBtn.addEventListener('click', () => {
                if (likeBtn.classList.contains('disabled'))
                    return;

                const request = new Request(urlPrefix + `${objectId}/like`, {
                    method: "POST",
                    headers: {'X-CSRFToken': getCookie('csrftoken')},
                    mode: 'same-origin',
                    body: JSON.stringify({ type: 'like' }),
                });

                fetch(request).then((response) => {
                    response.json().then((data) => {
                        likeCounter.innerHTML = data.rating;
                        toggleButtons(likeBtn, dislikeBtn);
                    });
                });
            });

            dislikeBtn.addEventListener('click', () => {
                if (dislikeBtn.classList.contains('disabled'))
                    return;

                const request = new Request(urlPrefix + `${objectId}/like`, {
                    method: "POST",
                    headers: {'X-CSRFToken': getCookie('csrftoken')},
                    mode: 'same-origin',
                    body: JSON.stringify({ type: 'dislike' }),
                });

                fetch(request).then((response) => {
                    response.json().then((data) => {
                        likeCounter.innerHTML = data.rating;
                        toggleButtons(dislikeBtn, likeBtn);
                    });
                });
            });
        }
    }
}
