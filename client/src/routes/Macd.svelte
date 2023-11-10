<script lang="ts">
  import MacdInspectView from "../lib/MacdInspectView.svelte";
  import {Link} from "svelte-routing"

  export let ticker: string = "MATICUSDT";
  let input: string = ticker

  // function onCLick(){
  //   ticker = input
  //   console.log(`new ticker: ${ticker}`)
  //   console.log()
  //   window.open(`/page/macd/${ticker}`)
  // }
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