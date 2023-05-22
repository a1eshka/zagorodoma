function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');
// Настройка AJAX
$(function () {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
});

const ratingButtons = document.querySelectorAll('.rating-buttons');

ratingButtons.forEach(button => {
    button.addEventListener('click', event => {
        // Получаем значение рейтинга из data-атрибута кнопки
        const value = parseInt(event.target.dataset.value)
        const companyId = parseInt(event.target.dataset.company)
        const ratingSum = button.querySelector('.rating-sum');
        // Создаем объект FormData для отправки данных на сервер
        const formData = new FormData();
        // Добавляем id статьи, значение кнопки
        formData.append('company_id', companyId);
        formData.append('value', value);
        // Отправляем AJAX-Запрос на сервер
        fetch("/companies/rating/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "X-Requested-With": "XMLHttpRequest",
            },
            body: formData
        }).then(response => response.json())
        .then(data => {
            // Обновляем значение на кнопке
            ratingSum.textContent = data.rating_sum;
        })
        .catch(error => console.error(error));
    });
});