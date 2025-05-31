/* Countdown */
let weddingDate = luxon.DateTime.fromISO("2025-05-31T16:00:00");

let countdownElementDays = document.getElementById("countdown-days");
let countdownElementHours = document.getElementById("countdown-hours");
let countdownElementMinutes = document.getElementById("countdown-minutes");

function updateCountdown() {
    const now = luxon.DateTime.now();
    const diff = weddingDate.diff(now, ['days', 'hours', 'minutes', 'seconds']).toObject();

    if (diff.days > 0 || diff.hours > 0 || diff.minutes > 0 || diff.seconds > 0) {
        countdownElementDays.innerText = `${Math.floor(diff.days)}`;
        countdownElementHours.innerText = `${Math.floor(diff.hours)}`;
        countdownElementMinutes.innerText = `${Math.floor(diff.minutes)}`;
    } else {
        /* countdownElement.innerText = "Свадьба началась! 🎉"; */
    }
}

setInterval(updateCountdown, 1000);
updateCountdown();


/* Modal window */
let modalElement = document.getElementById("modal");
let rspv_title = document.getElementById("rspv-open-button");

rspv_title.addEventListener('click', OpenRSPV);

function OpenRSPV() {
    modalElement.showModal();
}

document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("modal");
    const closeButton = document.getElementById("close-dialog-button");
    const submitButton = document.getElementById("submit-dialog-button");

    // Закрытие модального окна
    closeButton.addEventListener("click", function () {
        modal.close();
    });

    // Обработка отправки формы
    submitButton.addEventListener("click", function (event) {
        event.preventDefault(); // Предотвращение стандартного поведения формы

        // Получение данных формы
        const name = modal.querySelector("input[name='name']").value;
        const guests = modal.querySelector("input[name='guests']").value;

        // Сбор значений чекбоксов
        const alcoholCheckboxes = modal.querySelectorAll("input[name='alcohol']:checked");
        const alcoholPreferences = Array.from(alcoholCheckboxes).map(checkbox => checkbox.value);

        // Проверка обязательных полей
        if (!name || !guests) {
            alert("Пожалуйста, заполните обязательные поля!");
            return;
        }

        // Данные для отправки
        const formData = {
            name: name,
            guests: guests,
            alcohol: alcoholPreferences,
        };

        // Отправка данных на сервер
        fetch("/submit-form", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(formData),
        })
        .then(response => {
            if (response.ok) {
                modal.close();
            } else {
                return response.json().then(data => {
                    alert(`Ошибка: ${data.message}`);
                });
            }
        })
        .catch(error => {
            console.error("Ошибка при отправке данных:", error);
            alert("Не удалось отправить данные. Попробуйте снова.");
        });
    });
});

/* Map */
let place_name = document.getElementById("place-name");
let map = document.getElementById("google-map");
place_name.addEventListener('click', toggleMap);

function toggleMap() {
    map.classList.toggle('visible');
}

document.addEventListener('scroll', function() {
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        const rect = section.getBoundingClientRect();
        if (rect.top < window.innerHeight && rect.bottom >= 0) {
            section.classList.add('visible');
        }
    });
});
