<script lang="ts">
  import { LineStyle } from "lightweight-charts";
  import { mapToEmas, type ChartData, type Tick, mapToPrice } from "../ticker";
  import { Chart, LineSeries } from "svelte-lightweight-charts";

  export let ticker_data: any = {};
  export let ticks: Tick[] = [];

  const price = mapToPrice(ticker_data);
  const emas = mapToEmas(ticker_data, ticks);
</script>

<!-- <Chart
  width={800}
  height={400}
  timeScale={{
    secondsVisible: true,
    timeVisible: true,
  }}
> -->
<LineSeries data={price} reactive={true} lineWidth={2} title="Price" />
{#each Object.keys(emas) as ema_key}
  <LineSeries
    title={ema_key}
    data={emas[ema_key].data}
    reactive={true}
    lineStyle={LineStyle.Dashed}
    color={emas[ema_key].color}
    lineWidth={2}
    priceScaleId="right"
  />
{/each}
<!-- </Chart> -->
