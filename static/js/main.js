const countdownElement = document.getElementById("countdown");
const weddingDate = luxon.DateTime.fromISO("2025-05-31T16:00:00");

function updateCountdown() {
    const now = luxon.DateTime.now();
    const diff = weddingDate.diff(now, ['days', 'hours', 'minutes', 'seconds']).toObject();

    if (diff.days > 0 || diff.hours > 0 || diff.minutes > 0 || diff.seconds > 0) {
        countdownElement.innerText = `До свадьбы осталось: ${Math.floor(diff.days)} дней, ${Math.floor(diff.hours)} часов, ${Math.floor(diff.minutes)} минут.`;
    } else {
        countdownElement.innerText = "Свадьба началась! 🎉";
    }
}

setInterval(updateCountdown, 1000);
updateCountdown();