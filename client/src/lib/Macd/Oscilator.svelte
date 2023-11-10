<script lang="ts">
  import Oscilator from "../Oscilator/index.svelte";
  import {
    type ChartData,
    mapToMacdOscilator,
  } from "../ticker";

  export let ticker_data: ChartData[] = [];
  export let id: string = "";
  export let ema_id: string = "";

  console.log("Oscilator");
  const oscilators = mapToMacdOscilator(ticker_data, id, ema_id);
</script>

<Oscilator {oscilators} />
