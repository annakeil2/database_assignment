// Countdown timer
const timer = document.getElementById("timer");

// We update the message every 15 minutes on the 15th minute
// Make the counter count down to the next 15th minute
if (timer) {
    const now = new Date();
    const now_min = now.getMinutes();
    const nearest_15 = getNext15Min(now_min);

    let seconds = ((nearest_15 - now_min) * 60) + (60 - now.getSeconds());
    setInterval(() => {
        seconds--;

        let min = Math.floor(seconds / 60);
        let sec = seconds % 60;

        timer.innerText = `Next bottle in: ${min}:${sec < 10 ? '0' : ''}${sec}`;

        if (seconds <= 0) seconds = 900;

    }, 1000);
}

function getNext15Min(nowMinutes) {
    if (nowMinutes < 15) {
        return 15;
    }
    if (nowMinutes < 30) {
        return 30;
    }
    if (nowMinutes < 45) {
        return 45;
    }
    return 60;
}