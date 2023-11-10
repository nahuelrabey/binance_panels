<script lang="ts">
  import { LineStyle } from "lightweight-charts";
  import { mapToEmas, type ChartData, type Tick } from "../ticker";
  import { Chart, LineSeries } from "svelte-lightweight-charts";

  export let price: ChartData[] = [];
  export let ticks: Tick[] = [];

  const emas = mapToEmas(price, ticks);

  console.log("EMA")
  console.log("price", price)
  console.log("ticks", ticks)
  console.log("emas", emas)

</script>
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
  {console.log(emas[ema_key])}
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
