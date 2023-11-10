<script lang="ts">
  import { Link } from "svelte-routing";
  import MomentumInspectView from "../lib/Momentum/InspectView.svelte";

  export let ticker: string = "MATICUSDT";
  let input: string = ticker;

</script>

<main>
  <input bind:value={input} placeholder="enter your ticker" />
  <Link to={`/page/momentum/${input}`}>submit</Link>
  {#key ticker}
    {console.log("render:", ticker)}
    <MomentumInspectView ticker={ticker} />
  {/key}
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
</style>
