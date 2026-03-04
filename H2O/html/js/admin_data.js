(function () {
    "use strict";

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
        card.className = "tool-card " + (cls || "");
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
        fetch("/admin/data/current")
            .then(function (r) {
                if (!r.ok) {
                    if (r.status === 401) {
                        showDataError("Login required to view packing data.");
                    } else {
                        showDataError("Could not load current data (HTTP " + r.status + ").");
                    }
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
        if (el) el.innerHTML = '<p class="error-msg">' + esc(msg) + "</p>";
    }

    function renderDataTable(productTypes, counts) {
        var el = $("currentDataContent");
        if (!el) return;

        if (!productTypes || Object.keys(productTypes).length === 0) {
            el.innerHTML = '<p class="empty-msg">No packing data available.</p>';
            return;
        }

        var sorted = Object.values(productTypes).sort(function (a, b) {
            return a.product_type_display_order - b.product_type_display_order
                || a.product_type_name.localeCompare(b.product_type_name);
        });

        var html = '<div class="data-summary">'
            + '<span>' + esc(counts.product_types) + ' product type' + (counts.product_types !== 1 ? 's' : '') + '</span>'
            + '<span class="sep">&bull;</span>'
            + '<span>' + esc(counts.skus) + ' SKU' + (counts.skus !== 1 ? 's' : '') + '</span>'
            + '</div>';

        sorted.forEach(function (pt) {
            var ptInactive = pt.product_type_active_flag !== "Y";
            var skus = Object.values(pt.skus || {}).sort(function (a, b) {
                return a.sku_display_order - b.sku_display_order
                    || a.sku_description.localeCompare(b.sku_description);
            });
            var activeCount = skus.filter(function (s) { return s.sku_active_flag === "Y"; }).length;

            html += '<div class="pt-group' + (ptInactive ? " pt-group--inactive" : "") + '">';
            html += '<div class="pt-header">'
                + '<span class="pt-name">' + esc(pt.product_type_name) + '</span>'
                + (ptInactive ? '<span class="badge badge-inactive">Inactive</span>' : '')
                + '<span class="pt-meta">' + esc(activeCount) + ' / ' + esc(skus.length) + ' active</span>'
                + '</div>';

            html += '<div class="table-wrap"><table class="sku-table">'
                + '<thead><tr>'
                + '<th>Description</th><th>Size</th><th>Length</th>'
                + '<th>Sticks / Bundle</th><th>Bundles / Truck</th><th>Actual Sticks / Truck</th>'
                + '<th>Popularity</th><th>Status</th><th>Notes</th>'
                + '</tr></thead><tbody>';

            skus.forEach(function (sku) {
                var inactive = sku.sku_active_flag !== "Y";
                html += '<tr class="' + (inactive ? "sku-row--inactive" : "") + '">'
                    + '<td class="sku-desc">' + esc(sku.sku_description) + '</td>'
                    + '<td>' + esc(sku.size_nominal) + '</td>'
                    + "<td>" + esc(sku.length_feet) + "'" + '</td>'
                    + '<td class="num">' + esc(sku.eagle_sticks_per_bundle) + '</td>'
                    + '<td class="num">' + esc(sku.eagle_bundles_per_truckload) + '</td>'
                    + '<td class="num">' + esc(sku.actual_sticks_per_truckload) + '</td>'
                    + '<td class="num">' + esc(sku.popularity_score) + '</td>'
                    + '<td><span class="badge ' + (inactive ? "badge-inactive" : "badge-active") + '">'
                    + (inactive ? "Inactive" : "Active") + '</span></td>'
                    + '<td class="notes-cell">' + esc(sku.notes || "") + '</td>'
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
        var r = await fetch(path, { method: "POST", body: fd });
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

    // -----------------------------------------------------------------------
    // Render helpers
    // -----------------------------------------------------------------------

    function renderValidationResult(v) {
        if (!v) return '<p class="error-msg">No validation data returned.</p>';
        if (v.is_valid) {
            var w = v.warnings ? v.warnings.length : 0;
            return '<div class="result-block result-block--ok">'
                + '<p class="result-headline">&#10003; Validation passed</p>'
                + '<p>' + esc(v.counts.product_types) + ' product type(s), '
                + esc(v.counts.skus) + ' SKU(s)</p>'
                + (w > 0
                    ? '<p>' + esc(w) + ' warning' + (w !== 1 ? 's' : '') + ':</p>'
                    + renderIssueList(v.warnings)
                    : '')
                + '</div>';
        }
        var ec = v.errors ? v.errors.length : 0;
        var wc = v.warnings ? v.warnings.length : 0;
        return '<div class="result-block result-block--error">'
            + '<p class="result-headline">&#10007; Validation failed — '
            + esc(ec) + ' error' + (ec !== 1 ? 's' : '')
            + (wc > 0 ? ', ' + esc(wc) + ' warning' + (wc !== 1 ? 's' : '') : '')
            + '</p>'
            + renderIssueList(v.errors)
            + (wc > 0 ? renderIssueList(v.warnings) : '')
            + '</div>';
    }

    function renderIssueList(issues) {
        if (!issues || issues.length === 0) return "";
        var html = '<ul class="issue-list">';
        issues.forEach(function (issue) {
            html += '<li class="issue-' + esc(issue.level) + '">';
            if (issue.row) html += 'Row ' + esc(issue.row) + ': ';
            if (issue.field) html += '<strong>' + esc(issue.field) + '</strong> — ';
            html += esc(issue.message) + '</li>';
        });
        html += '</ul>';
        return html;
    }

    function renderDiff(diff) {
        if (!diff) return '<p class="error-msg">No diff data returned.</p>';

        var added = diff.added_skus || [];
        var removed = diff.removed_skus || [];
        var changed = diff.changed_skus || {};
        var changedKeys = Object.keys(changed);
        var cc = diff.counts || {};

        var noChanges = added.length === 0 && removed.length === 0 && changedKeys.length === 0;

        var html = '<div class="diff-counts">'
            + '<div class="diff-count-box">'
            + '<span class="diff-count-label">Current</span>'
            + '<span class="diff-count-num">' + esc((cc.current || {}).skus || 0) + ' SKUs</span>'
            + '</div>'
            + '<div class="diff-count-box diff-count-box--uploaded">'
            + '<span class="diff-count-label">Uploaded</span>'
            + '<span class="diff-count-num">' + esc((cc.uploaded || {}).skus || 0) + ' SKUs</span>'
            + '</div>'
            + '</div>';

        if (noChanges) {
            html += '<div class="result-block result-block--ok">'
                + '<p class="result-headline">&#10003; No changes detected</p>'
                + '<p>The uploaded file matches the current published data.</p>'
                + '</div>';
            return html;
        }

        if (added.length > 0) {
            html += '<div class="diff-section">'
                + '<h3 class="diff-section-title diff-added-title">&#43; Added (' + esc(added.length) + ')</h3>'
                + '<ul class="diff-list diff-list--added">';
            added.forEach(function (k) { html += '<li>' + esc(k) + '</li>'; });
            html += '</ul></div>';
        }

        if (removed.length > 0) {
            html += '<div class="diff-section">'
                + '<h3 class="diff-section-title diff-removed-title">&#8722; Removed (' + esc(removed.length) + ')</h3>'
                + '<ul class="diff-list diff-list--removed">';
            removed.forEach(function (k) { html += '<li>' + esc(k) + '</li>'; });
            html += '</ul></div>';
        }

        if (changedKeys.length > 0) {
            html += '<div class="diff-section">'
                + '<h3 class="diff-section-title diff-changed-title">&#9651; Changed (' + esc(changedKeys.length) + ')</h3>';
            changedKeys.forEach(function (key) {
                html += '<div class="changed-sku">'
                    + '<div class="changed-sku-name">' + esc(key) + '</div>'
                    + '<table class="changes-table"><thead>'
                    + '<tr><th>Field</th><th>Before</th><th>After</th></tr>'
                    + '</thead><tbody>';
                (changed[key] || []).forEach(function (c) {
                    html += '<tr>'
                        + '<td class="change-field">' + esc(c.field) + '</td>'
                        + '<td class="change-before">' + esc(c.before == null ? "" : c.before) + '</td>'
                        + '<td class="change-after">' + esc(c.after == null ? "" : c.after) + '</td>'
                        + '</tr>';
                });
                html += '</tbody></table></div>';
            });
            html += '</div>';
        }

        return html;
    }

    function renderError(err) {
        if (err.status === 401) {
            return '<div class="result-block result-block--error">'
                + '<p class="result-headline">&#10007; Unauthorized</p>'
                + '<p>Check your username and password.</p></div>';
        }
        if (err.status === 400 && err.payload && err.payload.is_valid === false) {
            return renderValidationResult(err.payload);
        }
        var msg = (err.payload && typeof err.payload === "object" && err.payload.detail)
            ? err.payload.detail
            : (typeof err.payload === "string" ? err.payload : err.message || "Unknown error");
        return '<div class="result-block result-block--error">'
            + '<p class="result-headline">&#10007; Error</p>'
            + '<p>' + esc(msg) + '</p></div>';
    }

    // -----------------------------------------------------------------------
    // Actions
    // -----------------------------------------------------------------------

    async function handleValidate() {
        var file = getFile();
        if (!file) { showResults("Validate", '<p class="error-msg">Select an .xlsx file first.</p>', "tool-card--error"); return; }
        hideResults();
        setBusy(true);
        try {
            var payload = await postFile("/admin/data/validate", file);
            showResults("Validation Result", renderValidationResult(payload),
                payload.is_valid ? "tool-card--ok" : "tool-card--error");
        } catch (err) {
            showResults("Validation Error", renderError(err), "tool-card--error");
        } finally {
            setBusy(false);
        }
    }

    async function handlePreview() {
        var file = getFile();
        if (!file) { showResults("Preview", '<p class="error-msg">Select an .xlsx file first.</p>', "tool-card--error"); return; }
        hideResults();
        setBusy(true);
        try {
            var payload = await postFile("/admin/data/preview", file);
            var html = renderValidationResult(payload.validation) + renderDiff(payload.diff);
            showResults("Preview Changes", html, "tool-card--neutral");
        } catch (err) {
            showResults("Preview Error", renderError(err), "tool-card--error");
        } finally {
            setBusy(false);
        }
    }

    async function handlePublish() {
        var file = getFile();
        var reason = $("changeReason") ? $("changeReason").value.trim() : "";
        if (!file) { showResults("Publish", '<p class="error-msg">Select an .xlsx file first.</p>', "tool-card--error"); return; }
        if (!reason) { showResults("Publish", '<p class="error-msg">Change reason is required.</p>', "tool-card--error"); return; }
        hideResults();
        setBusy(true);
        try {
            var payload = await postFile("/admin/data/publish", file, { change_reason: reason });
            var html = '<div class="result-block result-block--ok">'
                + '<p class="result-headline">&#10003; Published successfully</p>'
                + '<table class="info-table"><tbody>'
                + '<tr><th>Version ID</th><td>' + esc(payload.version_id) + '</td></tr>'
                + '<tr><th>Product types</th><td>' + esc(payload.counts.product_types) + '</td></tr>'
                + '<tr><th>SKUs</th><td>' + esc(payload.counts.skus) + '</td></tr>'
                + '</tbody></table></div>';
            showResults("Publish Result", html, "tool-card--ok");
            loadCurrentData();
        } catch (err) {
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
        content.innerHTML = '<p class="loading-msg">Loading&hellip;</p>';
        if (btn) btn.disabled = true;

        fetch("/admin/data/versions")
            .then(function (r) {
                if (!r.ok) throw new Error("HTTP " + r.status);
                return r.json();
            })
            .then(function (data) {
                var versions = data.versions || [];
                if (versions.length === 0) {
                    content.innerHTML = '<p class="muted-msg">No published versions found.</p>';
                    return;
                }
                var html = '<table class="versions-table"><thead>'
                    + '<tr><th>Version</th><th>Published</th><th>SKUs</th><th>Change Reason</th></tr>'
                    + '</thead><tbody>';
                versions.forEach(function (v) {
                    var dt = v.published_at ? new Date(v.published_at).toLocaleString() : v.version_id;
                    html += '<tr>'
                        + '<td class="version-id">' + esc(v.version_id) + '</td>'
                        + '<td>' + esc(dt) + '</td>'
                        + '<td class="num">' + esc((v.counts || {}).skus || "—") + '</td>'
                        + '<td>' + esc(v.change_reason || "") + '</td>'
                        + '</tr>';
                });
                html += '</tbody></table>';
                content.innerHTML = html;
            })
            .catch(function (err) {
                content.innerHTML = '<p class="error-msg">Could not load version history: ' + esc(err.message) + '</p>';
            })
            .finally(function () {
                if (btn) btn.disabled = false;
            });
    }

    // -----------------------------------------------------------------------
    // Wiring
    // -----------------------------------------------------------------------

    document.addEventListener("DOMContentLoaded", function () {
        loadCurrentData();

        var validateBtn = $("validateBtn");
        var previewBtn = $("previewBtn");
        var publishBtn = $("publishBtn");
        var loadVersionsBtn = $("loadVersionsBtn");

        if (validateBtn) validateBtn.addEventListener("click", handleValidate);
        if (previewBtn) previewBtn.addEventListener("click", handlePreview);
        if (publishBtn && getRole() === "admin") {
            publishBtn.addEventListener("click", handlePublish);
        }
        if (loadVersionsBtn) {
            loadVersionsBtn.addEventListener("click", loadVersionHistory);
        }
    });
})();
