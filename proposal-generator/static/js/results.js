/**
 * Results page — fetch scored results and render tier recommendation.
 */

(function () {
    "use strict";

    var loadingEl = document.getElementById("loading");
    var resultsEl = document.getElementById("results");
    var path = window.location.pathname;
    var sessionId = path.split("/").pop();

    var tierData = {};

    // Load tiers and results in parallel
    Promise.all([
        fetch("/api/tiers").then(function (r) { return r.json(); }),
        fetch("/api/results/" + sessionId).then(function (r) { return r.json(); }),
    ])
        .then(function (values) {
            tierData = values[0];
            var data = values[1];

            if (data.error) {
                loadingEl.innerHTML = '<p>Session not found.</p>';
                return;
            }

            loadingEl.style.display = "none";
            resultsEl.style.display = "block";
            renderResults(data);
        })
        .catch(function (err) {
            loadingEl.innerHTML = '<p>Failed to load results.</p>';
            console.error(err);
        });

    function renderResults(data) {
        var scores = data.scores;
        var tierKey = scores.recommended_tier.toLowerCase().replace(/ /g, "_");
        var tier = tierData[tierKey] || {};
        var dims = scores.dimensions || {};
        var maxScore = 12; // approximate max per dimension for bar scaling

        var html = "";

        // Tier recommendation card
        html += '<div class="tier-card">';
        html += '<h2>Recommended: ' + escHtml(scores.recommended_tier) + '</h2>';
        html += '<p class="tier-tagline">' + escHtml(tier.tagline || "") + '</p>';
        html += '<p class="tier-summary">' + escHtml(tier.summary || "") + '</p>';
        html += '</div>';

        // Score breakdown
        html += '<div class="score-breakdown">';
        html += '<h3>Assessment Breakdown</h3>';
        for (var dim in dims) {
            var score = dims[dim];
            var pct = Math.min((score / maxScore) * 100, 100);
            var name = dim.replace(/_/g, " ");
            html += '<div class="dimension">';
            html += '<span class="dimension-name">' + escHtml(name) + '</span>';
            html += '<div class="dimension-bar-container">';
            html += '<div class="dimension-bar" style="width:' + pct + '%"></div>';
            html += '</div>';
            html += '<span class="dimension-score">' + score + '</span>';
            html += '</div>';
        }
        html += '<div class="dimension" style="border-top:2px solid #e2e8f0;margin-top:8px;padding-top:12px;">';
        html += '<span class="dimension-name" style="font-weight:700;">Total</span>';
        html += '<div class="dimension-bar-container"></div>';
        html += '<span class="dimension-score" style="font-size:16px;">' + scores.total_score + '</span>';
        html += '</div>';
        html += '</div>';

        // Reasoning
        html += '<div class="reasoning">';
        html += '<h3>Why This Recommendation</h3>';
        var reasoningHtml = (scores.reasoning || "").replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        reasoningHtml = reasoningHtml.replace(/^- (.*)$/gm, '<li>$1</li>');
        if (reasoningHtml.indexOf('<li>') >= 0) {
            reasoningHtml = reasoningHtml.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
        }
        reasoningHtml = reasoningHtml.replace(/\n\n/g, '</p><p>').replace(/\n/g, '<br>');
        html += '<p>' + reasoningHtml + '</p>';
        html += '</div>';

        // Deliverables
        if (tier.included) {
            html += '<div class="deliverables">';
            html += '<h3>What You Get</h3>';
            html += '<ul>';
            for (var i = 0; i < tier.included.length; i++) {
                html += '<li>' + escHtml(tier.included[i]) + '</li>';
            }
            html += '</ul>';
            html += '</div>';
        }

        // Actions
        html += '<div class="actions">';
        html += '<button class="btn btn-primary" onclick="generateProposal()">Generate Proposal (PDF)</button>';
        html += '<a href="/survey" class="btn btn-secondary">Start Over</a>';
        html += '</div>';

        // Download area (hidden until proposal is generated)
        html += '<div id="download-area" style="display:none;margin-top:24px;">';
        html += '<div class="tier-card" style="border-color:#16a34a;text-align:center;">';
        html += '<h3 style="color:#16a34a;">Proposal Ready</h3>';
        html += '<p style="margin:12px 0;">Your proposal has been generated.</p>';
        html += '<a id="download-link" class="btn btn-success" href="#">Download PDF</a>';
        html += '</div></div>';

        resultsEl.innerHTML = html;
    }

    // Generate proposal (attached to window for onclick)
    window.generateProposal = function () {
        var btn = document.querySelector('.actions .btn-primary');
        btn.textContent = "Generating...";
        btn.disabled = true;

        fetch("/api/proposal/" + sessionId + "/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: "{}",
        })
            .then(function (r) { return r.json(); })
            .then(function (data) {
                btn.textContent = "Generate Proposal (PDF)";
                btn.disabled = false;

                var dlArea = document.getElementById("download-area");
                var dlLink = document.getElementById("download-link");
                dlLink.href = "/api/proposal/" + sessionId + "/download";
                dlArea.style.display = "block";
                dlArea.scrollIntoView({ behavior: "smooth" });
            })
            .catch(function (err) {
                btn.textContent = "Generate Proposal (PDF)";
                btn.disabled = false;
                console.error(err);
                alert("Failed to generate proposal. Check the server logs.");
            });
    };

    function escHtml(str) {
        var div = document.createElement("div");
        div.textContent = str;
        return div.innerHTML;
    }
})();
