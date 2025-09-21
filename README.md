# Kokoustranskriptien parsinta

Aja näin:

```bash
uv run kirjuri QJjodmUVHms
```

Transkriptiotiedostoja ilmestyy kansioon `out/`.
Kaikki katkelmat on listattu tiedostossa [`out/index.md`](out/index.md).
Indeksissä on korkeintaan 300 merkkiä katkelman tekstistä.
Katkelmat kokonaisuudessaan on tiedostoissa muotoa `out/[hh.mm.ss].md`.
Kussakin tiedostossa on linkki myös videokohtaan.

Transkriptio on melko karkea, se kannattaa ajaa lisäksi tekoälyn läpi.
Tiedostossa [`CLEANUP.md`](CLEANUP.md)
on ehdotettu konteksti tekoälylle, esim. Claude Code:

```
> Clean up @out/00.36.12.md as described in @CLEANUP.md.
```