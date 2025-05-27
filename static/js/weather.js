
const cityInput = document.getElementById("city-input");
const autocompleteList = document.getElementById("autocomplete-list");
const langSelect = document.getElementById("lang-select");
let autocompleteTimeout = null;

const historyKey = "weatherSearchHistory";

async function loadWeatherData(city) {
    const currentContainer = document.getElementById("weather-current");
    const historicalContainer = document.getElementById("weather-historical");
    const hourlyContainer = document.getElementById("weather-hourly");

    currentContainer.innerHTML = "Загрузка текущей погоды...";
    historicalContainer.innerHTML = "Загрузка прогноза...";
    hourlyContainer.innerHTML = "Загрузка почасового прогноза...";

    try {
        const forecastUrl = `/api/forecast?city=${encodeURIComponent(city.name)}&latitude=${city.latitude}&longitude=${city.longitude}`;
        const historicalUrl = `/api/historical?city=${encodeURIComponent(city.name)}&latitude=${city.latitude}&longitude=${city.longitude}`;
        const hourlyUrl = `/api/hourly/?city=${encodeURIComponent(city.name)}&latitude=${city.latitude}&longitude=${city.longitude}`;

        const [forecastResp, historicalResp, hourlyResp] = await Promise.all([
            fetch(forecastUrl),
            fetch(historicalUrl),
            fetch(hourlyUrl)
        ]);

        const forecast = await forecastResp.json();
        const historical = await historicalResp.json();
        const hourly = await hourlyResp.json();

        currentContainer.innerHTML = `
        <div class="card mt-3">
            <div class="card-body">
                <h5 class="card-title">Текущая погода в ${forecast.city}</h5>
                <p>Температура: ${forecast.temperature}°C</p>
                <p>Скорость ветра: ${forecast.windspeed} м/с</p>
                <p>Время: ${new Date(forecast.time).toLocaleString("ru-RU")}</p>
            </div>
        </div>
    `;

        const now = new Date();
        const oneHourAgo = new Date(now.getTime() - 60 * 60 * 1000);
        let hourlyHtml = `<h5 class='mt-4'>Почасовой прогноз (24 часа):</h5>`;
        hourlyHtml += `<table class='table table-sm table-bordered'><thead><tr><th>Время</th><th>Темп. °C</th><th>Осадки мм</th></tr></thead><tbody>`;

        let count = 0;
        for (let i = 0; i < hourly.time.length && count < 24; i++) {
            const time = new Date(hourly.time[i]);
            if (time > oneHourAgo) {
                hourlyHtml += `<tr>
                <td>${time.toLocaleString("ru-RU", {
                    hour: '2-digit',
                    minute: '2-digit',
                    day: '2-digit',
                    month: '2-digit'
                })}</td>
                <td>${hourly.temperature_2m[i]}</td>
                <td>${hourly.precipitation[i]}</td>
            </tr>`;
                count++;
            }
        }

        hourlyHtml += `</tbody></table>`;
        hourlyContainer.innerHTML = hourlyHtml;

        let historicalHtml = `
        <h5 class="mt-4">Прогноз по дням:</h5>
        <table class="table table-bordered">
            <thead><tr><th>Дата</th><th>Макс. температура</th><th>Мин. температура</th></tr></thead>
            <tbody>
    `;

        for (let i = 0; i < historical.time.length; i++) {
            historicalHtml += `
            <tr>
                <td>${historical.time[i]}</td>
                <td>${historical.temperature_2m_max[i]}°C</td>
                <td>${historical.temperature_2m_min[i]}°C</td>
            </tr>
        `;
        }

        historicalHtml += "</tbody></table>";
        historicalContainer.innerHTML = historicalHtml;

    } catch (error) {
        console.error("Ошибка при загрузке погоды:", error);
        currentContainer.innerHTML = "<div class='alert alert-danger'>Не удалось загрузить текущую погоду</div>";
        historicalContainer.innerHTML = "<div class='alert alert-danger'>Не удалось загрузить прогноз</div>";
        hourlyContainer.innerHTML = "<div class='alert alert-danger'>Не удалось загрузить почасовой прогноз</div>";
    }
}

cityInput.addEventListener("input", () => {
    const query = cityInput.value.trim();
    const lang = langSelect.value;
    if (query.length < 2) {
        autocompleteList.innerHTML = "";
        return;
    }
    if (autocompleteTimeout) clearTimeout(autocompleteTimeout);

    autocompleteTimeout = setTimeout(async () => {
        try {
            const res = await fetch(`/api/cities/?city=${encodeURIComponent(query)}&lang=${lang}`);
            const data = await res.json();
            autocompleteList.innerHTML = "";
            if (data.results) {
                data.results.forEach(city => {
                    const div = document.createElement("div");
                    div.classList.add("autocomplete-suggestion");
                    div.textContent = `${city.name}, ${city.country}`;
                    div.addEventListener("click", () => {
                        cityInput.value = city.name;
                        autocompleteList.innerHTML = "";
                        saveCityToHistory(city);
                        updateSearchHistoryUI();
                        loadWeatherData(city);
                    });
                    autocompleteList.appendChild(div);
                });
            }
        } catch (e) {
            console.error("Ошибка автодополнения:", e);
        }
    }, 300);
});


document.addEventListener("click", function (e) {
    if (!e.target.closest("#city-input") && !e.target.closest("#autocomplete-list")) {
        autocompleteList.innerHTML = "";
    }
});

function saveCityToHistory(city) {
    let history = JSON.parse(localStorage.getItem(historyKey)) || [];
    history = history.filter(c => c.id !== city.id);
    history.unshift(city);
    if (history.length > 5) history = history.slice(0, 5);
    localStorage.setItem(historyKey, JSON.stringify(history));
}

function updateSearchHistoryUI() {
    const historyList = document.getElementById("search-history");
    const history = JSON.parse(localStorage.getItem(historyKey)) || [];
    historyList.innerHTML = "";
    history.forEach(city => {
        const li = document.createElement("li");
        li.className = "list-group-item history-button";
        li.innerText = `${city.name}, ${city.country}`;
        li.addEventListener("click", () => loadWeatherData(city));
        historyList.appendChild(li);
    });
}

updateSearchHistoryUI();
