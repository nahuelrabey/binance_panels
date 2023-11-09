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
    <Link to="/page/momentum">Momentum View</Link>
    <Link to="/page/macd">MACD View</Link>
  </nav>
  <div>
    <Route path="/page/momentum" component={Momentum} />
    <Route path="/page/macd" component={Macd} />
    <Route path="/"><Home/></Route>
  </div>
</Router>
