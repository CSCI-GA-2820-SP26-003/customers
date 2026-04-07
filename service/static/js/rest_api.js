$(function () {

    function update_form_data(res) {
        $("#customer_id").val(res.id);
        $("#customer_name").val(res.name);
        $("#customer_address").val(res.address);
        $("#customer_status").val(res.status);
    }

    function clear_form_data() {
        $("#customer_name").val("");
        $("#customer_address").val("");
        $("#customer_status").val("active");
    }

    function flash_message(message) {
        $("#flash-message").removeClass("success error info hidden");
        $("#flash-message").text(message);
        if (message.includes("Success")) {
            $("#flash-message").addClass("success");
        } else if (message.includes("Error") || message.includes("error")) {
            $("#flash-message").addClass("error");
        } else {
            $("#flash-message").addClass("info");
        }
    }

    function fail_message(res) {
        const msg = (res.responseJSON && res.responseJSON.message)
            ? res.responseJSON.message
            : "Request failed";
        flash_message(msg);
    }

    function current_customer_id() {
        const id = $("#customer_id").val();
        return id && id.trim() !== "" ? id.trim() : null;
    }

    function render_results_rows(list) {
        const body = $("#results-body");
        body.empty();
        if (!list.length) {
            body.append('<tr><td colspan="4" class="empty-state">No customers</td></tr>');
            return;
        }
        list.forEach(function (res) {
            const row = `<tr>
                <td>${res.id}</td>
                <td>${res.name}</td>
                <td>${res.address}</td>
                <td>${res.status}</td>
            </tr>`;
            body.append(row);
        });
    }

    $("#service-info-btn").click(function () {
        const ajax = $.ajax({ type: "GET", url: "/" });
        ajax.done(function (res) {
            flash_message("Success: " + JSON.stringify(res));
        });
        ajax.fail(fail_message);
    });

    $("#health-btn").click(function () {
        const ajax = $.ajax({ type: "GET", url: "/health" });
        ajax.done(function (res) {
            flash_message("Success: " + JSON.stringify(res));
        });
        ajax.fail(fail_message);
    });

    $("#create-btn").click(function () {
        const name = $("#customer_name").val();
        const address = $("#customer_address").val();
        const statusVal = $("#customer_status").val();

        if (!name || name.trim() === "" || !address || address.trim() === "") {
            flash_message("Error: Name and Address are required");
            return;
        }

        const data = {
            name: name,
            address: address,
            status: statusVal
        };

        const ajax = $.ajax({
            type: "POST",
            url: "/customers",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            update_form_data(res);
            render_results_rows([res]);
            flash_message("Success");
        });

        ajax.fail(fail_message);
    });

    $("#retrieve-btn").click(function () {
        const customer_id = $("#search_id").val();

        if (!customer_id || customer_id.trim() === "") {
            flash_message("Error: Customer ID is required");
            return;
        }

        const ajax = $.ajax({
            type: "GET",
            url: `/customers/${customer_id}`,
            contentType: "application/json",
        });

        ajax.done(function (res) {
            update_form_data(res);
            render_results_rows([res]);
            flash_message("Success");
        });

        ajax.fail(fail_message);
    });

    $("#search-btn").click(function () {
        const q = $("#search_name").val();
        if (!q || q.trim() === "") {
            flash_message("Error: Customer name is required");
            return;
        }
        const ajax = $.ajax({
            type: "GET",
            url: "/customers",
            data: { name: q.trim() },
        });
        ajax.done(function (res) {
            if (res.length === 1) {
                update_form_data(res[0]);
            }
            render_results_rows(res);
            flash_message("Success");
        });
        ajax.fail(fail_message);
    });

    $("#list-btn").click(function () {
        const ajax = $.ajax({ type: "GET", url: "/customers" });
        ajax.done(function (res) {
            render_results_rows(res);
            flash_message("Success");
        });
        ajax.fail(fail_message);
    });

    $("#clear-btn").click(function () {
        $("#search_id").val("");
        $("#search_name").val("");
        $("#results-body").empty();
        $("#results-body").append(
            '<tr><td colspan="4" class="empty-state">No data loaded yet.</td></tr>'
        );
        flash_message("Cleared");
    });

    $("#update-btn").click(function () {
        const id = current_customer_id();
        if (!id) {
            flash_message("Error: Customer ID is required");
            return;
        }
        const name = $("#customer_name").val();
        const address = $("#customer_address").val();
        const statusVal = $("#customer_status").val();
        if (!name || name.trim() === "" || !address || address.trim() === "") {
            flash_message("Error: Name and Address are required");
            return;
        }
        const data = { name: name.trim(), address: address.trim(), status: statusVal };
        const ajax = $.ajax({
            type: "PUT",
            url: `/customers/${id}`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });
        ajax.done(function (res) {
            update_form_data(res);
            render_results_rows([res]);
            flash_message("Success");
        });
        ajax.fail(fail_message);
    });

    $("#delete-btn").click(function () {
        const id = current_customer_id();
        if (!id) {
            flash_message("Error: Customer ID is required");
            return;
        }
        const ajax = $.ajax({ type: "DELETE", url: `/customers/${id}` });
        ajax.done(function () {
            $("#customer_id").val("");
            clear_form_data();
            $("#results-body").empty();
            $("#results-body").append(
                '<tr><td colspan="4" class="empty-state">No data loaded yet.</td></tr>'
            );
            flash_message("Success");
        });
        ajax.fail(fail_message);
    });

    $("#suspend-btn").click(function () {
        const id = current_customer_id();
        if (!id) {
            flash_message("Error: Customer ID is required");
            return;
        }
        const ajax = $.ajax({ type: "PUT", url: `/customers/${id}/suspend` });
        ajax.done(function (res) {
            update_form_data(res);
            render_results_rows([res]);
            flash_message("Success");
        });
        ajax.fail(fail_message);
    });

    $("#activate-btn").click(function () {
        const id = current_customer_id();
        if (!id) {
            flash_message("Error: Customer ID is required");
            return;
        }
        const ajax = $.ajax({ type: "PUT", url: `/customers/${id}/activate` });
        ajax.done(function (res) {
            update_form_data(res);
            render_results_rows([res]);
            flash_message("Success");
        });
        ajax.fail(fail_message);
    });

    $("#reset-form-btn").click(function () {
        $("#customer_id").val("");
        clear_form_data();
        flash_message("Form reset");
    });

});
