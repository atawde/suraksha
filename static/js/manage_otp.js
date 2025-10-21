let generatedOTP = null;
let otpSentTime = null;
let resendTimer = null;
let resendCountdown = 10; // seconds before resend is allowed

const sendBtn = document.getElementById('sendOtpBtn');
const resendBtn = document.getElementById('resendBtn');
const cancelBtn = document.getElementById('cancelBtn');
const verifyBtn = document.getElementById('verifyBtn');
const message = document.getElementById('message');
const error = document.getElementById('error');
const timer = document.getElementById('timer');
const otpSection = document.getElementById('otp-section');
const mobileInput = document.getElementById('mobile');

async function sendOtp() {
  const mobile = mobileInput.value.trim();
  message.textContent = '';
  error.textContent = '';

//  if (!mobile.startsWith('+') || mobile.length < 10) {
//    error.textContent = 'Please enter a valid mobile number with country code.';
//    return;
//  }

  // Generate OTP
  generatedOTP = Math.floor(100000 + Math.random() * 900000);
  otpSentTime = Date.now();
  console.log("Generated OTP:", generatedOTP); // for testing

  // Call backend Twilio API
  try {
    const response = await fetch('/send_otp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phone: mobile, otp: generatedOTP })
    });
    const data = await response.json();

    if (data.new_user_required) {
      // redirect to registration page
      window.location.href = '/new_user';
      return;
    }

    if (data.success) {
      message.textContent = 'OTP sent successfully! Please check your SMS.';
      otpSection.style.display = 'block';
      startResendTimer();
    } else {
      error.textContent = 'Error sending OTP: ' + data.error;
    }
  } catch (e) {
    error.textContent = 'Network error: ' + e.message;
  }
}

// Verify OTP
function verifyOtp() {
  const enteredOtp = document.getElementById('otpInput').value.trim();
  message.textContent = '';
  error.textContent = '';

  if (!generatedOTP) {
    error.textContent = 'Please generate an OTP first.';
    return;
  }

  // Expiry check (5 mins)
  if (Date.now() - otpSentTime > 5 * 60 * 1000) {
    error.textContent = 'OTP expired. Please request a new one.';
    generatedOTP = null;
    return;
  }

  if (enteredOtp === generatedOTP.toString()) {
    message.textContent = '✅ OTP Verified Successfully!';
    error.textContent = '';
    document.getElementById('verifyBtn').disabled = true;
    // Redirect after 5 seconds
    setTimeout(() => {
      window.location.href = '/';  // redirect to home page
    }, 5000);
  } else {
    error.textContent = '❌ Incorrect OTP. Please try again.';
  }
}

// Timer for enabling resend button
function startResendTimer() {
  resendCountdown = 10;
  resendBtn.disabled = true;
  resendBtn.style.display = 'inline';
  timer.textContent = `Try again in ${resendCountdown}s`;

  clearInterval(resendTimer);
  resendTimer = setInterval(() => {
    resendCountdown--;
    if (resendCountdown > 0) {
      timer.textContent = `Try again in ${resendCountdown}s`;
    } else {
      clearInterval(resendTimer);
      timer.textContent = '';
      resendBtn.disabled = false;
    }
  }, 1000);
}

// Cancel -> Go back home
cancelBtn.addEventListener('click', () => {
  window.location.href = '/'; // adjust as per your route
});

// Event bindings
sendBtn.addEventListener('click', sendOtp);
resendBtn.addEventListener('click', sendOtp);
verifyBtn.addEventListener('click', verifyOtp);

function validateMobile() {
//        document.getElementById("submitBtn").onclick = async () => {
      const phone = document.getElementById("mobile").value.trim();
      if (!phone) {
        alert("Please enter a valid mobile number");
        return;
      }
      // Check: only digits and exactly 10 characters
      if (!/^\d{10}$/.test(phone)) {
         alert("Please enter a valid 10-digit mobile number.");
         return;
      }
    }

