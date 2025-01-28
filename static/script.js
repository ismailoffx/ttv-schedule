document.addEventListener("DOMContentLoaded", function() {
    // Real vaqtni yangilash
    function updateCurrentTime() {
        const now = new Date().toLocaleString("en-US", { timeZone: "Asia/Tashkent" });
        document.getElementById("current-time").textContent = now;

        // Hozirgi ko'rsatuvni va vaqtini yangilash
        const timeLeftElem = document.getElementById("time-left");
        if (timeLeftElem) {
            let timeLeft = timeLeftElem.textContent.split(":");
            let hours = parseInt(timeLeft[0]);
            let minutes = parseInt(timeLeft[1]);
            let seconds = parseInt(timeLeft[2]);

            if (seconds > 0) {
                seconds--;
            } else {
                if (minutes > 0) {
                    minutes--;
                    seconds = 59;
                } else if (hours > 0) {
                    hours--;
                    minutes = 59;
                    seconds = 59;
                }
            }

            // Yangi vaqtni ko'rsatish
            timeLeftElem.textContent = `${hours}:${minutes}:${seconds}`;
        }
    }

    setInterval(updateCurrentTime, 1000); // Soatni har soniyada yangilash

    // Bugungi jadvalni ko'rsatish va yashirish
    const fullScheduleButton = document.getElementById('full-schedule-button');
    const fullSchedule = document.getElementById('full-schedule');

    fullScheduleButton.addEventListener('click', function() {
        if (fullSchedule.style.display === "none" || fullSchedule.style.display === "") {
            fullSchedule.style.display = "block";
        } else {
            fullSchedule.style.display = "none";
        }
    });
});
