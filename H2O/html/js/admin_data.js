(function () {
    "use strict";

    // -----------------------------------------------------------------------
    // Auth
    // -----------------------------------------------------------------------

    function getToken() {
        return sessionStorage.getItem("h2o_auth") || "";
    }

    function authHeaders() {
        var token = getToken();
        return token ? { "Authorization": "Basic " + token } : {};
    }

    function signOut() {
        sessionStorage.removeItem("h2o_auth");
        window.location.href = "/html/login.html";
    }

    function requireAuth() {
        if (!getToken()) {
            window.location.href = "/html/login.html";
            return false;
        }
        return true;
    }

    function handleUnauthorized() {
        sessionStorage.removeItem("h2o_auth");
        window.location.href = "/html/login.html";
    }

    // -----------------------------------------------------------------------
    // Utilities
    // -----------------------------------------------------------------------

    function esc(value) {
        return String(value == null ? "" : value)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#39;");
    }

    function $(id) { return document.getElementById(id); }

    function getRole() {
        return document.body.getAttribute("data-role") || "review";
    }

    function getFile() {
        var input = $("workbookFile");
        return input && input.files && input.files[0] ? input.files[0] : null;
    }

    function setBusy(busy) {
        document.querySelectorAll("[data-action]").forEach(function (el) {
            el.disabled = busy;
        });
    }

    function showResults(title, html, cls) {
        var card = $("resultsCard");
        var titleEl = $("resultsTitle");
        var content = $("resultsContent");
        if (!card) return;
        titleEl.textContent = title;
        content.innerHTML = html;
        card.hidden = false;
        var borderCls = cls === "tool-card--ok" ? " border-success"
                      : cls === "tool-card--error" ? " border-danger" : "";
        card.className = "card mb-4 shadow-sm" + borderCls;
        card.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    function hideResults() {
        var card = $("resultsCard");
        if (card) card.hidden = true;
    }

    // -----------------------------------------------------------------------
    // Current data table
    // -----------------------------------------------------------------------

    function loadCurrentData() {
        fetch("/admin/data/current", { headers: authHeaders() })
            .then(function (r) {
                if (r.status === 401) { handleUnauthorized(); return null; }
                if (!r.ok) {
                    showDataError("Could not load current data (HTTP " + r.status + ").");
                    return null;
                }
                return r.json();
            })
            .then(function (data) {
                if (!data) return;
                renderDataTable(data.product_types, data.counts);
            })
            .catch(function () {
                showDataError("Could not connect to server.");
            });
    }

    function showDataError(msg) {
        var el = $("currentDataContent");
        if (el) el.innerHTML = '<p class="text-danger mb-0">' + esc(msg) + "</p>";
    }

    function renderDataTable(productTypes, counts) {
        var el = $("currentDataContent");
        if (!el) return;

        if (!productTypes || Object.keys(productTypes).length === 0) {
            el.innerHTML = '<p class="text-muted mb-0">No packing data available.</p>';
            return;
        }

        var sorted = Object.values(productTypes).sort(function (a, b) {
            return a.product_type_display_order - b.product_type_display_order
                || a.product_type_name.localeCompare(b.product_type_name);
        });

        var html = '<p class="text-muted small mb-3">'
            + esc(counts.product_types) + ' product type' + (counts.product_types !== 1 ? 's' : '')
            + ' &bull; '
            + esc(counts.skus) + ' SKU' + (counts.skus !== 1 ? 's' : '')
            + '</p>';

        sorted.forEach(function (pt) {
            var ptInactive = pt.product_type_active_flag !== "Y";
            var skus = Object.values(pt.skus || {}).sort(function (a, b) {
                return a.sku_display_order - b.sku_display_order
                    || a.sku_description.localeCompare(b.sku_description);
            });
            var activeCount = skus.filter(function (s) { return s.sku_active_flag === "Y"; }).length;

            html += '<div class="mb-4' + (ptInactive ? ' opacity-75' : '') + '">';
            html += '<div class="d-flex align-items-center gap-2 mb-2">'
                + '<span class="fw-semibold">' + esc(pt.product_type_name) + '</span>'
                + (ptInactive ? '<span class="badge bg-secondary">Inactive</span>' : '')
                + '<span class="ms-auto small text-muted">' + esc(activeCount) + ' / ' + esc(skus.length) + ' active</span>'
                + '</div>';

            html += '<div class="table-responsive"><table class="table table-sm table-bordered mb-0">'
                + '<thead class="table-dark"><tr>'
                + '<th>Description</th><th>Size</th><th>Length</th>'
                + '<th class="text-end">Sticks / Bundle</th><th class="text-end">Bundles / Truck</th>'
                + '<th class="text-end">Actual Sticks / Truck</th><th class="text-end">Popularity</th>'
                + '<th>Status</th><th>Notes</th>'
                + '</tr></thead><tbody>';

            skus.forEach(function (sku) {
                var inactive = sku.sku_active_flag !== "Y";
                html += '<tr class="' + (inactive ? 'table-secondary' : '') + '">'
                    + '<td>' + esc(sku.sku_description) + '</td>'
                    + '<td>' + esc(sku.size_nominal) + '</td>'
                    + "<td>" + esc(sku.length_feet) + "'" + '</td>'
                    + '<td class="text-end">' + esc(sku.eagle_sticks_per_bundle) + '</td>'
                    + '<td class="text-end">' + esc(sku.eagle_bundles_per_truckload) + '</td>'
                    + '<td class="text-end">' + esc(sku.actual_sticks_per_truckload) + '</td>'
                    + '<td class="text-end">' + esc(sku.popularity_score) + '</td>'
                    + '<td><span class="badge ' + (inactive ? 'bg-secondary' : 'bg-success') + '">'
                    + (inactive ? 'Inactive' : 'Active') + '</span></td>'
                    + '<td>' + esc(sku.notes || '') + '</td>'
                    + '</tr>';
            });

            html += '</tbody></table></div></div>';
        });

        el.innerHTML = html;
    }

    // -----------------------------------------------------------------------
    // API helpers
    // -----------------------------------------------------------------------

    async function postFile(path, file, extra) {
        var fd = new FormData();
        fd.append("file", file);
        if (extra) {
            Object.keys(extra).forEach(function (k) { fd.append(k, extra[k]); });
        }
        var r = await fetch(path, { method: "POST", body: fd, headers: authHeaders() });
        if (r.status === 401) { handleUnauthorized(); throw new Error("Unauthorized"); }
        var ct = r.headers.get("content-type") || "";
        var body = ct.includes("application/json") ? await r.json() : await r.text();
        if (!r.ok) {
            var err = new Error("HTTP " + r.status);
            err.status = r.status;
            err.payload = body;
            throw err;
        }
        return body;
    }

    async function triggerDownload(path, filename) {
        try {
            var r = await fetch(path, { headers: authHeaders() });
            if (r.status === 401) { handleUnauthorized(); return; }
            if (!r.ok) { alert("Download failed (HTTP " + r.status + ")."); return; }
            var blob = await r.blob();
            var url = URL.createObjectURL(blob);
            var a = document.createElement("a");
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        } catch (_) {
            alert("Download failed. Please try again.");
        }
    }

    function handleDownload() {
        var ts = new Date().toISOString().slice(0, 10).replace(/-/g, "");
        triggerDownload("/admin/data/current_excel", "packing_data_" + ts + ".xlsx");
    }

    function handleDownloadJson() {
        triggerDownload("/admin/data/current_json", "load_packing_data.js");
    }

    // -----------------------------------------------------------------------
    // Render helpers
    // -----------------------------------------------------------------------

    function renderValidationResult(v) {
        if (!v) return '<p class="text-danger mb-0">No validation data returned.</p>';
        if (v.is_valid) {
            var w = v.warnings ? v.warnings.length : 0;
            return '<div class="alert alert-success mb-3">'
                + '<p class="fw-semibold mb-1">&#10003; Validation passed</p>'
                + '<p class="mb-' + (w > 0 ? '1' : '0') + '">' + esc(v.counts.product_types) + ' product type(s), '
                + esc(v.counts.skus) + ' SKU(s)</p>'
                + (w > 0
                    ? '<p class="mb-1">' + esc(w) + ' warning' + (w !== 1 ? 's' : '') + ':</p>'
                    + renderIssueList(v.warnings)
                    : '')
                + '</div>';
        }
        var ec = v.errors ? v.errors.length : 0;
        var wc = v.warnings ? v.warnings.length : 0;
        return '<div class="alert alert-danger mb-3">'
            + '<p class="fw-semibold mb-1">&#10007; Validation failed — '
            + esc(ec) + ' error' + (ec !== 1 ? 's' : '')
            + (wc > 0 ? ', ' + esc(wc) + ' warning' + (wc !== 1 ? 's' : '') : '')
            + '</p>'
            + renderIssueList(v.errors)
            + (wc > 0 ? renderIssueList(v.warnings) : '')
            + '</div>';
    }

    function renderIssueList(issues) {
        if (!issues || issues.length === 0) return "";
        var html = '<ul class="mb-0 ps-3">';
        issues.forEach(function (issue) {
            var liCls = issue.level === "error" ? "text-danger" : "text-warning-emphasis";
            html += '<li class="' + liCls + '">';
            if (issue.row) html += 'Row ' + esc(issue.row) + ': ';
            if (issue.field) html += '<strong>' + esc(issue.field) + '</strong> — ';
            html += esc(issue.message) + '</li>';
        });
        html += '</ul>';
        return html;
    }

    function renderDiff(diff) {
        if (!diff) return '<p class="text-danger mb-0">No diff data returned.</p>';

        var added = diff.added_skus || [];
        var removed = diff.removed_skus || [];
        var changed = diff.changed_skus || {};
        var changedKeys = Object.keys(changed);
        var cc = diff.counts || {};

        var noChanges = added.length === 0 && removed.length === 0 && changedKeys.length === 0;

        var html = '<div class="d-flex gap-3 mb-3">'
            + '<div class="border rounded p-2 text-center">'
            + '<span class="small text-muted d-block">Current</span>'
            + '<span class="fw-bold d-block fs-5">' + esc((cc.current || {}).skus || 0) + ' SKUs</span>'
            + '</div>'
            + '<div class="border rounded p-2 text-center">'
            + '<span class="small text-muted d-block">Uploaded</span>'
            + '<span class="fw-bold d-block fs-5">' + esc((cc.uploaded || {}).skus || 0) + ' SKUs</span>'
            + '</div>'
            + '</div>';

        if (noChanges) {
            html += '<div class="alert alert-success mb-0">'
                + '<p class="fw-semibold mb-1">&#10003; No changes detected</p>'
                + '<p class="mb-0">The uploaded file matches the current published data.</p>'
                + '</div>';
            return html;
        }

        if (added.length > 0) {
            html += '<div class="mb-3">'
                + '<h6 class="fw-semibold text-success">&#43; Added (' + esc(added.length) + ')</h6>'
                + '<ul class="list-group list-group-flush">';
            added.forEach(function (k) {
                html += '<li class="list-group-item list-group-item-success py-1 small">' + esc(k) + '</li>';
            });
            html += '</ul></div>';
        }

        if (removed.length > 0) {
            html += '<div class="mb-3">'
                + '<h6 class="fw-semibold text-danger">&#8722; Removed (' + esc(removed.length) + ')</h6>'
                + '<ul class="list-group list-group-flush">';
            removed.forEach(function (k) {
                html += '<li class="list-group-item list-group-item-danger py-1 small">' + esc(k) + '</li>';
            });
            html += '</ul></div>';
        }

        if (changedKeys.length > 0) {
            html += '<div class="mb-3">'
                + '<h6 class="fw-semibold text-warning-emphasis">&#9651; Changed (' + esc(changedKeys.length) + ')</h6>';
            changedKeys.forEach(function (key) {
                html += '<div class="mb-3">'
                    + '<div class="fw-semibold mb-1">' + esc(key) + '</div>'
                    + '<table class="table table-sm table-bordered mb-0"><thead>'
                    + '<tr><th>Field</th><th>Before</th><th>After</th></tr>'
                    + '</thead><tbody>';
                (changed[key] || []).forEach(function (c) {
                    html += '<tr>'
                        + '<td class="text-muted">' + esc(c.field) + '</td>'
                        + '<td class="text-danger">' + esc(c.before == null ? "" : c.before) + '</td>'
                        + '<td class="text-success">' + esc(c.after == null ? "" : c.after) + '</td>'
                        + '</tr>';
                });
                html += '</tbody></table></div>';
            });
            html += '</div>';
        }

        return html;
    }

    function renderError(err) {
        if (err.status === 401) { handleUnauthorized(); return ""; }
        if (err.status === 400 && err.payload && err.payload.is_valid === false) {
            return renderValidationResult(err.payload);
        }
        var msg = (err.payload && typeof err.payload === "object" && err.payload.detail)
            ? err.payload.detail
            : (typeof err.payload === "string" ? err.payload : err.message || "Unknown error");
        return '<div class="alert alert-danger mb-0">'
            + '<p class="fw-semibold mb-1">&#10007; Error</p>'
            + '<p class="mb-0">' + esc(msg) + '</p></div>';
    }

    // -----------------------------------------------------------------------
    // Actions
    // -----------------------------------------------------------------------

    async function handleValidate() {
        var file = getFile();
        if (!file) { showResults("Validate", '<p class="text-danger mb-0">Select an .xlsx file first.</p>', "tool-card--error"); return; }
        hideResults();
        setBusy(true);
        try {
            var payload = await postFile("/admin/data/validate", file);
            showResults("Validation Result", renderValidationResult(payload),
                payload.is_valid ? "tool-card--ok" : "tool-card--error");
        } catch (err) {
            if (err.message === "Unauthorized") return;
            showResults("Validation Error", renderError(err), "tool-card--error");
        } finally {
            setBusy(false);
        }
    }

    async function handlePreview() {
        var file = getFile();
        if (!file) { showResults("Preview", '<p class="text-danger mb-0">Select an .xlsx file first.</p>', "tool-card--error"); return; }
        hideResults();
        setBusy(true);
        try {
            var payload = await postFile("/admin/data/preview", file);
            var html = renderValidationResult(payload.validation) + renderDiff(payload.diff);
            showResults("Preview Changes", html, "tool-card--neutral");
        } catch (err) {
            if (err.message === "Unauthorized") return;
            showResults("Preview Error", renderError(err), "tool-card--error");
        } finally {
            setBusy(false);
        }
    }

    async function handlePublish() {
        var file = getFile();
        var reason = $("changeReason") ? $("changeReason").value.trim() : "";
        if (!file) { showResults("Publish", '<p class="text-danger mb-0">Select an .xlsx file first.</p>', "tool-card--error"); return; }
        if (!reason) { showResults("Publish", '<p class="text-danger mb-0">Change reason is required.</p>', "tool-card--error"); return; }
        hideResults();
        setBusy(true);
        try {
            var payload = await postFile("/admin/data/publish", file, { change_reason: reason });
            var html = '<div class="alert alert-success mb-0">'
                + '<p class="fw-semibold mb-2">&#10003; Published successfully</p>'
                + '<table class="table table-sm mb-0"><tbody>'
                + '<tr><th>Version ID</th><td>' + esc(payload.version_id) + '</td></tr>'
                + '<tr><th>Product types</th><td>' + esc(payload.counts.product_types) + '</td></tr>'
                + '<tr><th>SKUs</th><td>' + esc(payload.counts.skus) + '</td></tr>'
                + '</tbody></table></div>';
            showResults("Publish Result", html, "tool-card--ok");
            loadCurrentData();
        } catch (err) {
            if (err.message === "Unauthorized") return;
            showResults("Publish Error", renderError(err), "tool-card--error");
        } finally {
            setBusy(false);
        }
    }

    // -----------------------------------------------------------------------
    // Version history (admin only)
    // -----------------------------------------------------------------------

    function loadVersionHistory() {
        var btn = $("loadVersionsBtn");
        var content = $("versionsContent");
        if (!content) return;
        content.innerHTML = '<p class="text-muted mb-0">Loading&hellip;</p>';
        if (btn) btn.disabled = true;

        fetch("/admin/data/versions", { headers: authHeaders() })
            .then(function (r) {
                if (r.status === 401) { handleUnauthorized(); return null; }
                if (!r.ok) throw new Error("HTTP " + r.status);
                return r.json();
            })
            .then(function (data) {
                if (!data) return;
                var versions = data.versions || [];
                if (versions.length === 0) {
                    content.innerHTML = '<p class="text-muted mb-0">No published versions found.</p>';
                    return;
                }
                var html = '<div class="table-responsive"><table class="table table-sm table-hover mb-0"><thead>'
                    + '<tr><th>Version</th><th>Published</th><th class="text-end">SKUs</th><th>Change Reason</th></tr>'
                    + '</thead><tbody>';
                versions.forEach(function (v) {
                    var dt = v.published_at ? new Date(v.published_at).toLocaleString() : v.version_id;
                    html += '<tr>'
                        + '<td class="font-monospace small">' + esc(v.version_id) + '</td>'
                        + '<td>' + esc(dt) + '</td>'
                        + '<td class="text-end">' + esc((v.counts || {}).skus || "—") + '</td>'
                        + '<td>' + esc(v.change_reason || "") + '</td>'
                        + '</tr>';
                });
                html += '</tbody></table></div>';
                content.innerHTML = html;
            })
            .catch(function (err) {
                content.innerHTML = '<p class="text-danger mb-0">Could not load version history: ' + esc(err.message) + '</p>';
            })
            .finally(function () {
                if (btn) btn.disabled = false;
            });
    }

    // -----------------------------------------------------------------------
    // Wiring
    // -----------------------------------------------------------------------

    document.addEventListener("DOMContentLoaded", function () {
        if (!requireAuth()) return;

        loadCurrentData();

        var validateBtn = $("validateBtn");
        var previewBtn = $("previewBtn");
        var publishBtn = $("publishBtn");
        var loadVersionsBtn = $("loadVersionsBtn");
        var downloadBtn = $("downloadBtn");
        var downloadJsonBtn = $("downloadJsonBtn");
        var signOutBtn = $("signOutBtn");

        if (validateBtn) validateBtn.addEventListener("click", handleValidate);
        if (previewBtn) previewBtn.addEventListener("click", handlePreview);
        if (publishBtn && getRole() === "admin") {
            publishBtn.addEventListener("click", handlePublish);
        }
        if (loadVersionsBtn) loadVersionsBtn.addEventListener("click", loadVersionHistory);
        if (downloadBtn) downloadBtn.addEventListener("click", handleDownload);
        if (downloadJsonBtn) downloadJsonBtn.addEventListener("click", handleDownloadJson);
        if (signOutBtn) signOutBtn.addEventListener("click", signOut);
    });
})();
