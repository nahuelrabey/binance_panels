<script lang="ts">
  import SimpleInspectView from "./lib/SimpleInspectView.svelte";

  let ticker: string = "MATICUSDT";
</script>

<main>
  <input bind:value={ticker} placeholder="enter your ticker" />
  {#key ticker}
    <SimpleInspectView ticker={ticker} />
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
