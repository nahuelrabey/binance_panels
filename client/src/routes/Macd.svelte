<script lang="ts">
  import MacdInspectView from "../lib/MacdInspectView.svelte";

  let ticker: string = "MATICUSDT";
</script>

<main>
  <input bind:value={ticker} placeholder="enter your ticker" />
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