
function copyPrompt() {
  const ta = document.getElementById('prompt');
  const btn = document.getElementById('copyBtn');
  const original = btn.textContent;
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(ta.value).then(() => {
      btn.textContent = "✓ Copied";
      setTimeout(() => { btn.textContent = original; }, 1500);
    });
  } else {
    // Fallback without alert: use execCommand silently
    ta.select();
    ta.setSelectionRange(0, 999999);
    document.execCommand('copy');
    btn.textContent = "✓ Copied";
    setTimeout(() => { btn.textContent = original; }, 1500);
  }
}
