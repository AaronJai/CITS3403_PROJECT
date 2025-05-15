// Fetch live environmental news
  document.addEventListener("DOMContentLoaded", function () {
    fetch("https://api.rss2json.com/v1/api.json?rss_url=http://feeds.bbci.co.uk/news/science_and_environment/rss.xml")
      .then((res) => res.json())
      .then((data) => {
        const news = data.items.slice(0, 4).map((item) => {
          let thumbnail = item.thumbnail ? item.thumbnail : "https://cdn-icons-png.flaticon.com/512/2909/2909594.png";
          return `
            <div class="bg-white p-4 rounded-lg shadow mb-4 zoom flex">
              <a href="${item.link}" target="_blank" class="text-xl font-bold text-green-900 hover:underline">
                <img src="${thumbnail}" alt="News Thumbnail" class="w-24 h-24 object-cover rounded-lg mr-4 flex-shrink-0">
              </a>
              <div class="flex flex-col">
                <a href="${item.link}" target="_blank" class="text-xl font-bold text-green-900 hover:underline">
                ${item.title}
                </a>
                <p class="text-sm text-gray-600 mt-1">${new Date(item.pubDate).toLocaleDateString()}</p>
                <p class="text-gray-700 mt-2 leading-relaxed">${item.description.split(" ").slice(0, 25).join(" ")}...</p>
              </div>
            </div>
          `}).join("");

        document.getElementById("news-feed").innerHTML = news;
      });
  });