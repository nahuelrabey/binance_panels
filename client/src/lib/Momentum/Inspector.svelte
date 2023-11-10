<script lang="ts">
  import Ema from "../Ema/index.svelte";
  import Oscilator from "./Oscilator.svelte";
  import type { Time } from "lightweight-charts";
  import {
    extractTickValues,
    mapToPrice,
    postTickerMomentum,
    type ChartData,
    type Tick,
  } from "../ticker";

  export let ticker: string = "MATICUSDT";
  export let interval: string = "1m";

  let price: ChartData[] = [];
  let ticks: Tick[] = [
    ["green", 10],
    ["orange", 40],
    ["red", 60],
  ];
  async function fetch_ticker(
    ticker: string,
    ticks: [string, number][],
    interval: string
  ) {
    const ticks_values = extractTickValues(ticks);
    const json = await postTickerMomentum(ticker, interval, ticks_values);
    price = mapToPrice(json);
  }

  fetch_ticker(ticker, ticks, interval);
</script>

<div>
  <h3>{ticker} {interval}</h3>
  {#key price}
  <Ema price={price} ticks={ticks}/>
  <Oscilator price={price} ticks={ticks}/>
  {/key}
</div>


<style>
  h3 {
    font-weight: 100;
    font-size: 1.5em;
  }
</style>
