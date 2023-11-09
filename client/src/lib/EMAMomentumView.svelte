<script lang="ts">
  import { Chart, LineSeries } from "svelte-lightweight-charts";
  import { LineStyle } from "lightweight-charts";
  import type { Time } from "lightweight-charts";
  import {
    extractTickValues,
    mapToEmas,
    mapToMomentumOscilator,
    mapToPrice,
    postData,
  } from "./ticker";

  export let ticker: string = "MATICUSDT";
  export let interval: string = "1m";

  console.log("ticker:", ticker)

  type ChartData = {
    time: Time;
    value: number;
  };

  let price: ChartData[] = [];
  let emas: { [key: string]: { color: string; data: ChartData[] } } = {};
  let momentum_oscilators: {
    [key: string]: { color: string; data: ChartData[] };
  } = {};
  let ticks: [string, number][] = [
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
    const json = await postData(ticker, interval, ticks_values);
    console.log(json);
    price = mapToPrice(json);
    emas = mapToEmas(json, ticks);
    momentum_oscilators = mapToMomentumOscilator(json, ticks);
  }

  fetch_ticker(ticker, ticks, interval);
</script>

<div>
  <h3>{ticker} {interval}</h3>
  <Chart
    width={800}
    height={400}
    timeScale={{
      secondsVisible: true,
      timeVisible: true,
    }}
  >
    <LineSeries data={price} reactive={true} lineWidth={2} title="Price"/>
    {#each Object.keys(emas) as ema_key}
      <LineSeries
        title = {ema_key}
        data={emas[ema_key].data}
        reactive={true}
        lineStyle={LineStyle.Dashed}
        color={emas[ema_key].color}
        lineWidth={2}
      />
    {/each}
  </Chart>
  <Chart
    width={800}
    height={200}
    timeScale={{
      secondsVisible: true,
      timeVisible: true,
    }}
  >
    {#each Object.keys(momentum_oscilators) as momentum_oscilator_key}
      <LineSeries
        data={momentum_oscilators[momentum_oscilator_key].data}
        reactive={true}
        color={momentum_oscilators[momentum_oscilator_key].color}
        lineWidth={2}
      />
    {/each}
  </Chart>
</div>


<style>
  h3 {
    font-weight: 100;
    font-size: 1.5em;
  }
</style>
