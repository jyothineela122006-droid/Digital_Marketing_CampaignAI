const form = document.getElementById("predictionForm");
const result = document.getElementById("result");

form.addEventListener("submit", async function(event) {
    event.preventDefault();

    const data = {};

    const numericFields = [
        "Age", "Income", "AdSpend",
        "ClickThroughRate", "ConversionRate",
        "WebsiteVisits", "PagesPerVisit",
        "TimeOnSite", "SocialShares",
        "EmailOpens", "EmailClicks",
        "PreviousPurchases", "LoyaltyPoints"
    ];

    numericFields.forEach(field => {
        data[field] = Number(document.getElementById(field).value);
    });

    data.Gender = document.getElementById("Gender").value;
    data.CampaignChannel = document.getElementById("CampaignChannel").value;
    data.CampaignType = document.getElementById("CampaignType").value;

    result.textContent = "Analyzing your campaign...";

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const output = await response.json();

        if (!response.ok) {
            throw new Error(output.error || "Prediction failed");
        }

        result.innerHTML = `
            <h2>${output.message}</h2>
            <h3>AI Prediction: ${output.prediction}</h3>
            <h3>Conversion Probability: ${output.probability}%</h3>

            <div class="progress-container">
                <div class="progress-bar"
                     style="width: ${output.probability}%">
                </div>
            </div>

            <p>Campaign analysis completed successfully!</p>
        `;

    } catch (error) {
        result.textContent = "Error: " + error.message;
    }
});

// AUTOMATIC ACTIVE SIDEBAR MENU

const menuLinks = document.querySelectorAll(".sidebar-nav a");

function updateActiveMenu() {
    const currentPage = window.location.hash || "#home";

    menuLinks.forEach(link => {
        link.classList.toggle(
            "active",
            link.getAttribute("href") === currentPage
        );
    });
}

menuLinks.forEach(link => {
    link.addEventListener("click", updateActiveMenu);
});

window.addEventListener("hashchange", updateActiveMenu);

updateActiveMenu();
