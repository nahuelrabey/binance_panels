<script lang="ts">
    import EmaMomentumView from "./EMAMomentumView.svelte";
    export let ticker: string;
</script>

<div>
  <EmaMomentumView interval={"1m"} ticker={ticker}/>
  <EmaMomentumView interval={"1h"} ticker={ticker}/>
  <EmaMomentumView interval={"1d"} ticker={ticker}/>
  <EmaMomentumView interval={"1w"} ticker={ticker}/>
</div>