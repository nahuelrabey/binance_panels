<script lang="ts">
  import Macd from "./MacdInspector.svelte";
  export let ticker: string;

  const short = 12;
  const long = 26;
  const signal = 9;
</script>

<div>
  <Macd interval={"1m"} ticker={ticker} short={short} long={long} signal={signal} />
  <Macd interval={"1h"} ticker={ticker} short={short} long={long} signal={signal} />
  <Macd interval={"1d"} ticker={ticker} short={short} long={long} signal={signal} />
  <Macd interval={"1w"} ticker={ticker} short={short} long={long} signal={signal} />
</div>
