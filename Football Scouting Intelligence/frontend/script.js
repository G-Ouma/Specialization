const API_URL = "http://127.0.0.1:8000";
let currentPage = 0;
const pageSize = 10;
let currentFilters = {};

// Load players when the page opens
document.addEventListener("DOMContentLoaded", () => {
    loadPlayers();
});

async function loadPlayers() {
    currentPage = 0;
    currentFilters = {};
    await fetchPlayerPage();
}


// Display players in the table
function displayPlayers(players) {
    const tableBody = document.getElementById("players-table");

    tableBody.innerHTML = "";

    players.forEach(player => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>
                <a href="#" class="player-profile-link"
                data-player="${encodeURIComponent(player.name)}">
                    ${player.name}
                </a>
            </td>
            <td>${player.position || "Unknown"}</td>
            <td>${player.goals ?? 0}</td>
            <td>${player.assists ?? 0}</td>
            <td>${player.pass_accuracy ?? "N/A"}${player.pass_accuracy != null ? "%" : ""}</td>
        `;

        tableBody.appendChild(row);
    });
}


// Update dashboard statistics
async function updateDashboard() {
    try {
        const response = await fetch(`${API_URL}/dashboard`);

        if (!response.ok) {throw new Error("Could not retrieve dashboard statistics.");}

        const stats = await response.json();

        document.getElementById("total-players").textContent = stats.total_players;

        document.getElementById("top-goals").textContent = stats.top_goals;

        document.getElementById("total-positions").textContent = stats.total_positions;

    } catch (error) {console.error(error);}
}


// Search players
document.getElementById("search-button").addEventListener("click", searchPlayers);
document.getElementById("previous-page").addEventListener("click", () => {if (currentPage > 0) {currentPage--; fetchPlayerPage();}});

document.getElementById("next-page").addEventListener("click", () => {currentPage++; fetchPlayerPage(); });

async function searchPlayers() {
    currentPage = 0;

    currentFilters = {
        name: document.getElementById("player-name").value.trim(),
        position: document.getElementById("player-position").value
    };

    await fetchPlayerPage();
}


async function fetchPlayerPage() {
    const statusMessage = document.getElementById("status-message");
    const tableBody = document.getElementById("players-table");

    statusMessage.textContent = "Loading players...";
    tableBody.innerHTML = "";

    const params = new URLSearchParams({skip: currentPage * pageSize, limit: pageSize});

    Object.entries(currentFilters).forEach(([key, value]) => {if (value) {params.append(key, value);}});

    try {
        const response = await fetch(
            `${API_URL}/players?${params}`
        );

        if (!response.ok) {
            throw new Error("Could not retrieve players.");
        }

        
        const players = await response.json();

        const countResponse = await fetch(`${API_URL}/players/count?${params}`);

        if (!countResponse.ok) {throw new Error("Could not retrieve player count.");}

        const countData = await countResponse.json();
        const totalPlayers = countData.total;
        document.getElementById("search-summary").textContent = `${totalPlayers} player${totalPlayers === 1 ? "" : "s"} found.`;

        displayPlayers(players);
        updateDashboard();

        const firstPlayer = totalPlayers === 0
            ? 0
            : currentPage * pageSize + 1;

        const lastPlayer = currentPage * pageSize + players.length;

        statusMessage.textContent =`Showing ${firstPlayer}–${lastPlayer} of ${totalPlayers} players.`;

        document.getElementById("page-info").textContent = `Page ${currentPage + 1}`;

        document.getElementById("previous-page").disabled = currentPage === 0;

        document.getElementById("next-page").disabled = players.length < pageSize;

    } catch (error) {
        statusMessage.textContent = "Unable to retrieve players.";
        console.error(error);
    }
}


document.getElementById("compare-button").addEventListener("click", comparePlayers);

async function comparePlayers() {
    const player1 = document.getElementById("player-one").value.trim();
    const player2 = document.getElementById("player-two").value.trim();

    const resultsContainer = document.getElementById("comparison-results");

    if (!player1 || !player2) {
        resultsContainer.textContent = "Please enter both player names.";
        return;
    }

    resultsContainer.textContent = "Comparing players...";

    const params = new URLSearchParams({player1: player1, player2: player2});

    try {
        const response = await fetch(`${API_URL}/players/compare?${params}`);

        const data = await response.json();

        if (!response.ok) {throw new Error(data.detail || "Comparison failed.");}

        const metrics = [
            ["Position", "position"],
            ["Goals", "goals"],
            ["Assists", "assists"],
            ["Pass Accuracy (%)", "pass_accuracy"],
            ["Interceptions", "interceptions"],
            ["Tackles Won", "tackles_won"]
        ];

        let table = `
            <table>
                <thead>
                    <tr>
                        <th>Statistic</th>
                        <th>${data[0].name}</th>
                        <th>${data[1].name}</th>
                    </tr>
                </thead>
                <tbody>
        `;

        metrics.forEach(([label, field]) => {
            table += `
                <tr>
                    <td>${label}</td>
                    <td>${data[0][field] ?? "N/A"}</td>
                    <td>${data[1][field] ?? "N/A"}</td>
                </tr>
            `;
        });

        table += `
                </tbody>
            </table>
        `;

        resultsContainer.innerHTML = table;

    } catch (error) {
        resultsContainer.textContent = error.message;
        console.error(error);
    }
}


document.getElementById("leaderboard-button").addEventListener("click", loadLeaderboard);

async function loadLeaderboard() {
    const statistic = document.getElementById("leaderboard-statistic").value;
    const limit = document.getElementById("leaderboard-limit").value;

    const resultsContainer = document.getElementById("leaderboard-results");

    if (!limit || Number(limit) < 1) {
        resultsContainer.textContent = "Enter a valid player limit.";
        return;
    }

    resultsContainer.textContent = "Generating leaderboard...";

    const params = new URLSearchParams({statistic: statistic, limit: limit});

    try {
        const response = await fetch(`${API_URL}/players/leaderboard?${params}`);

        const data = await response.json();

        if (!response.ok) {throw new Error(data.detail || "Could not generate leaderboard.");}

        let table = `
            <table>
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Player</th>
                        <th>Position</th>
                        <th>${statistic.replaceAll("_", " ")}</th>
                    </tr>
                </thead>
                <tbody>
        `;

        data.forEach((player, index) => {
            table += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${player.name}</td>
                    <td>${player.position || "Unknown"}</td>
                    <td>${player.value ?? "N/A"}</td>
                </tr>
            `;
        });

        table += `
                </tbody>
            </table>
        `;

        resultsContainer.innerHTML = table;

    } catch (error) {
        resultsContainer.textContent = error.message;
        console.error(error);
    }
}


document.getElementById("players-table").addEventListener("click", async (event) => {const link = event.target.closest(".player-profile-link");

    if (!link) return;

    event.preventDefault();

    const playerName = decodeURIComponent(link.dataset.player);
    const profileSection = document.getElementById("player-profile");
    const profileContent = document.getElementById("profile-content");

    profileSection.style.display = "block";
    profileContent.textContent = "Loading player profile...";

    try {
        const response = await fetch(`${API_URL}/players/${encodeURIComponent(playerName)}/profile`);

        const data = await response.json();

        if (!response.ok) {throw new Error(data.detail || "Could not load player profile.");}

        renderPlayerProfile(data);

        profileSection.scrollIntoView({ behavior: "smooth" });

    } catch (error) {
        profileContent.textContent = error.message;
        console.error(error);
    }
});


function renderPlayerProfile(data) {const profileContent = document.getElementById("profile-content");

    profileContent.innerHTML = "";

    const heading = document.createElement("h3");
    heading.textContent = data.name;

    const details = document.createElement("div");
    details.className = "profile-overview";

    const fields = [
        ["Position", data.position],
        ["Team", data.team],
        ["Competition", data.competition],
        ["Season", data.season]
    ];

    fields.forEach(([label, value]) => {
        const item = document.createElement("p");
        item.textContent = `${label}: ${value || "N/A"}`;
        details.appendChild(item);
    });

    profileContent.appendChild(heading);
    profileContent.appendChild(details);

    const rankingSection = document.createElement("div");
    rankingSection.className = "profile-statistics";

    const rankingHeader = document.createElement("div");
    rankingHeader.className = "ranking-header";

    const rankingHeading = document.createElement("h3");
    rankingHeading.textContent = "Positional Rankings";

    const rankingSubtitle = document.createElement("span");
    rankingSubtitle.textContent = `Compared with ${data.positional_ranking.players_in_position} players in the same position.`;

    rankingHeader.appendChild(rankingHeading);
    rankingHeader.appendChild(rankingSubtitle);

    rankingSection.appendChild(rankingHeader);

    profileContent.appendChild(rankingSection);

    const ranking = data.positional_ranking;

    const rankingStats = [
        ["Goals", "goals_rank"],
        ["Assists", "assists_rank"],
        ["Passing Accuracy", "passing_accuracy_rank"],
        ["Tackles Won", "tackles_won_rank"],
        ["Interceptions", "interceptions_rank"],
        ["Chances Created", "chances_created_rank"],
        ["Dribbles", "dribbles_rank"],
        ["Aerial Duels Won", "aerial_duels_won_rank"]
    ];

    const rankingGrid = document.createElement("div");
    rankingGrid.className = "statistics-grid";

    rankingStats.forEach(([label, field]) => {
        const card = document.createElement("div");
        card.className = "stat-card";

        const value = ranking[field];

        card.innerHTML = `
            <span class="stat-label">${label}</span>
            <strong>${value ? `${value}${value === 1 ? "st" : value === 2 ? "nd" : value === 3 ? "rd" : "th"}` : "N/A"}</strong>
        `;

        rankingGrid.appendChild(card);
    });

    rankingSection.appendChild(rankingGrid);

    const attackingSection = document.createElement("div");
    attackingSection.className = "profile-statistics";

    const attackingHeading = document.createElement("h3");
    attackingHeading.textContent = "Attacking Performance";

    attackingSection.appendChild(attackingHeading);

    profileContent.appendChild(attackingSection);

    const attackingStats = [
        ["Goals", "goals"],
        ["Assists", "assists"],
        ["Shots", "shots"],
        ["Goals per 90", "goals_per_90"],
        ["Assists per 90", "assists_per_90"],
        ["Shots per 90", "shots_per_90"]
    ];

    const attackingGrid = document.createElement("div");
    attackingGrid.className = "statistics-grid";

    attackingStats.forEach(([label, field]) => {
        const card = document.createElement("div");
        card.className = "stat-card";

        const value = data.statistics[field];

        card.innerHTML = `
            <span class="stat-label">${label}</span>
            <strong>${value ?? "N/A"}</strong>
        `;

        attackingGrid.appendChild(card);
    });

    attackingSection.appendChild(attackingGrid);

    const passingSection = document.createElement("div");
    passingSection.className = "profile-statistics";

    const passingHeading = document.createElement("h3");
    passingHeading.textContent = "Passing & Creativity";

    passingSection.appendChild(passingHeading);

    profileContent.appendChild(passingSection);

    const passingStats = [
        ["Passes Completed", "passes_complete"],
        ["Incomplete Passes", "passes_incomplete"],
        ["Pass Accuracy (%)", "pass_accuracy"],
        ["Key Passes", "key_passes"],
        ["Chances Created", "chances_created"],
        ["Progressive Passes", "progressive_passes_complete"]
    ];

    const passingGrid = document.createElement("div");
    passingGrid.className = "statistics-grid";

    passingStats.forEach(([label, field]) => {
        const card = document.createElement("div");
        card.className = "stat-card";

        const value = data.statistics[field];

        card.innerHTML = `
            <span class="stat-label">${label}</span>
            <strong>${value ?? "N/A"}</strong>
        `;

        passingGrid.appendChild(card);
    });

    passingSection.appendChild(passingGrid);

    const defensiveSection = document.createElement("div");
    defensiveSection.className = "profile-statistics";

    const defensiveHeading = document.createElement("h3");
    defensiveHeading.textContent = "Defensive Performance";

    defensiveSection.appendChild(defensiveHeading);

    profileContent.appendChild(defensiveSection);

    const defensiveStats = [
        ["Tackles Won", "tackles_won"],
        ["Total Tackles", "total_tackles"],
        ["Interceptions", "interceptions"],
        ["Clearances", "clearances"],
        ["Blocks", "blocks"],
        ["Tackle Success Rate (%)", "tackle_success_rate"]
    ];

    const defensiveGrid = document.createElement("div");
    defensiveGrid.className = "statistics-grid";

    defensiveStats.forEach(([label, field]) => {
        const card = document.createElement("div");
        card.className = "stat-card";

        const value = data.statistics[field];

        card.innerHTML = `<span class="stat-label">${label}</span> <strong>${value ?? "N/A"}</strong>`;

        defensiveGrid.appendChild(card);
    });

    defensiveSection.appendChild(defensiveGrid);

    const playingTimeSection = document.createElement("div");
    playingTimeSection.className = "profile-statistics";

    const playingTimeHeading = document.createElement("h3");
    playingTimeHeading.textContent = "Playing Time & Appearances";

    playingTimeSection.appendChild(playingTimeHeading);

    profileContent.appendChild(playingTimeSection);

    const playingTimeStats = [
        ["Matches", "matches"],
        ["Minutes Played", "estimated_minutes"],
        ["Starts", "estimated_starts"],
        ["Substitute Appearances", "estimated_sub_apps"],
        ["90-Minute Equivalents", "estimated_90s"]
    ];

    const playingTimeGrid = document.createElement("div");
    playingTimeGrid.className = "statistics-grid";

    playingTimeStats.forEach(([label, field]) => {
        const card = document.createElement("div");
        card.className = "stat-card";

        const value = data.statistics[field];

        card.innerHTML = `
            <span class="stat-label">${label}</span>
            <strong>${value ?? "N/A"}</strong>
        `;

        playingTimeGrid.appendChild(card);
    });

    playingTimeSection.appendChild(playingTimeGrid);

    const progressionSection = document.createElement("div");
    progressionSection.className = "profile-statistics";

    const progressionHeading = document.createElement("h3");
    progressionHeading.textContent = "Ball Progression & Dribbling";

    progressionSection.appendChild(progressionHeading);

    profileContent.appendChild(progressionSection);

    const progressionStats = [
        ["Dribbles", "dribbles"],
        ["Box Carries", "box_carries"],
        ["Box Touches", "box_touches"],
        ["Progressive Passes", "progressive_passes_complete"],
        ["Incomplete Progressive Passes", "progressive_passes_incomplete"]
    ];

    const progressionGrid = document.createElement("div");
    progressionGrid.className = "statistics-grid";

    progressionStats.forEach(([label, field]) => {
        const card = document.createElement("div");
        card.className = "stat-card";

        const value = data.statistics[field];

        card.innerHTML = `<span class="stat-label">${label}</span> <strong>${value ?? "N/A"}</strong>`;

        progressionGrid.appendChild(card);
    });

    progressionSection.appendChild(progressionGrid);

    const aerialSection = document.createElement("div");
    aerialSection.className = "profile-statistics";

    const aerialHeading = document.createElement("h3");
    aerialHeading.textContent = "Crossing & Aerial Performance";

    aerialSection.appendChild(aerialHeading);

    profileContent.appendChild(aerialSection);

    const aerialStats = [
        ["Crosses Attempted", "crosses_attempted"],
        ["Crosses Completed", "crosses_complete"],
        ["Cross Accuracy (%)", "cross_accuracy"],
        ["Aerial Duels Won", "aerial_duels_won"],
        ["Total Aerial Duels", "aerial_duels_total"],
        ["Aerial Duel Success (%)", "aerial_duels_success_rate"]
    ];

    const aerialGrid = document.createElement("div");
    aerialGrid.className = "statistics-grid";

    aerialStats.forEach(([label, field]) => {
        const card = document.createElement("div");
        card.className = "stat-card";

        const value = data.statistics[field];

        card.innerHTML = `<span class="stat-label">${label}</span> <strong>${value ?? "N/A"}</strong>`;

        aerialGrid.appendChild(card);
    });

    aerialSection.appendChild(aerialGrid);

    const disciplineSection = document.createElement("div");
    disciplineSection.className = "profile-statistics";

    const disciplineHeading = document.createElement("h3");
    disciplineHeading.textContent = "Discipline & Match Conduct";

    disciplineSection.appendChild(disciplineHeading);

    profileContent.appendChild(disciplineSection);

    const disciplineStats = [
        ["Fouls Committed", "fouls_committed"],
        ["Yellow Cards", "yellow_cards"],
        ["Red Cards", "red_cards"]
    ];

    const disciplineGrid = document.createElement("div");
    disciplineGrid.className = "statistics-grid";

    disciplineStats.forEach(([label, field]) => {
        const card = document.createElement("div");
        card.className = "stat-card";

        const value = data.statistics[field];

        card.innerHTML = `<span class="stat-label">${label}</span> <strong>${value ?? "N/A"}</strong>`;

        disciplineGrid.appendChild(card);
    });

    disciplineSection.appendChild(disciplineGrid);
}

document.getElementById("close-profile").addEventListener("click", () => {document.getElementById("player-profile").style.display = "none";});