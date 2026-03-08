(function () {
    "use strict";

    function $(id) { return document.getElementById(id); }

    function showError(msg) {
        var el = $("loginError");
        el.textContent = msg;
        el.classList.remove("d-none");
    }

    function hideError() {
        $("loginError").classList.add("d-none");
    }

    function authHeaders(token) {
        return { "Authorization": "Basic " + token };
    }

    async function redirectByRole(token) {
        var adminCheck = await fetch("/admin/data/versions", { headers: authHeaders(token) });
        window.location.href = adminCheck.ok ? "/html/admin_data.html" : "/html/review_data.html";
    }

    async function attemptLogin() {
        var username = $("username").value.trim();
        var password = $("password").value;
        if (!username || !password) {
            showError("Enter your username and password.");
            return;
        }

        var token = btoa(username + ":" + password);
        var btn = $("loginBtn");
        btn.disabled = true;
        hideError();

        try {
            var r = await fetch("/admin/data/current", { headers: authHeaders(token) });
            if (r.status === 401) {
                showError("Invalid username or password.");
                return;
            }
            if (!r.ok) {
                showError("Server error (" + r.status + "). Please try again.");
                return;
            }
            sessionStorage.setItem("h2o_auth", token);
            await redirectByRole(token);
        } catch (_) {
            showError("Could not connect to server.");
        } finally {
            btn.disabled = false;
        }
    }

    document.addEventListener("DOMContentLoaded", function () {
        // If already signed in, redirect immediately
        var existing = sessionStorage.getItem("h2o_auth");
        if (existing) {
            fetch("/admin/data/current", { headers: authHeaders(existing) })
                .then(function (r) {
                    if (r.ok) return redirectByRole(existing);
                    sessionStorage.removeItem("h2o_auth");
                })
                .catch(function () {});
        }

        $("loginBtn").addEventListener("click", attemptLogin);
        ["username", "password"].forEach(function (id) {
            $(id).addEventListener("keydown", function (e) {
                if (e.key === "Enter") attemptLogin();
            });
        });

        // Focus username on load
        $("username").focus();
    });
})();
