$(function () {

    // ****************************************
    // Update the form with data from the response
    // ****************************************
    function update_form_data(res) {
        $("#customer_id").val(res.id);
        $("#customer_name").val(res.name);
        $("#customer_address").val(res.address);
        $("#customer_status").val(res.status);
    }

    // ****************************************
    // Clear all form fields
    // ****************************************
    function clear_form_data() {
        $("#customer_name").val("");
        $("#customer_address").val("");
        $("#customer_status").val("active");
    }

    // ****************************************
    // Flash a message to the user
    // ****************************************
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

    // ****************************************
    // Create a Customer
    // ****************************************
    $("#create-btn").click(function () {
        let name = $("#customer_name").val();
        let address = $("#customer_address").val();
        let status = $("#customer_status").val();

        if (!name || name.trim() === "" || !address || address.trim() === "") {
            flash_message("Error: Name and Address are required");
            return;
        }

        let data = {
            "name": name,
            "address": address,
            "status": status
        };

        let ajax = $.ajax({
            type: "POST",
            url: "/customers",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            update_form_data(res);
            flash_message("Success");
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message);
        });
    });

    // ****************************************
    // Retrieve a Customer by ID
    // ****************************************
    $("#retrieve-btn").click(function () {
        let customer_id = $("#search_id").val();

        if (!customer_id || customer_id.trim() === "") {
            flash_message("Error: Customer ID is required");
            return;
        }

        let ajax = $.ajax({
            type: "GET",
            url: `/customers/${customer_id}`,
            contentType: "application/json",
        });

        ajax.done(function (res) {
            update_form_data(res);
            let row = `<tr>
                <td>${res.id}</td>
                <td>${res.name}</td>
                <td>${res.address}</td>
                <td>${res.status}</td>
            </tr>`;
            $("#results-body").empty();
            $("#results-body").append(row);
            flash_message("Success");
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message);
        });
    });

    // ****************************************
    // List All Customers
    // ****************************************
    $("#list-btn").click(function () {
        let ajax = $.ajax({
            type: "GET",
            url: "/customers",
            contentType: "application/json",
        });

        ajax.done(function (res) {
            $("#results-body").empty();
            if (res.length === 0) {
                let row = `<tr><td colspan="4">No customers found</td></tr>`;
                $("#results-body").append(row);
            } else {
                for (let i = 0; i < res.length; i++) {
                    let row = `<tr id="row_${res[i].id}">
                        <td>${res[i].id}</td>
                        <td>${res[i].name}</td>
                        <td>${res[i].address}</td>
                        <td>${res[i].status}</td>
                    </tr>`;
                    $("#results-body").append(row);
                }
            }
            flash_message("Success");
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message);
        });
    });

    // ****************************************
    // Update a Customer
    // ****************************************
    $("#update-btn").click(function () {
        let customer_id = $("#customer_id").val();

        if (!customer_id || customer_id.trim() === "") {
            flash_message("No customer selected to update");
            return;
        }

        let name = $("#customer_name").val();
        let address = $("#customer_address").val();
        let status = $("#customer_status").val();

        if (!name || name.trim() === "" || !address || address.trim() === "") {
            flash_message("Error: Name and Address are required");
            return;
        }

        let data = {
            "name": name,
            "address": address,
            "status": status
        };

        let ajax = $.ajax({
            type: "PUT",
            url: `/customers/${customer_id}`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            update_form_data(res);
            flash_message("Success");
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message);
        });
    });

    // ****************************************
    // Delete a Customer
    // ****************************************
    $("#delete-btn").click(function () {
        let customer_id = $("#customer_id").val();

        if (!customer_id || customer_id.trim() === "") {
            flash_message("No customer selected to delete");
            return;
        }

        let ajax = $.ajax({
            type: "DELETE",
            url: `/customers/${customer_id}`,
            contentType: "application/json",
        });

        ajax.done(function () {
            clear_form_data();
            $("#customer_id").val("");
            flash_message("Customer has been Deleted!");
        });

        ajax.fail(function () {
            flash_message("Server error!");
        });
    });

    // ****************************************
    // Query by Name
    // ****************************************
    $("#search-btn").click(function () {
        let name = $("#search_name").val();

        if (!name || name.trim() === "") {
            flash_message("Customer Name is required for search");
            return;
        }

        let ajax = $.ajax({
            type: "GET",
            url: `/customers?name=${name}`,
            contentType: "application/json",
        });

        ajax.done(function (res) {
            $("#results-body").empty();
            if (res.length === 0) {
                let row = `<tr><td colspan="4">No customers found</td></tr>`;
                $("#results-body").append(row);
            } else {
                for (let i = 0; i < res.length; i++) {
                    let row = `<tr id="row_${res[i].id}">
                        <td>${res[i].id}</td>
                        <td>${res[i].name}</td>
                        <td>${res[i].address}</td>
                        <td>${res[i].status}</td>
                    </tr>`;
                    $("#results-body").append(row);
                }
                update_form_data(res[0]);
            }
            flash_message("Success");
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message);
        });
    });

    // ****************************************
    // Suspend a Customer
    // ****************************************
    $("#suspend-btn").click(function () {
        let customer_id = $("#customer_id").val();

        if (!customer_id || customer_id.trim() === "") {
            flash_message("No customer selected to suspend");
            return;
        }

        let ajax = $.ajax({
            type: "PUT",
            url: `/customers/${customer_id}/suspend`,
            contentType: "application/json",
        });

        ajax.done(function (res) {
            update_form_data(res);
            flash_message("Success");
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message);
        });
    });

    // ****************************************
    // Activate a Customer
    // ****************************************
    $("#activate-btn").click(function () {
        let customer_id = $("#customer_id").val();

        if (!customer_id || customer_id.trim() === "") {
            flash_message("No customer selected to activate");
            return;
        }

        let ajax = $.ajax({
            type: "PUT",
            url: `/customers/${customer_id}/activate`,
            contentType: "application/json",
        });

        ajax.done(function (res) {
            update_form_data(res);
            flash_message("Success");
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message);
        });
    });

    // ****************************************
    // Clear Search
    // ****************************************
    $("#clear-btn").click(function () {
        $("#search_id").val("");
        $("#search_name").val("");
        $("#customer_id").val("");
        clear_form_data();
        $("#results-body").empty();
        $("#results-body").append(`<tr><td colspan="4">No results</td></tr>`);
        flash_message("Search cleared");
    });

    // ****************************************
    // Reset the Form
    // ****************************************
    $("#reset-form-btn").click(function () {
        $("#customer_id").val("");
        clear_form_data();
        flash_message("Form reset");
    });

});
