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
        </p>
        <p class="text-[16px] text-gray-800 mt-2">
          Efficient commuting habits, such as using public transport, walking, cycling, or choosing fuel-efficient vehicles, are clearly contributing to this result.
        </p><br>
      `}

      <p class="text-[16px] text-gray-800 mt-2">
        Breakdown of your travel emissions: Car ${data.travel.carPct.toFixed(0)}%, Air ${data.travel.airPct.toFixed(0)}%, Transit ${data.travel.transitPct.toFixed(0)}%.
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
        Breakdown: Electricity ${data.home.electricityPct.toFixed(0)}%, Natural Gas ${data.home.naturalGasPct.toFixed(0)}%, Heating Fuel ${data.home.heatingFuelPct.toFixed(0)}%, Water ${data.home.waterPct.toFixed(0)}%, Construction ${data.home.constructionPct.toFixed(0)}%.
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
          This may be due to a high consumption of meat, dairy, or processed snacks.
        </p>
        <p class="text-[16px] text-gray-800 mt-2">
          Consider reducing intake of red meat and dairy, and incorporating more plant-based meals into your diet.
          Minimizing heavily packaged or processed foods can also contribute to lower emissions.
        </p><br>
      ` : `
        <p class="text-[16px] text-gray-800 mt-2">
          🥦 Your food-related emissions are within the sustainable target range.
          This indicates a balanced diet with limited high-emission items like red meat and dairy.
        </p>
        <p class="text-[16px] text-gray-800 mt-2">
          Continue choosing plant-based options, seasonal produce, and low-packaging items to maintain or further reduce your food footprint.
        </p><br>
      `}

      <p class="text-[16px] text-gray-800 mt-2">
        Breakdown of your food emissions: Meat ${data.food.meatPct.toFixed(0)}%, Dairy ${data.food.dairyPct.toFixed(0)}%, Fruits & Vegetables ${data.food.fruitVegPct.toFixed(0)}%, Cereals ${data.food.cerealsPct.toFixed(0)}%, Snacks ${data.food.snacksPct.toFixed(0)}%.
      </p>

      ${data.meatPct > data.dairyPct && data.meatPct > data.fruitVegPct && data.meatPct > data.cerealsPct && data.meatPct > data.snacksPct ? `
        <p class="text-[16px] text-gray-800 mt-2">
          Meat is the largest contributor to your food emissions. Reducing beef or lamb and replacing them with legumes, tofu, or plant proteins can significantly lower your impact.
        </p><br>` : ''}

      ${data.dairyPct > data.meatPct && data.dairyPct > data.fruitVegPct && data.dairyPct > data.cerealsPct && data.dairyPct > data.snacksPct ? `
        <p class="text-[16px] text-gray-800 mt-2">
          Dairy products contribute the most to your food emissions. Try plant-based alternatives like almond, oat, or soy milk to reduce this footprint.
        </p><br>` : ''}

      ${data.snacksPct > data.meatPct && data.snacksPct > data.dairyPct && data.snacksPct > data.fruitVegPct && data.snacksPct > data.cerealsPct ? `
        <p class="text-[16px] text-gray-800 mt-2">
          Processed snacks are a major source of your food emissions. Choosing whole foods and reducing packaging waste can make a big difference.
        </p><br>` : ''}

      <ul class="list-disc pl-5 mt-2 text-[16px] text-gray-800">
        <li><strong>Reduce Meat:</strong> Choose plant-based proteins like legumes or tofu.</li>
        <li><strong>Dairy Alternatives:</strong> Use soy, oat, or almond milk to lower impact.</li>
        <li><strong>Snack Smart:</strong> Minimize processed, packaged foods.</li><br>
      </ul>
    `,

      // Shopping PCT Analysis
      shopping: `
        ${data.shoppingTotal > GOALS.shopping ? `
          <p class="text-[16px] text-gray-800 mt-2">
            🛍️ Your shopping-related carbon emissions exceed the recommended sustainable target.
            This might be due to frequent purchases of furniture, clothing, or usage of service-based expenditures.
          </p>
          <p class="text-[16px] text-gray-800 mt-2">
            Consider reducing discretionary purchases, choosing second-hand or more durable goods, and evaluating the necessity of recurring service costs.
          </p><br>
        ` : `
          <p class="text-[16px] text-gray-800 mt-2">
            🛒 Your shopping-related emissions are within the recommended sustainable range.
            This suggests that you're making mindful choices around consumption and services.
          </p>
          <p class="text-[16px] text-gray-800 mt-2">
            Maintaining this pattern by buying less but better-quality products and supporting sustainable service providers will help keep your impact low.
          </p><br>
        `}

        <p class="text-[16px] text-gray-800 mt-2">
          Breakdown of your shopping emissions: Furniture ${data.shopping.furniturePct.toFixed(0)}%, Clothing ${data.shopping.clothingPct.toFixed(0)}%, Other Goods ${data.shopping.otherGoodsPct.toFixed(0)}%, Services ${data.shopping.servicesPct.toFixed(0)}%.
        </p>

        ${data.furniturePct > data.clothingPct && data.furniturePct > data.otherGoodsPct && data.furniturePct > data.servicesPct ? `
          <p class="text-[16px] text-gray-800 mt-2">
            Furniture and appliances are the largest contributors in your shopping emissions. Consider buying second-hand, choosing longer-lasting products, or delaying non-essential upgrades.
          </p><br>` : ''}

        ${data.clothingPct > data.furniturePct && data.clothingPct > data.otherGoodsPct && data.clothingPct > data.servicesPct ? `
          <p class="text-[16px] text-gray-800 mt-2">
            Clothing makes up the largest part of your shopping footprint. Try reducing fast fashion purchases, supporting sustainable brands, and buying higher-quality pieces less frequently.
          </p><br>` : ''}

        ${data.servicesPct > data.furniturePct && data.servicesPct > data.clothingPct && data.servicesPct > data.otherGoodsPct ? `
          <p class="text-[16px] text-gray-800 mt-2">
            Services are your main source of shopping emissions. Review any non-essential subscriptions or high-emission services to find opportunities for reduction.
          </p><br>` : ''}

        <ul class="list-disc pl-5 mt-2 text-[16px] text-gray-800">
          <li><strong>Furniture:</strong> Opt for second-hand or sustainably-made furnishings.</li>
          <li><strong>Clothing:</strong> Avoid fast fashion and favor quality over quantity.</li>
          <li><strong>Services:</strong> Review subscriptions or service plans with high emissions.</li><br>
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
