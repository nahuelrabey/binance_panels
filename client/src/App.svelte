<script>
  import { Router, Link, Route } from "svelte-routing";
  import Home from "./routes/Home.svelte";
  import Momentum from "./routes/Momentum.svelte";
  import Macd from "./routes/Macd.svelte";

  export let url = "";
</script>

<Router {url}>
  <nav>
    <Link to="/">Home</Link>
    <Link to="/page/momentum/BTCUSDT">Momentum View</Link>
    <Link to="/page/macd/BTCUSDT">MACD View</Link>
  </nav>
  <div>
    <Route path="/page/momentum/:ticker" let:params
      ><Momentum ticker={params.ticker} /></Route
    >
    <Route path="/page/macd/:ticker" let:params
      ><Macd ticker={params.ticker} /></Route
    >
    <Route path="/"><Home /></Route>
  </div>
</Router>
