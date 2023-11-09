<script lang="ts">
  import svelteLogo from "./assets/svelte.svg";
  import viteLogo from "/vite.svg";
  import { Chart, LineSeries } from "svelte-lightweight-charts";
  import { LineStyle } from "lightweight-charts";
  import type { Time } from "lightweight-charts";
  import { extractTickValues, mapToEmas, mapToPrice, postData } from "./lib/ticker";

  type ChartData = {
    time: Time;
    value: number;
  };

  let price: ChartData[] = [];
  let emas: { [key: string]: { color: string; data: ChartData[] } } = {};
  const ticks: [string, number][] = [
    ["green", 10],
    ["orange", 40],
    ["red", 60],
  ];
  async function fetch_ticker(ticker:string) {
    const ticks_values = extractTickValues(ticks);
    const json = await postData(ticker, "1m", ticks_values);
    console.log(json)
    price = mapToPrice(json);
    emas = mapToEmas(json, ticks);
  }

  fetch_ticker("MATICUSDT");
</script>

<main>
  <div>
    <a href="https://vitejs.dev" target="_blank" rel="noreferrer">
      <img src={viteLogo} class="logo" alt="Vite Logo" />
    </a>
    <a href="https://svelte.dev" target="_blank" rel="noreferrer">
      <img src={svelteLogo} class="logo svelte" alt="Svelte Logo" />
    </a>
  </div>
  <h1>Vite + Svelte</h1>
  <Chart width={800} height={600}>
    <LineSeries data={price} reactive={true} lineWidth={2} />
    {#each Object.keys(emas) as ema_key}
      <LineSeries
        data={emas[ema_key].data}
        reactive={true}
        lineStyle={LineStyle.Dashed}
        color={emas[ema_key].color}
        lineWidth={2}
      />
    {/each}
  </Chart>

  <p>
    Check out <a
      href="https://github.com/sveltejs/kit#readme"
      target="_blank"
      rel="noreferrer">SvelteKit</a
    >, the official Svelte app framework powered by Vite!
  </p>

  <p class="read-the-docs">Click on the Vite and Svelte logos to learn more</p>
</main>

<style>
  .logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
    transition: filter 300ms;
  }
  .logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
  }
  .logo.svelte:hover {
    filter: drop-shadow(0 0 2em #ff3e00aa);
  }
  .read-the-docs {
    color: #888;
  }
</style>
