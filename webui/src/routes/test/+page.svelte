<script lang="ts">
	import { Drawer, Minimap, Node, Svelvet, ThemeToggle } from 'svelvet';
</script>

<div class="flex justify-center p-8">
	<div class="border border-black">
		<Svelvet height={(5 * window.innerHeight) / 6} width={(5 * window.innerWidth) / 6}>
			<Node position={{ x: 25, y: 25 }} dimensions={{ height: 50, width: 50 }} />
			<Minimap width={100} corner="NE" slot="minimap" />
		</Svelvet>
	</div>
</div>
