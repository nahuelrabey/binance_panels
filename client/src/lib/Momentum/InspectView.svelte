<script lang="ts">
  import Momentum from "./Inspector.svelte";
  export let ticker: string;
</script>

<div>
  <Momentum interval={"1m"} {ticker} />
  <Momentum interval={"1h"} {ticker} />
  <Momentum interval={"1d"} {ticker} />
  <Momentum interval={"1w"} {ticker} />
</div>
