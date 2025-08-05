      document.addEventListener("DOMContentLoaded", function () {
      const status = document.getElementById("status");
      const spinner = document.getElementById("spinner");
      const modal = document.getElementById("paymentModal");
      const modalTitle = document.getElementById("modalTitle");
      const modalMessage = document.getElementById("modalMessage");
      const modalGif = document.getElementById("modalGif");

      const successGif = modal.getAttribute("data-success-url");
      const failedGif = modal.getAttribute("data-failed-url");

      function showStatus(message, type) {
        status.textContent = message;
        status.className = type;
        status.style.display = "block";
      }
      function showSpinner(show) { spinner.style.display = show ? "block" : "none"; }
      function showModal(title, htmlContent, isSuccess) {
        modalTitle.textContent = title;
        modalGif.src = (isSuccess ? successGif : failedGif) + "?t=" + Date.now();
        modalMessage.innerHTML = htmlContent;
        modal.style.display = "block";
      }
      window.closeModal = () => modal.style.display = "none";

      function pollPayment(checkoutID, phone, amount) {
        let attempts = 0;
        const interval = setInterval(() => {
          fetch("/results/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ CheckoutRequestID: checkoutID }),
          })
            .then(res => res.json())
            .then(result => {
              const resultCode = (result.ResultCode || result.result_code)?.toString();
              const txn = result.transaction_details || {};
              attempts++;

              if (resultCode === "0") {
                clearInterval(interval);
                showSpinner(false);
                showStatus("Payment Successful!", "success");
                showModal("Payment Successful", `
                  <p><strong>Transaction ID:</strong> ${txn.TransactionID || "N/A"}</p>
                  <p><strong>Amount:</strong> KES ${txn.Amount || amount}</p>
                  <p><strong>Phone:</strong> ${txn.PhoneNumber || phone}</p>
                  <p><strong>Date:</strong> ${txn.TransactionDate || "N/A"}</p>
                `, true);
              } else if (attempts >= 2) { // stop after ~30s
                clearInterval(interval);
                showSpinner(false);
                const msg = result.ResultDesc || result.result_desc || "User did not enter anything or cancelled the transaction.";
                showStatus(msg, "error");
                showModal("Payment Failed", `<p>${msg}</p>`, false);
              }
            })
            .catch(err => {
              clearInterval(interval);
              showSpinner(false);
              showStatus("Error: " + err.message, "error");
              showModal("Error", `<p>${err.message}</p>`, false);
            });
        }, 5000); // poll every 5s
      }

      window.initiatePayment = function (event) {
        event.preventDefault();
        let phone = document.getElementById("phone").value.trim();
        const amount = document.getElementById("amount").value;

        if (!phone || !amount) {
          showStatus("Please fill in both phone and amount.", "error");
          return;
        }
        if (phone.startsWith("07")) phone = "254" + phone.slice(1);

        showStatus("Initiating payment...", "success");
        showSpinner(true);

        fetch("/stk/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ phone, amount }),
        })
          .then(res => res.json())
          .then(data => {
            if (data.CheckoutRequestID) {
              showStatus("Waiting for confirmation...", "success");
              pollPayment(data.CheckoutRequestID, phone, amount);
            } else {
              showSpinner(false);
              const msg = data.error || "Failed to initiate payment.";
              showStatus(msg, "error");
              showModal("Payment Failed", `<p>${msg}</p>`, false);
            }
          })
          .catch(err => {
            showSpinner(false);
            showStatus("Network error: " + err.message, "error");
            showModal("Network Error", `<p>${err.message}</p>`, false);
          });
      };
    });
    document.addEventListener("DOMContentLoaded", function() {
      const doneBtn = document.getElementById("doneBtn");
  
      if (doneBtn) {
          doneBtn.addEventListener("click", function() {
              // Close modal
              const modal = document.querySelector("#paymentModal");
              if (modal) {
                  modal.style.display = "none";
              }
  
              // Refresh page
              location.reload();
          });
      }
  });

