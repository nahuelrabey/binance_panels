<script lang="ts">
  import MacdInspectView from "../lib/Macd/InspectView.svelte";
  import {Link} from "svelte-routing"

  export let ticker: string = "MATICUSDT";
  let input: string = ticker

</script>

<main>
  <input bind:value={input} placeholder="enter your ticker" />
  <!-- <button on:click={()=>onCLick()}>submit</button> -->
  <Link to={`/page/macd/${input}`}>submit</Link>
  {#key ticker}
    {console.log("render:", ticker)}
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