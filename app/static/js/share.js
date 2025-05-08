function shareWith(email) {
    fetch('/api/share', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email })
    })
    .then(res => res.json())
    .then(data => {
      alert(data.message); 
      location.reload();
    });
  }
function shareWith(email) {
    fetch('/api/share', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email })
    })
    .then(res => res.json())
    .then(() => {
        window.location.href = '/share';
      });
  }

  function togglePreview(email) {
    document.querySelectorAll('[id^="preview-"]').forEach(row => row.classList.add('hidden'));
    const target = document.getElementById(`preview-${email}`);
    if (target) {
        target.classList.remove('hidden');
    }
}