/**
 * Survey flow — multi-step questionnaire with category navigation.
 * No framework dependencies.
 */

(function () {
    "use strict";

    let categories = [];
    let currentCategory = 0;
    let answers = {};

    const surveyEl = document.getElementById("survey");
    const loadingEl = document.getElementById("loading");
    const contactEl = document.getElementById("contact-step");
    const submittingEl = document.getElementById("submitting");
    const categoryEl = document.getElementById("category-container");
    const progressBar = document.getElementById("progress-bar");
    const progressText = document.getElementById("progress-text");
    const btnPrev = document.getElementById("btn-prev");
    const btnNext = document.getElementById("btn-next");
    const btnBackContact = document.getElementById("btn-back-contact");
    const btnSubmit = document.getElementById("btn-submit");

    // Load questions
    fetch("/api/questions")
        .then(function (r) { return r.json(); })
        .then(function (data) {
            categories = data.categories;
            loadingEl.style.display = "none";
            surveyEl.style.display = "block";
            renderCategory();
        });

    // Navigation
    btnNext.addEventListener("click", function () {
        if (currentCategory < categories.length - 1) {
            currentCategory++;
            renderCategory();
        } else {
            // Show contact form
            surveyEl.style.display = "none";
            contactEl.style.display = "block";
        }
    });

    btnPrev.addEventListener("click", function () {
        if (currentCategory > 0) {
            currentCategory--;
            renderCategory();
        }
    });

    btnBackContact.addEventListener("click", function () {
        contactEl.style.display = "none";
        surveyEl.style.display = "block";
        renderCategory();
    });

    btnSubmit.addEventListener("click", submitSurvey);

    function renderCategory() {
        var cat = categories[currentCategory];
        var total = categories.length;
        var pct = ((currentCategory + 1) / total) * 100;

        progressBar.style.width = pct + "%";
        progressText.textContent = "Step " + (currentCategory + 1) + " of " + total;

        btnPrev.style.display = currentCategory > 0 ? "inline-block" : "none";
        btnNext.textContent = currentCategory < total - 1 ? "Next" : "Continue";

        var html = '<h2 class="category-title">' + escHtml(cat.title) + "</h2>";
        html += '<p class="category-description">' + escHtml(cat.description) + "</p>";

        for (var i = 0; i < cat.questions.length; i++) {
            var q = cat.questions[i];
            html += '<div class="question">';
            html += '<div class="question-text">' + escHtml(q.text) + "</div>";
            html += '<div class="options">';

            for (var j = 0; j < q.options.length; j++) {
                var opt = q.options[j];
                var selected = answers[q.id] === opt.value ? " selected" : "";
                var checked = answers[q.id] === opt.value ? " checked" : "";
                html += '<div class="option' + selected + '" data-qid="' + q.id + '" data-value="' + opt.value + '">';
                html += '<input type="radio" name="' + q.id + '" value="' + opt.value + '"' + checked + '>';
                html += "<label>" + escHtml(opt.label) + "</label>";
                html += "</div>";
            }
            html += "</div></div>";
        }

        categoryEl.innerHTML = html;

        // Attach click handlers
        var options = categoryEl.querySelectorAll(".option");
        for (var k = 0; k < options.length; k++) {
            options[k].addEventListener("click", onOptionClick);
        }

        window.scrollTo(0, 0);
    }

    function onOptionClick(e) {
        var el = e.currentTarget;
        var qid = el.getAttribute("data-qid");
        var value = el.getAttribute("data-value");

        answers[qid] = value;

        // Update UI — deselect siblings, select this
        var siblings = el.parentNode.querySelectorAll(".option");
        for (var i = 0; i < siblings.length; i++) {
            siblings[i].classList.remove("selected");
            siblings[i].querySelector("input").checked = false;
        }
        el.classList.add("selected");
        el.querySelector("input").checked = true;
    }

    function submitSurvey() {
        var clientName = document.getElementById("client_name").value || "Prospective Client";
        var contactEmail = document.getElementById("contact_email").value || "";

        contactEl.style.display = "none";
        submittingEl.style.display = "block";

        fetch("/api/submit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                answers: answers,
                client_name: clientName,
                contact_email: contactEmail,
            }),
        })
            .then(function (r) { return r.json(); })
            .then(function (data) {
                window.location.href = "/results/" + data.session_id;
            })
            .catch(function (err) {
                submittingEl.innerHTML =
                    '<div class="loading"><p>Something went wrong. Please try again.</p></div>';
                console.error(err);
            });
    }

    function escHtml(str) {
        var div = document.createElement("div");
        div.textContent = str;
        return div.innerHTML;
    }
})();
