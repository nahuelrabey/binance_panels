<script lang="ts">
  import { Chart, LineSeries } from "svelte-lightweight-charts";
  import Ema from "../Ema/index.svelte";
  import {
    extractTickValues,
    mapToEmas,
    mapToMacdOscilator,
    mapToPrice,
    postMacdEmaId,
    postMacdId,
    postTickerMacd,
  } from "../ticker";
  import Oscilator from "./Oscilator.svelte";

  export let ticker: string = "MATICUSDT";
  export let interval: string = "1m";
  export let short: number = 12;
  export let long: number = 24;
  export let signal: number = 9;

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
    const json = await postTickerMacd(
      ticker,
      interval,
      ticks_values,
      short,
      long,
      signal
    );

    const macd_id = await postMacdId(short, long, signal);
    const macd_ema_id = await postMacdEmaId(short, long, signal);
    return {
      json,
      macd_id,
      macd_ema_id,
    };
  }

  const promise = fetch_ticker(ticker, ticks, interval);
</script>

<div>
  <h3>{ticker} {interval}</h3>
  {#await promise}
    <p>Loading...</p>
  {:then { json, macd_ema_id, macd_id }}
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
      <Ema ticker_data={json} {ticks} />
      <Oscilator ticker_data={json} id={macd_id} ema_id={macd_ema_id} />
    </Chart>
  {/await}
</div>

<style>
  h3 {
    font-weight: 100;
    font-size: 1.5em;
  }
</style>
