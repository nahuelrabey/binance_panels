<script lang="ts">
  import { Chart, LineSeries } from "svelte-lightweight-charts";
  import type { OscilatorHash } from "../ticker";

  export let oscilators: OscilatorHash = {};
</script>

<!-- <Chart
  width={800}
  height={200}
  timeScale={{
    secondsVisible: true,
    timeVisible: true,
  }}
> -->
{#each Object.keys(oscilators) as key}
  <LineSeries
    data={oscilators[key].data}
    reactive={true}
    color={oscilators[key].color}
    lineWidth={2}
    priceScaleId="left"
  />
{/each}
<!-- </Chart> -->
