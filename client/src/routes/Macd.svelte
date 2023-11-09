<script lang="ts">
  import MacdInspectView from "../lib/MacdInspectView.svelte";

  let pre_ticker: string = "MATICUSDT";
  let ticker = pre_ticker

  // $: getTicker = ()=>ticker
</script>

<main>
  <input bind:value={pre_ticker} placeholder="enter your ticker" />
  <button on:click={()=>ticker = pre_ticker}>submit</button>
  {#key ticker}
    <MacdInspectView ticker={ticker} />
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