<script lang="ts">
    import EmaMacdInspector from "./EmaMacdInspector.svelte";
    export let ticker: string;
</script>

<div>
  <EmaMacdInspector interval={"1m"} ticker={ticker}/>
  <EmaMacdInspector interval={"1h"} ticker={ticker}/>
  <EmaMacdInspector interval={"1d"} ticker={ticker}/>
  <EmaMacdInspector interval={"1w"} ticker={ticker}/>
</div>