/**
 * rest_api.js – Client-side helpers for the Customer Administration UI
 *
 * Placeholder stubs for CRUD operations against the Customer REST API.
 * Wire up full implementations when the UI feature is built out.
 */

const BASE_URL = "/customers";

/** Show a flash message at the bottom of the page */
function flash(message, type = "info") {
  const el = document.getElementById("flash-message");
  el.textContent = message;
  el.className = `flash ${type}`;
  setTimeout(() => { el.className = "flash hidden"; }, 4000);
}

/** Populate the results table from an array of customer objects */
function populateTable(customers) {
  const tbody = document.getElementById("results-body");
  tbody.innerHTML = "";
  customers.forEach((c) => {
    const row = tbody.insertRow();
    row.insertCell().textContent = c.id;
    row.insertCell().textContent = c.name;
    row.insertCell().textContent = c.address;
    row.insertCell().textContent = c.status;
    row.addEventListener("click", () => fillForm(c));
  });
}

/** Fill the detail form with a selected customer */
function fillForm(customer) {
  document.getElementById("customer_id").value      = customer.id;
  document.getElementById("customer_name").value    = customer.name;
  document.getElementById("customer_address").value = customer.address;
  document.getElementById("customer_status").value  = customer.status;
}

/** Clear the detail form */
function clearForm() {
  document.getElementById("customer-form").reset();
  document.getElementById("customer_id").value = "";
}

// ---------------------------------------------------------------------------
// Event listeners (stubs – full implementation pending)
// ---------------------------------------------------------------------------

document.getElementById("search-btn").addEventListener("click", () => {
  flash("Search not yet implemented", "info");
});

document.getElementById("clear-btn").addEventListener("click", () => {
  document.getElementById("search_id").value   = "";
  document.getElementById("search_name").value = "";
  document.getElementById("results-body").innerHTML = "";
  clearForm();
});

document.getElementById("create-btn").addEventListener("click", () => {
  flash("Create not yet implemented", "info");
});

document.getElementById("update-btn").addEventListener("click", () => {
  flash("Update not yet implemented", "info");
});

document.getElementById("delete-btn").addEventListener("click", () => {
  flash("Delete not yet implemented", "info");
});

document.getElementById("retrieve-btn").addEventListener("click", () => {
  flash("Retrieve not yet implemented", "info");
});
