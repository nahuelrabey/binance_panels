<script lang="ts">
    import EmaMomentumInspector from "./EmaMomentumInspector.svelte";
    export let ticker: string;
</script>

<div>
  <EmaMomentumInspector interval={"1m"} ticker={ticker}/>
  <EmaMomentumInspector interval={"1h"} ticker={ticker}/>
  <EmaMomentumInspector interval={"1d"} ticker={ticker}/>
  <EmaMomentumInspector interval={"1w"} ticker={ticker}/>
</div>