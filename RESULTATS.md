# Resultats — Nombres de Rado per a x₁ + a·x₂ − x₃ = c

> **Actualització (9 juliol 2026, tarda):** les **Conjectures 1 i 2 de
> Dwivedi–Tripathi estan demostrades** (Teoremes 3 i 4 de la nota).
> La Conjectura 1 resulta ser el cas q=0 del nostre teorema unificat del règim
> r ≤ d (per a c ≤ 0, r = a i la fórmula es redueix a (a+3)(a−c)+1); dues
> demostracions independents, cadascuna verificada correcte×2. La Conjectura 2 se'n
> segueix per l'argument de reflexió del seu Teorema 7 (verificat correcte×2).
> El valor exacte de Rad₂(a;c) queda determinat a tot arreu excepte la banda
> a < c < a(K+2). Esborranys a demostracio/draft_UB-q0-unified.md,
> draft_C1-independent.md i draft_C2-reduction.md; retocs a
> les notes de revisió (aplicades); manuscrit actualitzat (25 pp).

*Projecte "Descobriments matemàtiques" — juliol 2026.*
*Problema font: S. Dwivedi & A. Tripathi, Integers 20 (2020) #A36; reobert com a
Open Problem 1 a Integers 25 (2025) #A108 ("It would be desirable to determine
the exact value of the Rado number in all cases").*

**Notació.** Rad₂(a;c) és el mínim N tal que tota 2-coloració de [1,N] conté una
solució monocromàtica de x₁ + a·x₂ − x₃ = c (valors repetits permesos). Existeix
si i només si v₂(a) ≤ v₂(c). Escrivim d = a−c.

---

## 1. Teorema (nou, amb demostració completa)

> **Teorema.** Per a tot a ≥ 3 senar: **Rad₂(a; a−1) = 2a+2.**

*(El cas a=3 — Rad₂(3;2)=8 — és l'únic que apareixia al paper de 2020, com a
càlcul aïllat. La família completa és nova.)*

Les solucions de l'equació amb c = a−1 són les ternes (x, k, x+(k−1)a+1).

**Cota inferior (Rad₂ ≥ 2a+2).** Definim χ a [1, 2a+1] amb classes
- **A** = { x senar : x ≤ a } ∪ { x parell : a+3 ≤ x ≤ 2a },
- **B** = la resta = { x parell : x ≤ a+1 } ∪ { x senar : x ≥ a+2 }.

Si x₁=x, x₂=k, x₃=x+(k−1)a+1 ≤ 2a+1 amb x ≥ 1, aleshores (k−1)a ≤ 2a−1, i per
tant k ∈ {1,2}.
- *Cap terna dins A:* 2 ∉ A (els parells d'A comencen a a+3), així que caldria
  k=1 i x₃=x+1. Si x ∈ A senar ≤ a, x+1 és parell ≤ a+1 ∈ B; si x ∈ A parell ∈
  [a+3, 2a], x+1 és senar ≥ a+4 ∈ B. Mai monocromàtica.
- *Cap terna dins B:* 1 ∉ B, així que caldria k=2 i x₃=x+a+1. Si x ∈ B parell
  ≤ a−1, x₃ és parell dins [a+3, 2a] ∈ A. Si x = a+1, x₃ = 2a+2 fora de rang.
  Si x ∈ B senar ≥ a+2, x₃ ≥ 2a+3 fora de rang. Mai monocromàtica. ∎

*(Comprovació mecànica: aquesta coloració s'ha verificat vàlida amb el checker
independent per a tot a senar de 3 a 199.)*

**Cota superior (Rad₂ ≤ 2a+2).** Sigui χ una 2-coloració de [1, 2a+2] sense
solucions monocromàtiques; WLOG χ(1)=0.

1. (x,1,x+1) és solució per a tot x ≤ 2a+1: com que χ(1)=0, **no hi ha dos
   consecutius de color 0**. En particular (1,1,2) força χ(2)=1.
2. (x,2,x+a+1) és solució per a x ≤ a+1: com que χ(2)=1, **si χ(x)=1 amb
   x ≤ a+1, aleshores χ(x+a+1)=0**.
3. Les parelles {x, x+a+1}, x ∈ [1,a+1], particionen [1,2a+2]; pel pas 2 cada
   parella conté almenys un 0, així que #0 ≥ a+1. Pel pas 1 (no-adjacència),
   #0 ≤ a+1. Per tant **#0 = a+1 exactament**, i un conjunt de a+1 elements
   sense dos consecutius dins [1,2a+2] té necessàriament la forma
   {1, 3, …, 2j−3} ∪ {2j, 2j+2, …, 2a+2} per a algun j; χ(1)=0 exclou j=1,
   així que j ∈ [2, a+2].
4. Tots els casos donen contradicció:
   - **j = a+2** (els 0 són tots els senars): la terna (a+1, 2, 2a+2) és tota
     de color 1 (a+1 i 2a+2 són parells). Monocromàtica.
   - **3 ≤ j ≤ a+1**: aleshores χ(1)=χ(3)=0 i 2a+2 ≥ 2j és parell, també 0;
     la terna (1, 3, 2a+2) és tota 0. Monocromàtica.
   - **j = 2** (els 0 són {1} ∪ {4,6,…,2a+2}): χ(3)=χ(2)=1 i a+4 és senar ≥ 5,
     també 1; la terna (3, 2, a+4) és tota 1 (a+4 ≤ 2a+2 perquè a ≥ 2).
     Monocromàtica. ∎

*(Per a a parell, c = a−1 és senar i el nombre no existeix, per la condició
v₂; el teorema cobreix doncs tots els casos existents de la diagonal d=1.)*

---

## 2. Teorema 2 (nou, demostrat i verificat): tota la zona 0 < c < a

Zona on el paper de 2020 no dona **cap** conjectura (només cotes).

> **Teorema 2 (juliol 2026).** Siguin 1 ≤ c ≤ a−2 amb
> v₂(a) ≤ v₂(c), d = a−c ≥ 2, i r = a mod 2d pres a [1, 2d]. Aleshores
>
> **Rad₂(a;c) = (a+3)(a−c) + a − min(r−1, d−1).**
>
> (Amb el Teorema 1 — cas d=1, on el valor és 2a+2, una unitat per sota
> d'aquesta expressió — la zona 0 < c < a queda **completament resolta**.)

**Demostració** — en tres peces, als fitxers de `demostracio/`:

1. **Cota inferior, tot d ≥ 2** (`draft_LB-general.md`): la família extremal de
   la secció 2b és vàlida a [1, N−1]. Es reescriu la coloració en *forma normal
   chunk-offset* — punts de salt p_j = ja + t, offset w(x) = x − a·J(x), color
   = [w(x)−1 mod 2d < d] — i una tricotomia del recompte de salts redueix tota
   terna al rang k ≤ d+2 amb tres casos, tots contradictoris.
2. **Cota superior, règim r ≤ d** (`draft_UB-r-le-d.md`): 9 lemes (transport,
   aparellament, finestra, zona llunyana, endgame en dos casos).
3. **Cota superior, règim r > d** (`draft_UB-r-gt-d.md`): la peça més elegant.
   Tota coloració bona de [1,N] amb χ(1)=0 ha de ser 2d-periòdica a la finestra
   [1, a+d+1] (escala de ±2d), invertida al bloc superior, i **antipodal**
   (φ(ρ+d) = 1−φ(ρ)); tres famílies de ternes explícites forcen que φ sigui
   **s-antiperiòdica** (s = r−d); i antipodal + s-antiperiòdic és impossible
   exactament quan v₂(s) ≠ v₂(d) — **que és exactament la condició d'existència
   del nombre de Rado**. L'aritmètica 2-àdica del problema tanca ella mateixa
   l'última porta.

A més, `draft_UB-d2.md` dona una demostració independent del cas d=2 (ambdós
règims), que corrobora les peces 2 i 3 on se solapen.

**Rastre de verificació** (cada peça, 2 revisors independents amb
comprovacions computacionals pròpies, més lectura línia a línia nostra):
- Cota inferior: correcte per duplicat. Règim r ≤ d: correcte per duplicat.
- Règim r > d: correcte per duplicat (replay exhaustiu de les 2¹³ coloracions del
  cas mínim, 313.950 tuples 2-àdiques, tests de mutació, control negatiu de
  no-vacuïtat). Totes les observacions restants són de redacció (documentades
  a `demostracio/les notes de revisió (aplicades)`).
- Les comprovacions finites que usen les demostracions es reprodueixen amb
  `demostracio/verify_proofs.py` (committejat, independent).

Observacions:
- Per a a < 2d es redueix a Rad₂ = (a+3)(a−c) + c + 1 (règim de c petit).
- El cas a = 2d (c = d) mai satisfà la condició d'existència.
- La periodicitat en a és 2d = 2(a−c), amb sostre d−1: un patró que no
  s'assembla a cap de les fórmules del paper original.

**Evidència**: 610 valors exactes, cadascun amb testimoni verificat
independentment i certificat DRAT verificat:
- 310 valors *in-sample* (a ∈ [3,31]) — encaix 310/310;
- **300 valors *out-of-sample* (a ∈ [33,45]) predits abans de calcular-los —
  encaix 300/300**.

**Família extremal explícita** (cota inferior de la conjectura, `family.py`):
amb a = 2dq + r, la coloració de [1, N*] per trams alternats (començant amb 1):
- si r ≤ d: ales de (2q+1) trams de mida d, i **d defectes** — trams de zeros
  allargats a mida d+r — separats per (2q−1) trams de mida d;
- si r > d (s = r−d): ales de (2q+2) trams, i **d+1 defectes** — trams curts
  de mida s — separats per (2q+1) trams de mida d.

La longitud total quadra algebraicament amb N* = Rad₂−1 en ambdós règims, i la
validesa s'ha comprovat mecànicament per a **tots** els (a,d) existents amb
d ≥ 2 i a ≤ 80: **2.016/2.016**. Per a d=1 la mateixa construcció donaria
longitud 2a+2 — exactament la longitud que el Teorema demostra impossible:
l'excepció d=1 de la conjectura és la degeneració coherent de la família.

---

## 3. Confirmació de les conjectures de Dwivedi–Tripathi al grid

Escombrat complet a ∈ [3,15], c ∈ [−100,300] (3.662 parells existents, 0 errors):

- **Conjectura 1** (c ≤ 0 ⇒ Rad₂ = (a+3)(a−c)+1): confirmada en els **234 casos
  oberts** del grid (tots ara valors exactes certificats).
- **Conjectura 2** (c ≥ a(K+2) ⇒ Rad₂ = K+1): confirmada **12/12**.
- Les zones ja provades del paper (1.241 valors) es reprodueixen exactament —
  validació contínua del mètode.
- Zona mitjana a < c < a(K+2): **2.105 valors exactes nous** (658 coincideixen
  amb la cota inferior màxima coneguda; la resta l'excedeixen — estructura
  encara per minar).

**Total: 2.721 nombres de Rado exactes nous**, tots certificats
(2.421 del grid + 300 out-of-sample de la conjectura).

---

## 4. Com verificar-ho tot sense confiar en nosaltres

Cada valor Rad₂(a;c) = N es descompon en dues afirmacions verificables:

1. **Rad₂ > N−1**: `witnesses/a{a}_c{c}.json` conté una coloració explícita de
   [1,N−1]. Verificable amb `python check_witness.py witnesses/a7_c-6.json`
   (30 línies de força bruta, sense SAT) o amb qualsevol programa propi.
2. **Rad₂ ≤ N**: `certificates/rado_a{a}_c{c}_N{N}.cnf` (CNF regenerable
   independentment: 2 clàusules per solució de l'equació) i la prova
   `...drat`, verificable amb el verificador estàndard `drat-trim`:
   `drat-trim rado_a7_c-6_N131.cnf rado_a7_c-6_N131.drat` → `s VERIFIED`.

El Teorema de la secció 1 no depèn de cap càlcul: la demostració és
autocontinguda i llegible a mà.

**Re-verificació total del corpus** (`reverify_all.py`, executada de nou de cap
a cap): 3.889/3.889 testimonis re-validats per força bruta, i 2.663/2.663
certificats verificats amb un pas addicional: cada CNF es **regenera amb un
segon generador independent** (codi diferent) i es compara clàusula a clàusula
abans de re-executar drat-trim — això tanca el forat "prova UNSAT correcta però
de la fórmula equivocada".

---

## 5. Fitxers

| Fitxer | Contingut |
|---|---|
| `rado_core.py` | codificació SAT + cerca del valor exacte |
| `check_witness.py` | comprovador independent (força bruta) |
| `certify.py` | emissió i verificació de proves DRAT |
| `validate_known.py` | porta de validació (42 valors del paper) |
| `sweep.py`, `extend_smallc.py` | escombrats |
| `mine_smallc.py`, `verify_conjecture.py` | mineria i verificació de la conjectura |
| `results/*.jsonl`, `witnesses/`, `certificates/` | dades i certificats |

## 6. Feina futura

- Minar l'estructura de la zona mitjana (2.105 valors, `results/open_mid.csv`).
- Intentar la demostració de la conjectura per a d ≥ 2 (la cota inferior
  hauria de sortir d'una família de coloracions per blocs amb defecte de fase;
  la superior, d'un argument de forçament com el del Teorema).
- Possible contacte amb Dwivedi i Tripathi (el resultat respon el seu
  Open Problem 1 en la franja 0 < c < a i part de les altres).
