const GOALS = {
  total: 12.3,
  travel: 2.9,
  home: 3.5,
  food: 3.1,
  shopping: 2.8
};

document.addEventListener('DOMContentLoaded', () => {
  // get the user's emissions summary data
  fetch('/api/emissions_summary')
    .then(res => res.json())
    .then(data => {
    const insights = {
      // Travel PCT Analysis
      travel: `
      ${data.travelTotal > GOALS.travel ? `
        <p class="text-[16px] text-gray-800 mt-2">
          🚗 Your travel-related carbon emissions exceed the recommended sustainable target.
          This elevated footprint may be due to high reliance on personal vehicles, frequent air travel, or limited use of public transit options.
        </p>
        <p class="text-[16px] text-gray-800 mt-2">
          Consider strategies such as reducing short-haul flights, combining trips to cut down car use, or adopting public transportation more regularly.
          Even modest adjustments in your commuting habits—like carpooling, walking for nearby errands, or choosing trains over planes—can collectively bring meaningful reductions.
        </p>
        <p class="text-[16px] text-gray-800 mt-2">
          Switching to more fuel-efficient or electric vehicles, and planning holidays with lower carbon transport modes, can also significantly lower your overall emissions.
        </p><br>
      ` : `
        <p class="text-[16px] text-gray-800 mt-2">
          🚗 Your travel-related emissions are currently within the recommended sustainable target.
          This suggests you are making conscious choices such as minimizing unnecessary car trips, flying less frequently, or incorporating low-carbon transport methods into your lifestyle.
        </p><br>
        <p class="text-[16px] text-gray-800 mt-2">
          Efficient commuting habits, such as using public transport, walking, cycling, or choosing fuel-efficient vehicles, are clearly contributing to this result.
        </p><br>
      `}

      <p class="text-[16px] text-gray-800 mt-2">
        🟢 Breakdown of your travel emissions: Car ${data.travel.carPct.toFixed(0)}%, Air ${data.travel.airPct.toFixed(0)}%, Transit ${data.travel.transitPct.toFixed(0)}%.
      </p>

      ${data.carPct > data.airPct && data.carPct > data.transitPct ? `
        <p class="text-[16px] text-gray-800 mt-2">
          Most of your travel emissions come from personal vehicle use. Consider reducing solo driving, carpooling, or switching to public transport or electric vehicles. Even minor changes like combining errands into a single trip can lower emissions significantly.
        </p><br>` : ''}

      ${data.airPct > data.carPct && data.airPct > data.transitPct ? `
        <p class="text-[16px] text-gray-800 mt-2">
          A large portion of your travel footprint is from air travel. Limiting short-haul flights, opting for trains when possible, and exploring verified carbon offset programs can help mitigate this impact.
        </p><br>` : ''}

      ${data.transitPct > data.carPct && data.transitPct > data.airPct ? `
        <p class="text-[16px] text-gray-800 mt-2">
          Your highest share comes from public transportation. This is already a low-emission travel choice—great job! To go further, try combining transit with walking or biking when possible.
        </p><br>` : ''}

      <ul class="list-disc pl-5 mt-2 text-[16px] text-gray-800">
        <li><strong>Car Emissions:</strong> Improve fuel efficiency or switch to electric vehicles.</li>
        <li><strong>Air Travel:</strong> Reduce flights and use verified carbon offset programs.</li>
        <li><strong>Public Transit:</strong> Choose low-emission buses or trains when possible.</li><br>
      </ul>
    `,
    
      // Home PCT Analysis
      home: `
      ${data.homeTotal > GOALS.home ? `
        <p class="text-[16px] text-gray-800 mt-2">
          🏠 Your home-related carbon emissions are above the recommended annual limit. This may be caused by high usage of electricity, natural gas, heating fuels, water, or emissions tied to your house’s construction.
        </p>
        <p class="text-[16px] text-gray-800 mt-2">
          Consider energy-efficient appliances, improved insulation, lower hot water usage, and reducing unnecessary renovations or expansions.
        </p><br>
      ` : `
        <p class="text-[16px] text-gray-800 mt-2">
          🏠 Your household emissions are well within sustainable levels. Great job! This reflects mindful use of electricity, water, and space.
        </p>
        <p class="text-[16px] text-gray-800 mt-2">
          Continue these responsible habits, and consider upgrades like solar panels or greywater systems for further impact.
        </p><br>
      `}

      <p class="text-[16px] text-gray-800 mt-2">
        🔵 Breakdown: Electricity ${data.home.electricityPct.toFixed(0)}%, Natural Gas ${data.home.naturalGasPct.toFixed(0)}%, Heating Fuel ${data.home.heatingFuelPct.toFixed(0)}%, Water ${data.home.waterPct.toFixed(0)}%, Construction ${data.home.constructionPct.toFixed(0)}%.
      </p>

      ${data.electricityPct > data.naturalGasPct && data.electricityPct > data.heatingFuelPct && data.electricityPct > data.waterPct && data.electricityPct > data.constructionPct ? `
        <p class="text-[16px] text-gray-800 mt-2">
          Electricity is your largest home emission source. Reduce usage during peak hours, switch off idle devices, and consider green electricity plans.
        </p><br>` : ''}

      ${data.naturalGasPct > data.electricityPct && data.naturalGasPct > data.heatingFuelPct && naturalGasPct >data.waterPct && data.naturalGasPct > constructionPct ? `
        <p class="text-[16px] text-gray-800 mt-2">
          Natural gas use is high. You can reduce emissions by improving insulation and using programmable thermostats to avoid overheating.
        </p><br>` : ''}

      ${data.heatingFuelPct > data.electricityPct && data.heatingFuelPct > data.naturalGasPct && data.heatingFuelPct > data.waterPct && data.heatingFuelPct > data.constructionPct ? `
        <p class="text-[16px] text-gray-800 mt-2">
          Heating fuels are a major contributor. Upgrading to more efficient systems or switching to cleaner fuels may help.
        </p><br>` : ''}

      ${data.waterPct > data.electricityPct && data.waterPct > data.naturalGasPct && data.waterPct > data.heatingFuelPct && data.waterPct > data.constructionPct ? `
        <p class="text-[16px] text-gray-800 mt-2">
          Water-related emissions are high. Consider shortening hot showers, using cold water for laundry, and installing water-saving devices.
        </p><br>` : ''}

      ${data.constructionPct > data.electricityPct && data.constructionPct > data.naturalGasPct && data.constructionPct > data.heatingFuelPct && data.constructionPct >data. waterPct ? `
        <p class="text-[16px] text-gray-800 mt-2">
          Construction emissions dominate your home profile. Avoid unnecessary remodeling, and consider sustainable materials when renovating.
        </p><br>` : ''}

      <ul class="list-disc pl-5 mt-2 text-[16px] text-gray-800">
        <li><strong>Electricity:</strong> Turn off idle devices, use efficient lighting, and monitor usage.</li>
        <li><strong>Natural Gas:</strong> Lower thermostat temps and insulate well.</li>
        <li><strong>Heating Fuel:</strong> Upgrade systems or reduce runtime.</li>
        <li><strong>Water:</strong> Use low-flow fixtures and reduce hot water needs.</li>
        <li><strong>Construction:</strong> Maintain your home carefully and renovate only when necessary.</li><br>
      </ul>
    `,

      // Food PCT Analysis
    food: `
    ${data.foodTotal > GOALS.food ? `
      <p class="text-[16px] text-gray-800 mt-2">
        🥩 Your food-related carbon emissions exceed the recommended sustainable target.
        This may be due to a high consumption of meat, particularly red meats like beef and lamb, dairy products such as cheese and milk, or frequent intake of highly processed snacks and ready-to-eat meals.
      </p>
      <p class="text-[16px] text-gray-800 mt-2">
        To improve this, consider reducing your intake of red meat and full-fat dairy products, incorporating more plant-based meals and ingredients like legumes, grains, and vegetables into your diet.
        Additionally, minimizing heavily packaged and ultra-processed foods—often high in emissions due to industrial manufacturing—can also contribute to lower overall carbon output.
      </p><br>
    ` : `
      <p class="text-[16px] text-gray-800 mt-2">
        🥦 Your food-related emissions are within the sustainable target range.
        This indicates that you likely maintain a balanced, climate-conscious diet with limited intake of high-emission items such as red meat, full-fat dairy, or ultra-processed foods.
      </p>
      <p class="text-[16px] text-gray-800 mt-2">
        To maintain or further reduce your food footprint, continue prioritizing plant-based choices, seasonal fruits and vegetables, and food items with minimal packaging.
        Supporting local and organic farming where possible can also help contribute to a more sustainable lifestyle.
      </p><br>
    `}

    <p class="text-[16px] text-gray-800 mt-2">
      🟡 Breakdown of your food emissions: Meat ${data.food.meatPct.toFixed(0)}%, Dairy ${data.food.dairyPct.toFixed(0)}%, Fruits & Vegetables ${data.food.fruitVegPct.toFixed(0)}%, Cereals ${data.food.cerealsPct.toFixed(0)}%, Snacks ${data.food.snacksPct.toFixed(0)}%.
      This breakdown highlights the dominant sources of your food-related carbon footprint and can guide your dietary adjustments moving forward.
    </p>

    ${data.meatPct > data.dairyPct && data.meatPct > data.fruitVegPct && data.meatPct > data.cerealsPct && data.meatPct > data.snacksPct ? `
      <p class="text-[16px] text-gray-800 mt-2">
        Meat is currently the largest contributor to your food-related carbon emissions.
        Consider reducing consumption of beef, lamb, or processed meats and replacing them with more climate-friendly alternatives such as lentils, tofu, tempeh, or beans.
        These options not only have a lower carbon footprint but also offer rich nutritional value.
      </p><br>` : ''}

    ${data.dairyPct > data.meatPct && data.dairyPct > data.fruitVegPct && data.dairyPct > data.cerealsPct && data.dairyPct > data.snacksPct ? `
      <p class="text-[16px] text-gray-800 mt-2">
        Dairy products appear to be the top source of your food emissions.
        Switching to plant-based alternatives like almond milk, soy milk, oat milk, or even coconut-based yogurts can significantly reduce your impact.
        Many of these alternatives are now widely available and offer comparable nutritional benefits.
      </p><br>` : ''}

    ${data.snacksPct > data.meatPct && data.snacksPct > data.dairyPct && data.snacksPct > data.fruitVegPct && data.snacksPct > data.cerealsPct ? `
      <p class="text-[16px] text-gray-800 mt-2">
        Processed snacks and convenience foods are a major contributor to your current food emissions.
        These products often involve high levels of packaging, transportation, and processing.
        Opting for whole foods, homemade meals, or items with less packaging can greatly reduce your snack-related carbon output.
      </p><br>` : ''}

    <ul class="list-disc pl-5 mt-2 text-[16px] text-gray-800">
      <li><strong>Reduce Meat:</strong> Replace red meats with plant-based proteins like beans, tofu, lentils, or seitan to lower emissions.</li>
      <li><strong>Dairy Alternatives:</strong> Switch to oat, almond, or soy-based milk and yogurt to cut back on dairy-related carbon output.</li>
      <li><strong>Snack Smart:</strong> Avoid highly processed and packaged snacks; choose fresh, bulk, or homemade alternatives when possible.</li><br>
    </ul>
  `,

    // Shopping PCT Analysis
    shopping: `
    ${data.shoppingTotal > GOALS.shopping ? `
      <p class="text-[16px] text-gray-800 mt-2">
        🛍️ Your shopping-related carbon emissions exceed the recommended sustainable target.
        This might be due to frequent purchases of items such as furniture, clothing, or service-based expenditures including online subscriptions, household services, or entertainment.
      </p>
      <p class="text-[16px] text-gray-800 mt-2">
        Consider reducing discretionary purchases, opting for longer-lasting or second-hand goods, and critically evaluating the necessity and frequency of recurring service costs such as memberships or delivery services.
      </p><br>
    ` : `
      <p class="text-[16px] text-gray-800 mt-2">
        🛒 Your shopping-related emissions are within the recommended sustainable range.
        This suggests that you're making mindful and conscious choices around consumption patterns, prioritizing necessity over indulgence, and likely limiting the use of high-emission services.
      </p>
      <p class="text-[16px] text-gray-800 mt-2">
        Maintaining this pattern by continuing to buy fewer but better-quality products, reusing where possible, and supporting ethical and sustainable service providers will help you keep your carbon impact low in the long term.
      </p><br>
    `}

    <p class="text-[16px] text-gray-800 mt-2">
      🟣 Breakdown of your shopping emissions: Furniture ${data.shopping.furniturePct.toFixed(0)}%, Clothing ${data.shopping.clothingPct.toFixed(0)}%, Other Goods ${data.shopping.otherGoodsPct.toFixed(0)}%, Services ${data.shopping.servicesPct.toFixed(0)}%.
      This breakdown helps you identify which specific areas contribute most to your shopping footprint, providing a clear direction for improvement.
    </p>

    ${data.furniturePct > data.clothingPct && data.furniturePct > data.otherGoodsPct && data.furniturePct > data.servicesPct ? `
      <p class="text-[16px] text-gray-800 mt-2">
        Furniture and household appliances are currently the largest contributors in your shopping emissions.
        These items tend to have higher embodied carbon due to manufacturing and transportation processes. Consider delaying non-essential upgrades, buying second-hand when possible, or choosing products certified as sustainable or eco-friendly.
      </p><br>` : ''}

    ${data.clothingPct > data.furniturePct && data.clothingPct > data.otherGoodsPct && data.clothingPct > data.servicesPct ? `
      <p class="text-[16px] text-gray-800 mt-2">
        Clothing makes up the largest portion of your shopping carbon footprint.
        Fast fashion, with its high turnover and waste, is a significant contributor. To reduce your impact, try supporting slow fashion brands, purchasing fewer but more durable pieces, and avoiding trends that encourage frequent replacement.
      </p><br>` : ''}

    ${data.servicesPct > data.furniturePct && data.servicesPct > data.clothingPct && data.servicesPct > data.otherGoodsPct ? `
      <p class="text-[16px] text-gray-800 mt-2">
        Services are currently the main source of your shopping-related emissions.
        This includes everything from entertainment subscriptions to professional services and delivery-based conveniences. Audit your recurring payments and service contracts to identify areas where reductions or more sustainable alternatives are possible.
      </p><br>` : ''}

    <ul class="list-disc pl-5 mt-2 text-[16px] text-gray-800">
      <li><strong>Furniture:</strong> Opt for second-hand, refurbished, or sustainably-made furnishings to reduce embodied carbon and landfill waste.</li>
      <li><strong>Clothing:</strong> Avoid fast fashion trends, focus on high-quality wardrobe staples, and consider swapping or thrifting clothes.</li>
      <li><strong>Services:</strong> Regularly review subscriptions, especially those with high data or energy usage, and look for greener alternatives.</li><br>
    </ul>
  `,

    };
      // Populate the tab content with the insights
      document.getElementById('tabContent0').innerHTML = `<div>${insights.travel}</div>`;
      document.getElementById('tabContent1').innerHTML = `<div>${insights.home}</div>`;
      document.getElementById('tabContent2').innerHTML = `<div>${insights.food}</div>`;
      document.getElementById('tabContent3').innerHTML = `<div>${insights.shopping}</div>`;
    })
    .catch(err => console.error('Error loading emissions summary:', err));
});

fetch('/api/emissions_summary')
  .then(res => res.json())
  .then(data => {
    const categoryTotals = {
      Travel: data.travelTotal,
      Food: data.foodTotal,
      Home: data.homeTotal,
      Shopping: data.shoppingTotal
    };

    const total = Object.values(categoryTotals).reduce((a, b) => a + b, 0);
    const sortedCategories = Object.entries(categoryTotals).sort((a, b) => b[1] - a[1]);

    const highestCategory = sortedCategories[0][0];
    const secondCategory = sortedCategories[1][0];

    let intro = '';
    if (total > GOALS.total) {
      intro = `Your total carbon footprint this month is ${total.toFixed(2)} kg CO₂eq, which exceeds the recommended limit of ${GOALS.total} kg. This indicates a need for improvement in your consumption habits.`;
    } else {
      intro = `Your total footprint is ${total.toFixed(2)} kg CO₂eq, which is within the sustainable range. Still, let’s explore where small improvements can be made.`;
    }

    const suggestionsMap = {
      Food: "🍽️ Food is currently your largest emission category. Reducing red meat, dairy, and processed snacks — and cutting food waste — can make a big difference.",
      Travel: "🚗 Travel ranks high among your emissions. Consider more sustainable transport options like walking, cycling, or carpooling, and reduce short-distance flights.",
      Home: "🏠 Home-related emissions are significant. Focus on using energy-efficient appliances, reducing water usage, and improving insulation to save energy.",
      Shopping: "🛍️ Shopping is a major contributor. Reducing fast fashion, buying second-hand items, and cutting back on unnecessary goods can reduce your impact."
    };

    const summaryAdvice = `
      <p class="text-sm text-gray-700 mt-1">${intro}</p>
      <p class="text-sm text-gray-700 mt-2">${suggestionsMap[highestCategory]}</p>
      <p class="text-sm text-gray-700 mt-2">${suggestionsMap[secondCategory]}</p>
      <p class="text-sm text-gray-700 mt-2">🎯 Focus on these areas first to see the biggest improvements in your overall sustainability.</p>
    `;

    document.querySelector('#suggestions').innerHTML = `
      <h3 class="font-bold text-[#16372c] text-base">What you can do about it</h3>
      ${summaryAdvice}
    `;
  });
