# Créditos de las fotos

Todas las fotos vienen de [Wikimedia Commons](https://commons.wikimedia.org/) y tienen licencia libre. Se descargaron en tamaño web (960 px de ancho). Las licencias CC BY y CC BY-SA obligan a citar al autor y la licencia; la página lo hace en el pie ("Créditos de las fotos") y en la ficha de cada fecha.

| Archivo | Flor | Autor | Licencia | Original |
|---|---|---|---|---|
| `rosa-roja.jpg` | Rosa roja | Petro Stelte | CC BY-SA 4.0 | [Red-Rose-Sitia-Crete.jpg](https://commons.wikimedia.org/wiki/File:Red-Rose-Sitia-Crete.jpg) |
| `rosa-rosa.jpg` | Rosa rosa | Acabashi | CC BY-SA 4.0 | [Pink rose bloom… Boreham](https://commons.wikimedia.org/wiki/File:Pink_rose_bloom_of_a_climbing_rose_at_Boreham,_Essex,_England_1.jpg) |
| `ramo-rosas.jpg` | Ramo de rosas rosas | Jebulon | CC BY-SA 3.0 | [Bouquet de roses roses.jpg](https://commons.wikimedia.org/wiki/File:Bouquet_de_roses_roses.jpg) |
| `ramo-tulipanes.jpg` | Ramo de tulipanes | Gábor Juhász (juhg) | CC0 | [Tulip-bouquet-vienna](https://commons.wikimedia.org/wiki/File:Tulip-bouquet-vienna_(Unsplash).jpg) |
| `mimosa.jpg` | Mimosa (*Acacia dealbata*) | JMK | CC BY-SA 3.0 | [Acacia dealbata, blomme, Waterberg.jpg](https://commons.wikimedia.org/wiki/File:Acacia_dealbata,_blomme,_Waterberg.jpg) |
| `girasol.jpg` | Girasol | Böhringer Friedrich | CC BY-SA 2.5 | [Sonnenblume Helianthus 1.JPG](https://commons.wikimedia.org/wiki/File:Sonnenblume_Helianthus_1.JPG) |
| `muguet.jpg` | Lirio de los valles | Agnes Monkelbaan | CC BY-SA 4.0 | [Convallaria majalis 01](https://commons.wikimedia.org/wiki/File:Lelietje-van-dalen_of_meiklokje_(Convallaria_majalis)._14-05-2021_(actm.)_01.jpg) |
| `clavel.jpg` | Clavel | Andy Mabbett | CC BY-SA 4.0 | [Bright pink carnation cultivar](https://commons.wikimedia.org/wiki/File:Bright_pink_carnation_cultivar_-_2020-05-11_-_Andy_Mabbett_-_01.jpg) |
| `peonia.jpg` | Peonía | Acabashi | CC BY-SA 4.0 | [Cottage garden pink peony](https://commons.wikimedia.org/wiki/File:Cottage_garden_pink_peony_bloom_at_Boreham,_Essex,_England.jpg) |
| `lilium.jpg` | Lilium 'Marco Polo' | Derek Ramsey (Ram-Man) · Chanticleer Garden | CC BY-SA 3.0 | [Lilium 'Marco Polo'](https://commons.wikimedia.org/wiki/File:Lilium_%27Marco_Polo%27_Flower_2580px.jpg) |
| `hortensia-azul.jpg` | Hortensia azul | Subhrajyoti07 | CC BY-SA 4.0 | [Blue Hydrangea](https://commons.wikimedia.org/wiki/File:Blue_Hydrangea_(common_names_hydrangea_or_hortensia).jpg) |
| `crisantemo.jpg` | Crisantemo blanco | 阿橋 HQ | CC BY-SA 2.0 | [Chrysanthemum 'White Crane'](https://commons.wikimedia.org/wiki/File:%E8%8F%8A%E8%8A%B1-%E7%99%BD%E9%B6%B4_Chrysanthemum_morifolium_%27White_Crane%27_-%E5%8F%B0%E5%8C%97%E5%A3%AB%E6%9E%97%E5%AE%98%E9%82%B8_Taipei,_Taiwan-_(12010293154).jpg) |
| `cempasuchil.jpg` | Cempasúchil | Joydeep | CC BY-SA 3.0 | [Tagetes erecta 30012013.jpg](https://commons.wikimedia.org/wiki/File:Tagetes_erecta_30012013.jpg) |
| `violeta.jpg` | Violeta | Uoaei1 | CC BY-SA 4.0 | [Viola odorata 20210226.jpg](https://commons.wikimedia.org/wiki/File:Viola_odorata_20210226.jpg) |
| `nochebuena.jpg` | Nochebuena | Vengolis | CC BY-SA 4.0 | [Euphorbia pulcherrima 0111.jpg](https://commons.wikimedia.org/wiki/File:Euphorbia_pulcherrima_0111.jpg) |
| `ramo-silvestre.jpg` | Ramo de flores silvestres | Petro Stelte | CC BY-SA 4.0 | [Flower-bouquet-wild-flowers](https://commons.wikimedia.org/wiki/File:Flower-bouquet-wild-flowers-Sitia-Crete-Greece.jpg) |



## Versiones web (`imagenes/web/`)

Desde septiembre de 2026 la web usa copias optimizadas de estas fotos, con nombres descriptivos: `<nombre>-960` y `<nombre>-480` en AVIF y WebP, y `<nombre>-160.webp` recortada en cuadrado para miniaturas (por ejemplo, `girasol-amarillo-960.avif`). La correspondencia entre la foto original y su nombre web está en `IMAGES` dentro de `_build/datos.py`. Los `.jpg` originales se mantienen para las vistas previas en redes (`og:image`).

Para añadir una foto nueva: guárdala aquí en `.jpg`, genera sus versiones web (AVIF/WebP a 960 y 480 px y la miniatura de 160 px), añade su entrada en `IMAGES` de `_build/datos.py` con autor, licencia y enlace, y vuelve a generar la web con `python _build/build.py`.
