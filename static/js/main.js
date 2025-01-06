/* Countdown */
let weddingDate = luxon.DateTime.fromISO("2025-05-31T16:00:00");

let countdownElementDays = document.getElementById("countdown-days");
let countdownElementHours = document.getElementById("countdown-hours");
let countdownElementMinutes = document.getElementById("countdown-minutes");

function updateCountdown() {
    const now = luxon.DateTime.now();
    const diff = weddingDate.diff(now, ['days', 'hours', 'minutes', 'seconds']).toObject();

    if (diff.days > 0 || diff.hours > 0 || diff.minutes > 0 || diff.seconds > 0) {
        countdownElementDays.innerText = `${Math.floor(diff.days)} дней`;
        countdownElementHours.innerText = `${Math.floor(diff.hours)} часов`;
        countdownElementMinutes.innerText = `${Math.floor(diff.minutes)} минут`;
    } else {
        countdownElement.innerText = "Свадьба началась! 🎉";
    }
}

setInterval(updateCountdown, 1000);
updateCountdown();


/* Map */
let modalElement = document.getElementById("modal");

let rspv_title = document.getElementById("rspv-open-button");
let closeDialogButton = document.getElementById("close-dialog-button");

rspv_title.addEventListener('click', OpenRSPV);
closeDialogButton.addEventListener('click', CloseRSPV);

function OpenRSPV() {
    modalElement.showModal();
}
function CloseRSPV() {
    modalElement.close();
}

let place_name = document.getElementById("place-name");
let map = document.getElementById("google-map");

place_name.addEventListener('click', OpenMap);

function OpenMap() {
    if (map.style.display === 'unset') {
        map.style.display = 'none';
    }
    else {
        map.style.display = 'unset';
    }
}
