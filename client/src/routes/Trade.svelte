<script lang="ts">
  import { Link } from "svelte-routing";
  import Momentum from "../lib/Macd/Inspector.svelte";
  import Macd from "../lib/Momentum/Inspector.svelte";

  export let ticker: string = "BTCUSDT";
  export let interval: string = "1m";
  let ticker_in: string = ticker;
  let interval_in: string = interval;

  let ammount = 0;

  const buy15 = () => (ammount += 15);
  const buy20 = () => (ammount += 20);
  const buy25 = () => (ammount += 25);

  const sell15 = () => (ammount -= 15);
  const sell20 = () => (ammount -= 20);
  const sell25 = () => (ammount -= 25);
</script>

<h1>Trade View - {ticker}</h1>

<div class="inputs">
  <div>
    <input bind:value={ticker_in} placeholder="enter your ticker" />
    <Link to={`/page/trade/${ticker_in}/${interval_in}`}>submit</Link>
  </div>
  <div>
    <input bind:value={interval_in} placeholder="enter your ticker" />
    <a href={`/page/trade/${ticker_in}/${interval_in}`}>submit</a>
  </div>
  <div class="buy">
    <button on:click={buy15}>BUY 15</button>
    <button on:click={buy20}>BUY 20</button>
    <button on:click={buy25}>BUY 25</button>
  </div>
  <div class="sell">
    <button on:click={sell15}>SELL 15</button>
    <button on:click={sell20}>SELL 20</button>
    <button on:click={sell25}>SELL 25</button>
  </div>
    <p>AMMOUNT: {ammount}</p>
  <div />
</div>
<div class="graphs">
  <Momentum {ticker} {interval} />
  <Macd {ticker} {interval} />
</div>

<style>
  .inputs {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 10px;
  }
  .buy,
  .sell {
    color: white;
  }
  .buy button {
    background-color: greenyellow;
  }
  .sell button {
    background-color: #ff0000;
  }
  .graphs {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }
</style>
