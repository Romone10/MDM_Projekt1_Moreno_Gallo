<script>
    let url = location.protocol + "//" + location.host;

    let OS_Android = 0;
    let Display_60Hz = 0;
    let Display_120Hz = 0;
    let Battery_mAh = 0;
    let RAM_GB = 0;
    let GHz = 0;
    let Has_5G = 0;
    let Dual_Sim = 0;

    let predictedPrice = 0;

    async function predict() {
        const response = await fetch("/api/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                OS_Android,
                Display_60Hz,
                Display_120Hz,
                Battery_mAh,
                RAM_GB,
                GHz,
                Has_5G,
                Dual_Sim,
            }),
        });
        const data = await response.json();
        predictedPrice = data.price;
    }
</script>

<h1>Smartphone Analyse</h1>

<p>
    <strong>Betriebssystem von Android gewünscht? [m]</strong>
    <label>
        <input type="checkbox" bind:checked={OS_Android} />
    </label>
</p>

<p>
    <strong>60Hz Display gewünscht? [m]</strong>
    <label>
        <input type="checkbox" bind:checked={Display_60Hz} />
    </label>
</p>

<p>
    <strong>Oder doch lieber 120Hz für den nächsten Serienmarathon? [m]</strong>
    <label>
        <input type="checkbox" bind:checked={Display_120Hz} />
    </label>
</p>

<p>
    <strong>Batterie [m]</strong>
    <label>
        <select bind:value={Battery_mAh}>
            <option value="1000">1000</option>
            <option value="1100">1100</option>
            <option value="1200">1200</option>
            <option value="2500">2500</option>
            <option value="2800">2800</option>
            <option value="4000">4000</option>
            <option value="4500">4500</option>
            <option value="5000">5000</option>
            <option value="5100">5100</option>
        </select>
    </label>
</p>

<p>
    <strong>RAM [m]</strong>
    <label>
        <select bind:value={RAM_GB}>
            <option value="8">8</option>
            <option value="16">16</option>
            <option value="32">32</option>
            <option value="64">64</option>
            <option value="128">128</option>
        </select>
    </label>
</p>

<p>
    <strong>GHz [m]</strong>
    <label>
        <select bind:value={GHz}>
            <option value="1.77">1.77</option>
            <option value="2.2">2.2</option>
            <option value="2.4">2.4</option>
            <option value="2.8">2.8</option>
            <option value="100">100</option>
            <option value="208">208</option>
        </select>
    </label>
</p>

<p>
    <strong>5G für schnelleres Internet gewünscht? [m]</strong>
    <label>
        <input type="checkbox" bind:checked={Has_5G} />
    </label>
</p>

<p>
    <strong>Oft auf Reisen? Ein Smartphone mit Dual Sim kann helfen. [m]</strong
    >
    <label>
        <input type="checkbox" bind:checked={Dual_Sim} />
    </label>
</p>

<!-- 
<p>
    <strong>Was schätzt du, wie viel ein Smartphone mit den von dir gewählten Spezifikationen kostet? [m]</strong>
    <label>
        <input type="range" bind:value={price} min="0" max="3000" />
        <input type="number" bind:value={price} min="0" max="3000" />
    </label>
</p>
-->

<button on:click={predict}>Preisprognose</button>

<p>
    Preis für ein Smartphone mit den angegebenen Spezifikationen: {predictedPrice}
</p>
