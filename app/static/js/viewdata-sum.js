const GOALS = {
  total: 12.3,
  travel: 2.9,
  home: 3.5,
  food: 3.1,
  shopping: 2.8
};
document.addEventListener('DOMContentLoaded', () => {
  fetch('/api/emissions', {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
  })
    .then(response => {
      if (!response.ok) throw new Error('Fetch error');
      return response.json();
    })
    .then(data => {
      const car = data.car_emissions || 0;
      const air = data.air_travel_emissions || 0;
      const transit = data.public_transit_emissions || 0;
      const travelTotal = car + air + transit;

      const electricity = data.electricity_emissions || 0;
      const naturalGas = data.natural_gas_emissions || 0;
      const heatingFuel = data.heating_fuels_emissions || 0;
      const water = data.water_emissions || 0;
      const construction = data.construction_emissions || 0;
      const homeTotal = electricity + naturalGas + heatingFuel + water + construction;

      const meat = data.meat_emissions || 0;
      const dairy = data.dairy_emissions || 0;
      const fruitVeg = data.fruits_vegetables_emissions || 0;
      const cereals = data.cereals_emissions || 0;
      const snacks = data.snacks_emissions || 0;
      const foodTotal = meat + dairy + fruitVeg + cereals + snacks;

      const furniture = data.furniture_emissions || 0;
      const clothing = data.clothing_emissions || 0;
      const otherGoods = data.other_goods_emissions || 0;
      const services = data.services_emissions || 0;
      const shoppingTotal = furniture + clothing + otherGoods + services;

      insertCategoryInsights(
        travelTotal, homeTotal, foodTotal, shoppingTotal,
        car, air, transit,
        electricity, naturalGas, heatingFuel, water, construction,
        meat, dairy, fruitVeg, cereals, snacks, 
        furniture, clothing, otherGoods, services
      );
    })
    .catch(err => console.error('Emissions fetch error:', err));
});


function insertCategoryInsights(travelTotal, homeTotal, foodTotal, shoppingTotal, 
  car, air, transit, 
  electricity, naturalGas, heatingFuel, water, construction,
  meat, dairy, fruitVeg, cereals, snacks,
  furniture, clothing, otherGoods, services) 
{
  const total = car + air + transit;
  const safeTotal = total === 0 ? 1 : total;

  const airPct = (air / safeTotal) * 100;
  const carPct = (car / safeTotal) * 100;
  const transitPct = (transit / safeTotal) * 100;

  const safeHomeTotal = homeTotal === 0 ? 1 : homeTotal;
  const electricityPct = (electricity / safeHomeTotal) * 100;
  const naturalGasPct = (naturalGas / safeHomeTotal) * 100;
  const heatingFuelPct = (heatingFuel / safeHomeTotal) * 100;
  const waterPct = (water / safeHomeTotal) * 100;
  const constructionPct = (construction / safeHomeTotal) * 100;

  const safeFoodTotal = foodTotal === 0 ? 1 : foodTotal;
  const meatPct = (meat / safeFoodTotal) * 100;
  const dairyPct = (dairy / safeFoodTotal) * 100;
  const fruitVegPct = (fruitVeg / safeFoodTotal) * 100;
  const cerealsPct = (cereals / safeFoodTotal) * 100;
  const snacksPct = (snacks / safeFoodTotal) * 100;

  const safeShoppingTotal = shoppingTotal === 0 ? 1 : shoppingTotal;
  const furniturePct = (furniture / safeShoppingTotal) * 100;
  const clothingPct = (clothing / safeShoppingTotal) * 100;
  const otherGoodsPct = (otherGoods / safeShoppingTotal) * 100;
  const servicesPct = (services / safeShoppingTotal) * 100;

  const insights = {
    // Travel PCT Analysis
    travel: `
    ${travelTotal > GOALS.travel ? `
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
      Breakdown of your travel emissions: Car ${carPct.toFixed(0)}%, Air ${airPct.toFixed(0)}%, Transit ${transitPct.toFixed(0)}%.
    </p>

    ${carPct > airPct && carPct > transitPct ? `
      <p class="text-[16px] text-gray-800 mt-2">
        Most of your travel emissions come from personal vehicle use. Consider reducing solo driving, carpooling, or switching to public transport or electric vehicles. Even minor changes like combining errands into a single trip can lower emissions significantly.
      </p><br>` : ''}

    ${airPct > carPct && airPct > transitPct ? `
      <p class="text-[16px] text-gray-800 mt-2">
        A large portion of your travel footprint is from air travel. Limiting short-haul flights, opting for trains when possible, and exploring verified carbon offset programs can help mitigate this impact.
      </p><br>` : ''}

    ${transitPct > carPct && transitPct > airPct ? `
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
    ${homeTotal > GOALS.home ? `
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
      Breakdown: Electricity ${electricityPct.toFixed(0)}%, Natural Gas ${naturalGasPct.toFixed(0)}%, Heating Fuel ${heatingFuelPct.toFixed(0)}%, Water ${waterPct.toFixed(0)}%, Construction ${constructionPct.toFixed(0)}%.
    </p>

    ${electricityPct > naturalGasPct && electricityPct > heatingFuelPct && electricityPct > waterPct && electricityPct > constructionPct ? `
      <p class="text-[16px] text-gray-800 mt-2">
        Electricity is your largest home emission source. Reduce usage during peak hours, switch off idle devices, and consider green electricity plans.
      </p><br>` : ''}

    ${naturalGasPct > electricityPct && naturalGasPct > heatingFuelPct && naturalGasPct > waterPct && naturalGasPct > constructionPct ? `
      <p class="text-[16px] text-gray-800 mt-2">
        Natural gas use is high. You can reduce emissions by improving insulation and using programmable thermostats to avoid overheating.
      </p><br>` : ''}

    ${heatingFuelPct > electricityPct && heatingFuelPct > naturalGasPct && heatingFuelPct > waterPct && heatingFuelPct > constructionPct ? `
      <p class="text-[16px] text-gray-800 mt-2">
        Heating fuels are a major contributor. Upgrading to more efficient systems or switching to cleaner fuels may help.
      </p><br>` : ''}

    ${waterPct > electricityPct && waterPct > naturalGasPct && waterPct > heatingFuelPct && waterPct > constructionPct ? `
      <p class="text-[16px] text-gray-800 mt-2">
        Water-related emissions are high. Consider shortening hot showers, using cold water for laundry, and installing water-saving devices.
      </p><br>` : ''}

    ${constructionPct > electricityPct && constructionPct > naturalGasPct && constructionPct > heatingFuelPct && constructionPct > waterPct ? `
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
    ${foodTotal > GOALS.food ? `
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
      Breakdown of your food emissions: Meat ${meatPct.toFixed(0)}%, Dairy ${dairyPct.toFixed(0)}%, Fruits & Vegetables ${fruitVegPct.toFixed(0)}%, Cereals ${cerealsPct.toFixed(0)}%, Snacks ${snacksPct.toFixed(0)}%.
    </p>

    ${meatPct > dairyPct && meatPct > fruitVegPct && meatPct > cerealsPct && meatPct > snacksPct ? `
      <p class="text-[16px] text-gray-800 mt-2">
        Meat is the largest contributor to your food emissions. Reducing beef or lamb and replacing them with legumes, tofu, or plant proteins can significantly lower your impact.
      </p><br>` : ''}

    ${dairyPct > meatPct && dairyPct > fruitVegPct && dairyPct > cerealsPct && dairyPct > snacksPct ? `
      <p class="text-[16px] text-gray-800 mt-2">
        Dairy products contribute the most to your food emissions. Try plant-based alternatives like almond, oat, or soy milk to reduce this footprint.
      </p><br>` : ''}

    ${snacksPct > meatPct && snacksPct > dairyPct && snacksPct > fruitVegPct && snacksPct > cerealsPct ? `
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
      ${shoppingTotal > GOALS.shopping ? `
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
        Breakdown of your shopping emissions: Furniture ${furniturePct.toFixed(0)}%, Clothing ${clothingPct.toFixed(0)}%, Other Goods ${otherGoodsPct.toFixed(0)}%, Services ${servicesPct.toFixed(0)}%.
      </p>

      ${furniturePct > clothingPct && furniturePct > otherGoodsPct && furniturePct > servicesPct ? `
        <p class="text-[16px] text-gray-800 mt-2">
          Furniture and appliances are the largest contributors in your shopping emissions. Consider buying second-hand, choosing longer-lasting products, or delaying non-essential upgrades.
        </p><br>` : ''}

      ${clothingPct > furniturePct && clothingPct > otherGoodsPct && clothingPct > servicesPct ? `
        <p class="text-[16px] text-gray-800 mt-2">
          Clothing makes up the largest part of your shopping footprint. Try reducing fast fashion purchases, supporting sustainable brands, and buying higher-quality pieces less frequently.
        </p><br>` : ''}

      ${servicesPct > furniturePct && servicesPct > clothingPct && servicesPct > otherGoodsPct ? `
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

  document.getElementById('tabContent0').innerHTML = `<div>${insights.travel}</div>`;
  document.getElementById('tabContent1').innerHTML = `<div>${insights.home}</div>`;
  document.getElementById('tabContent2').innerHTML = `<div>${insights.food}</div>`;
  document.getElementById('tabContent3').innerHTML = `<div>${insights.shopping}</div>`;
}
