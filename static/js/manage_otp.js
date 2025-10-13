
    let generatedOtp = null;
    let otpExpiryTime = null;
    let otpTimer = null;
    let resendCountdown = null;
    let resendTimer = null;

    const modal = document.getElementById("otpModal");
    const body = document.body;
    const resendBtn = document.getElementById("resendBtn");

    function startResendCountdown() {
      let remaining = 30;
      resendBtn.disabled = true;
      resendBtn.textContent = `Resend OTP (30s)`;

      resendTimer = setInterval(() => {
        remaining--;
        resendBtn.textContent = `Resend OTP (${remaining}s)`;
        if (remaining <= 0) {
          clearInterval(resendTimer);
          resendBtn.disabled = false;
          resendBtn.textContent = "Resend OTP";
        }
      }, 1000);
    }

    async function sendOtp(phone) {
      generatedOtp = Math.floor(100000 + Math.random() * 900000).toString();
      otpExpiryTime = Date.now() + 5 * 60 * 1000;

      try {
        await fetch("/send_otp", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ phone, otp: generatedOtp })
        });
      } catch (err) {
        alert("Failed to send OTP. Check backend logs.");
        return false;
      }

      document.getElementById("otpInfo").textContent = `OTP sent to ${phone}. Valid for 5 minutes.`;
      document.getElementById("statusMsg").textContent = "";
      startResendCountdown();

      if (otpTimer) clearInterval(otpTimer);
      otpTimer = setInterval(() => {
        if (Date.now() > otpExpiryTime) {
          clearInterval(otpTimer);
          document.getElementById("statusMsg").textContent = "❌ OTP expired. Please resend.";
          document.getElementById("statusMsg").style.color = "red";
        }
      }, 1000);

      return true;
    }

    document.getElementById("sendOtpBtn").onclick = async () => {
      const phone = document.getElementById("phone").value.trim();
      if (!phone) {
        alert("Please enter a valid mobile number");
        return;
      }
      // Check: only digits and exactly 10 characters
      if (!/^\d{10}$/.test(phone)) {
         alert("Please enter a valid 10-digit mobile number.");
         return;
      }
      // Prepend +91
      const fullNumber = "+91" + phone;
//      alert("Formatted number: " + fullNumber);

      const ok = await sendOtp(fullNumber);
      if (ok) {
        modal.style.display = "flex";
        body.classList.add("modal-open");
      }
    };

    resendBtn.onclick = async () => {
      const phone = document.getElementById("phone").value.trim();
      const fullNumber = "+91" + phone;
      const ok = await sendOtp(fullNumber);
      if (ok) {
        document.getElementById("statusMsg").textContent = "🔄 OTP resent successfully!";
        document.getElementById("statusMsg").style.color = "green";
      }
    };

    document.getElementById("verifyOtpBtn").onclick = () => {
      const entered = document.getElementById("otpInput").value.trim();
      const msg = document.getElementById("statusMsg");

      if (Date.now() > otpExpiryTime) {
        msg.textContent = "❌ OTP expired. Please resend.";
        msg.style.color = "red";
        return;
      }

      if (entered === generatedOtp) {
        msg.textContent = "✅ OTP verified successfully!";
        msg.style.color = "green";
        clearInterval(otpTimer);
        clearInterval(resendTimer);

        setTimeout(() => {
          modal.style.display = "none";
          body.classList.remove("modal-open");
//          alert("Proceeding to next step...");
          window.location.href = "/register_user";
        }, 1200);
      } else {
        msg.textContent = "Invalid OTP. Please try again.";
        msg.style.color = "red";
      }
    };

    document.getElementById("cancelBtn").onclick = () => {
      if (confirm("Cancel verification and return to home?")) {
        clearInterval(otpTimer);
        clearInterval(resendTimer);
        modal.style.display = "none";
        body.classList.remove("modal-open");
//        alert("Returning to home screen...");
        window.location.href = "/home.html";
      }
    };


