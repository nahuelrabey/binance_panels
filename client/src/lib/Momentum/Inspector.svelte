<script lang="ts">
  import Ema from "../Ema/index.svelte";
  import Oscilator from "./Oscilator.svelte";
  import { onMount } from "svelte";

  import {
    extractTickValues,
    mapToPrice,
    postTickerMomentum,
    type ChartData,
    type Tick,
  } from "../ticker";
  import { Chart } from "svelte-lightweight-charts";

  export let ticker: string = "MATICUSDT";
  export let interval: string = "1m";

  const ticks: Tick[] = [
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
    return await postTickerMomentum(ticker, interval, ticks_values);
  }

  const ticker_promise: any = fetch_ticker(ticker, ticks, interval);

  // fetch_ticker(ticker, ticks, interval);
</script>

<div>
  <h3>{ticker} {interval}</h3>
  {#await ticker_promise}
    <p>loading...</p>
  {:then ticker_data}
    <!-- {console.log(ticker_data)} -->
    <Chart
      width={900}
      height={500}
      timeScale={{
        secondsVisible: true,
        timeVisible: true,
      }}
      leftPriceScale={{
        visible: true,
        scaleMargins: {
          top: 0.85,
          bottom: 0,
        },
      }}
      rightPriceScale={{
        visible: true,
      }}
      crosshair={{
        mode: 0,
      }}
    >
      <Ema {ticker_data} {ticks} />
      <Oscilator {ticker_data} {ticks} />
    </Chart>
  {:catch}
    <p>error</p>
  {/await}
</div>

<style>
  h3 {
    font-weight: 100;
    font-size: 1.5em;
  }
</style>
