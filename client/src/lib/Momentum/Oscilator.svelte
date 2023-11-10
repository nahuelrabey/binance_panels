<script lang="ts">
  import Oscilator from "../Oscilator/index.svelte";
  import { mapToMomentumOscilator, type ChartData, type Tick } from "../ticker";

  export let ticker_data: ChartData[] = [];
  export let ticks: Tick[] = []

  console.log("Oscilator")
  const oscilators = mapToMomentumOscilator(ticker_data, ticks);
  // console.log("oscilators", oscilators)
</script>

<Oscilator oscilators={oscilators} />
