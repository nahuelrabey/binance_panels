<script lang="ts">
  import MomentumInspectView from "../lib/MomentumInspectView.svelte";

  let ticker: string = "MATICUSDT";
</script>

<main>
  <input bind:value={ticker} placeholder="enter your ticker" />
  {#key ticker}
    <MomentumInspectView ticker={ticker} />
  {/key}
</main>

<style>
  main{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
</style>