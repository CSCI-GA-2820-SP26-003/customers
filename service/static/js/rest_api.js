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
    // Reset the Form
    // ****************************************
    $("#reset-form-btn").click(function () {
        $("#customer_id").val("");
        clear_form_data();
        flash_message("Form reset");
    });

});
