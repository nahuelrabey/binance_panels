<script lang="ts">
  import { Chart, LineSeries } from "svelte-lightweight-charts";
  import { LineStyle } from "lightweight-charts";
  import type { Time } from "lightweight-charts";
  import {
    extractTickValues,
    mapToEmas,
    mapToMacdOscilator,
    mapToPrice,
    postMacdEmaId,
    postMacdId,
    postTickerMacd,
    type OscilatorHash,
  } from "./ticker";

  export let ticker: string = "MATICUSDT";
  export let interval: string = "1m";
  export let short: number = 12;
  export let long: number = 24;
  export let signal: number = 9;

  type ChartData = {
    time: Time;
    value: number;
  };

  let price: ChartData[] = [];
  let emas: { [key: string]: { color: string; data: ChartData[] } } = {};
  let oscilators: OscilatorHash = {};
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
    const start = new Date().getTime();
    const ticks_values = extractTickValues(ticks);
    const json = await postTickerMacd(
      ticker,
      interval,
      ticks_values,
      short,
      long,
      signal
    );

    price = mapToPrice(json);
    emas = mapToEmas(json, ticks);

    const macd_id = await postMacdId(short, long, signal);
    const macd_ema_id = await postMacdEmaId(short, long, signal);

    oscilators = mapToMacdOscilator(json, macd_id, macd_ema_id);
    const end = new Date().getTime();
    console.log(`fetch_ticker took ${end - start} ms`);
  }

  fetch_ticker(ticker, ticks, interval).catch((e) => console.log(e));
</script>

<div>
  <h3>{ticker} {interval}</h3>
  <!-- {#key oscilators} -->
  {console.log("OSCILATORS:",oscilators)}
  <Chart
    width={800}
    height={400}
    timeScale={{
      secondsVisible: true,
      timeVisible: true,
    }}
  >
    <LineSeries data={price} reactive={true} lineWidth={2} title="Price" />
    {#each Object.keys(emas) as ema_key}
      <LineSeries
        title={ema_key}
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
    {#each Object.keys(oscilators) as key}
      <LineSeries
        data={oscilators[key].data}
        reactive={true}
        color={oscilators[key].color}
        lineWidth={2}
        lineStyle={oscilators[key].lineStyle}
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
