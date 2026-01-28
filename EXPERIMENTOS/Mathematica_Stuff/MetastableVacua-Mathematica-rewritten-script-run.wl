changmoduli = ({\[Tau] -> E^-\[Phi] vol^(1/2), \[Rho] -> vol^(1/3)} /. {vol -> (\[Tau] Exp[\[Phi]])^(3/2)});

VH3 = (AH3 Exp[2 \[Phi]])/\[Rho]^6 /. changmoduli /. {\[Phi] -> Log[1/s]}

VO3 = AO3 PowerExpand[(\[Rho]^((q - 6)/2) \[Tau]^-3) /. changmoduli] /. {\[Phi] -> Log[1/s]} /. {q -> 3}

VF5 = AF5 PowerExpand[(\[Rho]^(3 - p) \[Tau]^-4) /. changmoduli] /. {\[Phi] -> Log[1/s]} /. {p -> 5}

VF5 = AF5/\[Tau]^4;

VF3 = (AF3 Exp[4 \[Phi]])/\[Rho]^6 /. changmoduli /. {\[Phi] -> Log[1/s]}

VR6 = AR6 PowerExpand[(\[Rho]^-1 \[Tau]^-2) /. changmoduli];

VD5 = AD5/(Sqrt[s] \[Tau]^(5/2));

Vins = AA Exp[-aa \[Tau]];

(*VD5=AD5/(Sqrt[s^3] \[Tau]^(3/2));*)

Vreal = VH3 + VF3 + VD5 + VF5 + VO3 + 0 Vins

var = {s, \[Tau]};

NM = Length[var];

mij = Simplify[Table[D[Vreal, var[[i]], var[[j]]], {i, 1, NM}, {j, 1, NM}]];

detmij = Det[mij];

trmij = Tr[mij];

diV = Simplify[Table[D[Vreal, var[[i]]], {i, 1, NM}]];

egval = Eigenvalues[Table[D[Vreal, var[[i]], var[[j]]], {i, 1, 2}, {j, 1, 2}]];

pfun = Function[{s, \[Tau]}, 10^4 If[egval[[1]] < 0, egval[[1]], 0] + 10^4 If[egval[[2]] < 0, egval[[2]], 0]];

SetOptions[NMinimize, MaxIterations -> 500, WorkingPrecision -> 40];

max = 100;

data = Table[0, {i, 1, max}];

Do[
 {min, steps} = Reap[
   NMinimize[
    {
     10^4 diV . diV +
     10^4 (Abs[Vreal] - Vreal) +
     10^5 (Abs[detmij - trmij^2/4] + detmij - trmij^2/4) +
     10^5 (Abs[trmij] - trmij),
     s      > RandomInteger[{1, 100}]/100,
     \[Tau] > RandomInteger[{1, 100}]/100
    },
    {s, \[Tau], AF3, AH3, AO3, AF5, AD5},
    Method -> {
      "SimulatedAnnealing",
      "PerturbationScale" -> 0.5, 
      "LevelIterations" -> 50,
      "RandomSeed" -> 0, 
      "PostProcess" -> {
        FindMinimum,
        Method -> "ConjugateGradient",
        MaxIterations -> 500,
        PrecisionGoal -> 10^2,
        WorkingPrecision -> 500
      }
    },
    StepMonitor :> Sow[{s, \[Tau], AF3, AH3, AO3, AA, aa}]
   ]
 ];

 ll = Length[steps[[1]]];

 pp = Table[{steps[[1]][[i]][[1]], steps[[1]][[i]][[2]]}, {i, 1, ll}];

 If[Mod[taur, 10] == 0,
  Print["_______________________________________________________ taur \ = ", taur];
  Print["min = ", N[min, 10]];
  Print["diV = ", N[Simplify[Table[D[Vreal, var[[i]]], {i, 1, NM}]] /. min[[2]], 10]];
  Print["\!\(\*SuperscriptBox[\(m\), \(2\)]\) = ", N[egval /. min[[2]], 10]];
 ];

 data[[taur]] = Flatten[N[{min[[1]], min[[2]], egval /. min[[2]]}, 10]]; , {taur, 1, max}
]
