// Share carbon emissions data with user
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

// Generate a preview card for the shared user
function generatePreviewCard({ name, email, travel_pct, food_pct, home_pct, shopping_pct, total_emission }) {
  return `
<tr id="preview-${email}">
  <td colspan="5">
    <section class="mt-2">
      <div class="bg-white p-4 rounded-md">
        <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
          <div class="flex items-center mb-4">
            <img src="/static/assets/images/avatar.png" alt="Avatar"
                class="w-10 h-10 rounded-full mr-3" />
            <div>
              <p class="font-semibold">${name}</p>
              <p class="text-gray-500 text-sm hidden md:block">${email}</p>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4">
            ${['Travel', 'Home', 'Food', 'Shopping'].map((label, i) => {
              const percent = [travel_pct, home_pct, food_pct, shopping_pct][i];
              return `
              <div class="bg-white p-3 rounded-md shadow-sm">
                <h3 class="font-semibold">${label}</h3>
                <div class="mt-2 h-2 bg-gray-200 rounded-full">
                  <div class="h-2 bg-primary rounded-full" style="width: ${percent}%"></div>
                </div>
                <p class="text-sm text-gray-600 mt-1"><strong>${percent}%</strong> of their carbon budget</p>
              </div>`;
            }).join('')}
          </div>
          <p class="mt-4 text-sm font-semibold text-center">
            Total: <span class="text-primary">${total_emission.toFixed(2)}kg CO2eq</span> this month
          </p>
        </div>
      </div>
    </section>
  </td>
</tr>
  `;
}

// Load shared user emissions and display them in a preview card
function loadSharedUserEmissions(email) {
  fetch(`/api/emissions/${email}`)
    .then(res => res.json())
    .then(data => {
      document.querySelectorAll('[id^="preview-"]').forEach(row => row.remove());

      const previewHtml = generatePreviewCard({
        name: data.name || 'Unknown',
        email,
        travel_pct: data.travel_pct,
        food_pct: data.food_pct,
        home_pct: data.home_pct,
        shopping_pct: data.shopping_pct,
        total_emission: data.total_emissions
      });

      const userRow = document.querySelector(`tr[data-email="${email}"]`);
      if (userRow) {
        userRow.insertAdjacentHTML('afterend', previewHtml);
      }
    })
    .catch(error => {
      console.error('Error loading shared emissions:', error);
    });
}
