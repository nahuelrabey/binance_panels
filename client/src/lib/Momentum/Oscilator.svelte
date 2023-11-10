<script lang="ts">
  import Oscilator from "../Oscilator/index.svelte";
  import { mapToMomentumOscilator, type ChartData, type Tick } from "../ticker";

  export let price: ChartData[] = [];
  export let ticks: Tick[] = []
  const oscilators = mapToMomentumOscilator(price, ticks);
  console.log("Momentum")
  console.log("price", price)
  console.log("ticks", ticks)
  console.log("oscilators", oscilators)
</script>

<Oscilator oscilators={oscilators} />
