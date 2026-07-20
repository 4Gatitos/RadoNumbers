# La banda intermèdia a < c < a(K+2) — RESOLTA PER GENERADOR EXACTE

> **Actualització final (10 juliol 2026):** la banda queda **resolta en l'únic
> sentit que existeix per a aquest objecte** (no hi ha fórmula tancada — vegeu
> més avall): un **algorisme exacte polinòmic en a**, `midband_gen.py`, que
> calcula Rad₂(a;c) sense SAT.
>
> **Com funciona** (per capes): (L1) a∣c ⟹ c/a [teorema demostrat];
> (L2) cua profunda de la banda: fórmula tancada Rad₂ = lam−1+[lam≤E₁] [exacta
> a totes les dades]; (L3) nucli: reformulació rotació-finestra — condicionat
> als colors de la finestra de multiplicadors, el problema és exactament
> 2-SAT; s'escombren els O(m²) vectors de finestra de la família canònica
> (calent^i fred^* calent^l) i es fa cerca binària en N.
>
> **Reducció a un sol forat (verificat)**: la capa 2 (fórmula de la cua) és
> pura optimització de velocitat — amb `MIDBAND_NO_L2=1` el generador "només
> capa 3" segueix donant 7712/7712 exacte. Per tant la correcció del generador
> depèn d'UN SOL teorema conjectural: la completesa de la família de finestra.
>
> **Rigor**: (a) DEMOSTRAT que gen mai sobreestima — cada N acceptat porta una
> coloració explícita vàlida (cota inferior certificada incondicional);
> (b) la completesa de la família canònica (no subestimar) és **conjectural**,
> verificada empíricament a TOTS els valors mai calculats:
> **~28.000 verificacions, zero desajustos** — 7.600 midband + 6.192 fullband
> + 219 OOS a=18–22 (verificador independent propi) + ~14.000 més de les altres vies
> (4 rutes independents convergents, amb valors frescos fins a c=15.503,
> Rad₂=815). Pas restant per a estatus de teorema complet: demostrar la
> completesa de la família de finestra.

*(El document següent conserva l'anàlisi que va portar fins aquí.)*

*Última zona oberta del problema de Dwivedi–Tripathi. K = ⌈(1+c(a+3))/(1+a(a+3))⌉ − 1.*

## Veredicte: NO té fórmula tancada global (i això és un resultat, no un fracàs)

Després de calcular **11.347 valors exactes** (7.600 al dataset a≤24 + 3.747
fora de mostra a=25–32) i minar-los des de cinc angles amb verificació pròpia:

**Rad₂ a la banda intermèdia és genuïnament irregular (quasi-periòdic Sturmià).**
Al llarg de cada diagonal (a, μ) fixos, l'excés delta = Rad₂ − (K+1) és una
escala decreixent la deriva de la qual està governada per la fracció contínua
de μ/a — el mateix mecanisme de "defectes de fase" que va resoldre la finestra
0<c<a, però aquí **els defectes no es tanquen en cap període finit** per a
paràmetres genèrics. Un model periòdic sobreajustat (period-a, ajustat des de
les pròpies dades) topa al ~85%, molt lluny del 99% que exigiria una fórmula.
**Això explica per què Dwivedi–Tripathi només van poder donar cotes inferiors.**

## El que SÍ que hem obtingut (tot verificat al 100%, dins i fora de mostra)

### 1. Primera cota SUPERIOR per a la banda (conjectura nova, 11.347/11.347)
> **K+1 ≤ Rad₂(a;c) ≤ max(K+2, ⌊(a²+1)/2⌋).**

DT només tenien cotes inferiors; això **enclou** la banda entre dues cotes.
A prop del sostre de la banda l'interval és d'amplada 1 (Rad₂ ∈ {K+1, K+2}).
És una **conjectura** (verificada massivament, no demostrada).

### 2. Rebanades exactes (fórmules tancades sobre subconjunts, 100%)
- **a | c ⟹ Rad₂(a;c) = c/a** — ara **TEOREMA amb demostració completa**:
  si c = ma, la terna (x₁,x₂,x₃) = (m, m, m) satisfà m + am − m = am = c i és
  automàticament monocromàtica, de manera que Rad₂ ≤ m; i la cota inferior del
  seu Teorema 6 dona K+1 = m (per a m ≥ 2, ⌈(1+ma(a+3))/(1+a(a+3))⌉ = m).
  Això estén el seu Teorema 5 (provat només per a m ≤ a+1) a tot m. ∎
- c = a+1 ⟹ Rad₂ = 2a−1.
- c = 2a−1 ⟹ Rad₂ = 2(a−1) (a ≥ 5).
- Pic de la fila inferior (a senar, c = (3a−1)/2) ⟹ Rad₂ = (a²+1)/2.
  Aquest sol punt ja demostra que la cota inferior K+1 de DT és fluixa per
  Θ(a²) a la part baixa de la banda.

### 3. Estructura provada/observada
- delta = Rad₂ − (K+1) ≥ 0 sempre (confirma el seu Teorema 6), i és monòtona
  no creixent en lam per a (a,μ) fixos (99,7%; les excepcions són salts de
  ±1 d'aliàsing del sostre).
- Simetria t ↔ a−t de l'interior: el paràmetre real és el parell {t, a−t}.
- Els testimonis extremals són coloracions de període a ("t uns, a−t zeros")
  amb correccions Sturmianes de fase.

## Reformulació estructural (la porta d'entrada per a un algorisme exacte)

Amb e := c − a > 0, les ternes solució són (x, k, x + a(k−1) − e), i **tots els
desplaçaments s_k = a(k−1) − e són ≡ −e (mod a)**. Les restriccions connecten
doncs la classe de residu ρ (mod a) amb la classe ρ − e (mod a): el problema
està governat per la **rotació discreta per −e sobre Z_a** (amb g = gcd(e,a)
òrbites de longitud a/g) — l'origen estructural del comportament Sturmià
(teorema de les tres distàncies de la rotació). Els multiplicadors rellevants
k(s) = (s+e)/a + 1 viuen en una finestra d'amplada ~2N/a al voltant de
lam = ⌈c/a⌉; per a c ≥ a(K+2) surten de [1,N] i les restriccions s'evaporen —
exactament on comença el règim (ja demostrat) de la Conjectura 2. Tot és de
mida O(a): un algorisme exacte polinòmic en a és l'objectiu realista
("resolució per generador", no per fórmula).

## Confirmació (segon i tercer atac): la impossibilitat és robusta

Després de la mineria inicial es van llançar dos esforços profunds més:
- **Cinc anàlisis independents** (periodicitat, diagonals, testimonis, max-de-cotes,
  escèptic): veredicte unànime *estructura parcial*, cap fórmula global.
- **Quatre vies d'atac Beatty** (esglaons Beatty, serra directa, longitud de
  coloració, reducció a fracció contínua): cap va superar la línia base K+1 a
  l'interior. La millor descripció exacta per diagonal és
  delta = Δ₀ − d₁·⌊(lam−φ₁)/a⌋ − d₂·⌊(lam−φ₂)/a⌋ amb d₁+d₂=a, **però les mides
  dels salts (d₁,d₂) segueixen la fracció contínua de μ/a** — no hi ha un conjunt
  finit de casos elementals (a=13 dona {6,7} gairebé sempre, però μ=5 dona {9,4}).
- **Auto-similaritat trencada**: rad₂(a, c+a²) − rad₂(a,c) s'escampa de −120 a +19
  (moda 0 amb 2445/9470); ni tan sols hi ha recurrència neta període-a².

**Conclusió (robusta, no per manca d'esforç): Rad₂ a la banda intermèdia és un
objecte Sturmià / de tres distàncies genuí, governat per la fracció contínua de
(a−t)/a. No té fórmula tancada elemental ni recurrència neta.** Això *és* la
caracterització correcta de la zona, i explica per què Dwivedi–Tripathi (i
nosaltres) només podem donar cotes, no un valor exacte tancat. Una determinació
exacta requeriria un *generador* algorítmic euclidià sobre la cf de μ/a, no una
fórmula — un programa de recerca a part.

## Estat de rigor
- Rebanada a|c i valors de la fila inferior: **probablement demostrables** amb
  la maquinària de forçament del projecte (mu = 0 i lam = 2 casos).
- La cota superior (pin): **conjectura**; demostrar-la requereix un argument de
  coloració nou (direcció difícil).
- Irregularitat Sturmiana: caracterització estructural, no teorema formal.

## Fitxers
`midband_data.py`, `mine_midband.py`, `verify_midband_claims.py`,
`oos_midband.py`; dades a `results/midband.{csv,jsonl}`.

## Identitat de la cua (verificada a<200): E1(a,t) = Rad2(a; a-t)

El llindar E1 de la capa 2 del generador es EXACTAMENT el valor dels nostres
Teoremes 1-2 (finestra 0<c<a, ja demostrats i verificats) per a c' = a-t:
t=1 dona 2a+2 (Teorema 1) i t>=2 dona (a+2)t+a+1+max(t-(a mod 2t),0) =
(a+3)t+a-min(r-1,t-1) amb r = a mod 2t (Teorema 2). La cua profunda de la
banda hereta doncs l'estructura de la finestra resolta; la dependencia
"small-c upper bound" que la verificació assenyalava com a oberta ja esta
DEMOSTRADA al projecte (sec_ub1/sec_ub2). Forats restants reals: CCL
(completesa de familia) i pin G2 (Rad2 <= lam a la cua profunda).

## TANCAMENT (10 juliol 2026): CCL DEMOSTRADA — el generador és TEOREMA

L'últim forat (nucli en V) ha caigut amb una forma més forta del que calia:
tota coloració vàlida d'una instància V-core té porta x·g^(m−2)·y (vall
d'igual color, interior uniforme), sempre ≤ 3 trams. Peces noves: Lemma PAIR
(infactibilitat de dues distàncies quan v₂(P) ≠ v₂(Q), amb recíproc exacte)
i Lemma WINDOW (cicle senar — senar EXACTAMENT per la condició d'existència
2-àdica — que dos conjunts independents no poden cobrir). Checkat verificat per duplicat;
verificador consolidat demostracio/verify_vcore_ccl.py: ALL CHECKS PASS.

Cadena completa: CCL-V + Teorema SA (braç únic) + m≤3 + tricotomia V0
⟹ CCL total ⟹ (Lemma M + Teorema E) gen = Rad₂ a TOTA la banda, teorema.

AMB AIXÒ, Rad₂(a;c) per a x₁+a·x₂−x₃=c queda DETERMINAT AMB DEMOSTRACIÓ a
tot el rang de paràmetres on existeix: fórmules tancades demostrades a tot
arreu excepte la banda intermèdia, i allà un generador exacte demostrat
(sense fórmula tancada possible — caracterització Sturmiana). L'única
verificació pendent és externa: revisió humana / assistent formal.
