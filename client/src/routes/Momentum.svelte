<script lang="ts">
  import MomentumInspectView from "../lib/MomentumInspectView.svelte";

  let pre_ticker: string = "MATICUSDT";
  let ticker = pre_ticker;

  function onCLick(){
    ticker = pre_ticker
    console.log(`new ticker: ${ticker}`)
  }
</script>

<main>
  <input bind:value={pre_ticker} placeholder="enter your ticker" />
  <button on:click={() => onCLick()}>submit</button>
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
