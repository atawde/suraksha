  // same tab-switching JS
  (function(){
    const tabsEl = document.getElementById('tabs');
    if (!tabsEl) return;
    const tabs = Array.from(tabsEl.querySelectorAll('[role="tab"]'));
    const panels = tabs.map(t => document.getElementById(t.getAttribute('aria-controls')));

    function activateTab(newTab){
      tabs.forEach(t => { t.setAttribute('aria-selected','false'); t.setAttribute('tabindex','-1'); });
      panels.forEach(p => { p.hidden = true; p.classList.remove('active'); });

      newTab.setAttribute('aria-selected','true');
      newTab.setAttribute('tabindex','0');
      const panel = document.getElementById(newTab.getAttribute('aria-controls'));
      panel.hidden = false;
      panel.classList.add('active');
      newTab.focus();
    }

    tabs.forEach(t => t.addEventListener('click', () => activateTab(t)));
    tabs.forEach((t, idx) => {
      t.addEventListener('keydown', (e) => {
        const key = e.key;
        let newIndex = null;
        if (key === 'ArrowRight' || key === 'ArrowDown') newIndex = (idx + 1) % tabs.length;
        else if (key === 'ArrowLeft' || key === 'ArrowUp') newIndex = (idx - 1 + tabs.length) % tabs.length;
        else if (key === 'Home') newIndex = 0;
        else if (key === 'End') newIndex = tabs.length - 1;
        if (newIndex !== null){ e.preventDefault(); activateTab(tabs[newIndex]); }
      });
    });
  })();

function setupDocumentUpload(groupName, uploadDivId, fileInputId, buttonId, statusId, uploadUrl) {
  // Show upload section when a radio is selected
  document.querySelectorAll(`input[name="${groupName}"]`).forEach(radio => {
    radio.addEventListener('change', () => {
      document.getElementById(uploadDivId).classList.remove('hidden');
    });
  });

  const fileInput = document.getElementById(fileInputId);
  const uploadBtn = document.getElementById(buttonId);
  const status = document.getElementById(statusId);

  // Enable upload button when a file is chosen
  fileInput.addEventListener('change', () => {
    uploadBtn.disabled = !fileInput.files.length;
  });

  // Handle upload
  uploadBtn.addEventListener('click', async () => {
    const file = fileInput.files[0];
    const selectedDoc = document.querySelector(`input[name="${groupName}"]:checked`).value;

    if (!file) {
      status.textContent = "Please select a file first.";
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("doc_type", selectedDoc);

    status.textContent = "Uploading...";

    try {
      const response = await fetch(uploadUrl, {
        method: "POST",
        body: formData
      });

      if (response.ok) {
        status.textContent = "✅ Upload successful!";
        fileInput.value = "";
        uploadBtn.disabled = true;
      } else {
        status.textContent = "❌ Upload failed!";
      }
    } catch (err) {
      console.error(err);
      status.textContent = "⚠️ Error uploading file.";
    }
  });
}

// Initialize upload handlers for both groups
setupDocumentUpload("vehicle_doc", "vehicle-upload", "vehicle-file", "upload-vehicle-btn", "vehicle-status", "/upload");
setupDocumentUpload("personal_doc", "personal-upload", "personal-file", "upload-personal-btn", "personal-status", "/upload");

document.getElementById('mainForm').addEventListener('submit', function() {
  const btn = document.getElementById('submitBtn');
  btn.classList.add('loading');
  btn.textContent = "Submitting...";
});
