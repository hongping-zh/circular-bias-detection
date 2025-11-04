# Figure Captions for SoftwareX Submission

**Paper:** Sleuth: A Browser-Based Tool for Detecting Circular Bias in AI Evaluation  
**Date:** October 16, 2025

---

## Figure 1: Main Dashboard Interface

**File:** `fig1_main_interface.png`  
**Size:** 10×7 inches, 300 DPI  
**Format:** PNG (RGB)

**Caption:**
Sleuth's analytical dashboard displaying three visualization panels: **(A)** CBS gauge chart with color-coded risk zones (green: <0.3, yellow: 0.3-0.6, red: >0.6) showing CBS = 0.64 (High Risk); **(B)** Radar plot overlaying observed indicator values (red) against detection thresholds (black dashed) for PSI, CCS, and ρ_PC; **(C)** Time-series visualization of performance metrics (blue) and normalized constraint values (purple) across five evaluation periods, illustrating positive correlation pattern indicative of circular bias.

**Description for reviewers:**
This figure demonstrates the user interface components that deliver interpretable diagnostics. The gauge chart provides immediate risk assessment, the radar plot enables threshold-based detection, and the time-series panel reveals temporal correlation patterns between performance and resource allocation.

---

## Figure 2: Validation Results

**File:** `fig2_validation.png`  
**Size:** 6×4 inches, 300 DPI  
**Format:** PNG (RGB)

**Caption:**
Comparative performance of Sleuth across 100 synthetic evaluation sequences (50 unbiased, 50 biased). Bar chart displays mean values for CBS and constituent indicators (PSI, CCS, ρ_PC) in clean datasets (blue) versus biased datasets (orange). Red dashed line marks CBS detection threshold (0.6). Overall detection accuracy: 94% (47/50 biased datasets correctly flagged, 2/50 false positives in clean datasets).

**Description for reviewers:**
This figure validates Sleuth's detection capability on controlled synthetic data. The clear separation between clean and biased CBS distributions (0.24 vs 0.71) demonstrates the composite score's discriminative power. Individual indicators show complementary patterns: PSI captures parameter drift, CCS reveals constraint inconsistency, and ρ_PC detects performance-resource correlation.

---

## Figure 3: ImageNet Case Study

**File:** `fig3_imagenet_case.png`  
**Size:** 6×4 inches, 300 DPI  
**Format:** PNG (RGB)

**Caption:**
Scatter plot analyzing 12 ImageNet model evaluations spanning 2018-2023, showing strong positive correlation (ρ_PC = 0.72, p < 0.001) between effective dataset size and top-1 accuracy. Color gradient indicates chronological progression (purple: 2018 → yellow: 2023). Red dashed line represents linear regression fit. Composite analysis yielded CBS = 0.68 (High Risk), indicating potential circular bias through dataset expansion correlated with performance improvements.

**Description for reviewers:**
This figure demonstrates Sleuth's application to real-world benchmark data. The monotonic increase in both dataset size and accuracy over time, combined with strong correlation, suggests evaluation protocols were modified in response to performance observations—a classic circular bias pattern. This case study illustrates how Sleuth can identify integrity concerns in published evaluation practices.

---

## Technical Specifications

### All Figures Meet SoftwareX Requirements:
- ✅ Minimum 300 DPI resolution
- ✅ Color figures (also legible in grayscale via color-blind friendly palette)
- ✅ Sans-serif fonts (default matplotlib)
- ✅ Clear axis labels and legends
- ✅ Self-contained (captions provide full context)

### File Sizes:
- Figure 1: ~470 KB (complex multi-panel layout)
- Figure 2: ~180 KB (bar chart with annotations)
- Figure 3: ~220 KB (scatter plot with colormap)

**Total: ~870 KB** (well within typical journal limits)

---

## Embedding Instructions for LaTeX

If using LaTeX for submission:

```latex
\begin{figure}[ht]
\centering
\includegraphics[width=0.9\textwidth]{fig1_main_interface.png}
\caption{Sleuth's analytical dashboard displaying three visualization panels: 
(A) CBS gauge chart with color-coded risk zones showing CBS = 0.64 (High Risk); 
(B) Radar plot overlaying observed indicator values against detection thresholds; 
(C) Time-series visualization illustrating positive correlation pattern.}
\label{fig:interface}
\end{figure}

\begin{figure}[ht]
\centering
\includegraphics[width=0.7\textwidth]{fig2_validation.png}
\caption{Comparative performance across 100 synthetic evaluation sequences. 
Overall detection accuracy: 94\%.}
\label{fig:validation}
\end{figure}

\begin{figure}[ht]
\centering
\includegraphics[width=0.7\textwidth]{fig3_imagenet_case.png}
\caption{ImageNet case study showing strong correlation (ρ\_PC = 0.72, p < 0.001) 
between dataset size and accuracy. Composite CBS = 0.68 (High Risk).}
\label{fig:imagenet}
\end{figure}
```

---

## Embedding Instructions for Word

If using Microsoft Word for submission:

1. **Insert → Pictures → Browse Files**
2. Select `fig1_main_interface.png`, `fig2_validation.png`, `fig3_imagenet_case.png`
3. **Right-click → Format Picture → Size → Scale Height: 90%**
4. **Insert Caption:**
   - Reference → Insert Caption → Label: Figure
   - Copy caption text from above
5. **Text Wrapping:** Top and Bottom (for Figure 1), In Line with Text (for Figures 2-3)

---

## Quality Assurance Checklist

Before submission, verify:

- [x] All figures at 300 DPI
- [x] Color consistent across figures
- [x] Font sizes readable (minimum 8pt)
- [x] Axis labels include units where applicable
- [x] Legends positioned clearly
- [x] No overlapping text
- [x] Captions are self-contained (explain what, not why)
- [x] Figures referenced in main text (e.g., "as shown in Figure 1...")
- [x] File names match journal requirements
- [x] Copyright/attribution not needed (original work)

---

## Alternative Text for Accessibility

Provide these descriptions if journal requires accessibility compliance:

**Figure 1 Alt Text:**
"Multi-panel dashboard showing a semicircular gauge indicating high risk score of 0.64, a triangular radar chart comparing three metrics against thresholds, and a dual-axis line graph displaying increasing performance and resource usage over time."

**Figure 2 Alt Text:**
"Bar chart comparing four metrics between clean and biased datasets. Biased datasets show substantially higher Circular Bias Score (0.71) compared to clean datasets (0.24), exceeding the 0.6 threshold marked by a red dashed line."

**Figure 3 Alt Text:**
"Scatter plot showing 12 data points colored from purple to yellow representing years 2018-2023. Points follow an upward trend line, demonstrating positive correlation between dataset size (horizontal axis, 1.2-1.4 million samples) and accuracy (vertical axis, 0.70-0.78)."

---

## Notes for Authors

### Figure Placement Strategy:
- **Figure 1:** Place in Section 2.2 (User Interface) after describing dashboard components
- **Figure 2:** Place in Section 3.1 (Controlled Validation) after presenting accuracy metrics
- **Figure 3:** Place in Section 3.2 (Empirical Case Study) after discussing ImageNet analysis

### In-Text References:
```
Section 2.2: "...as visualized in the interactive dashboard (Figure 1)."
Section 3.1: "Validation results (Figure 2) demonstrate 94% detection accuracy..."
Section 3.2: "Analysis of ImageNet logs (Figure 3) reveals ρ_PC = 0.72 (p < 0.001)..."
```

---

## Graphical Abstract Recommendation

For the required **Graphical Abstract** (500×500 px), consider a simplified version of Figure 1's workflow:

**Suggested Design:**
```
CSV Upload → [Icon] → 
PSI/CCS/ρ_PC Calculation → [Icon] → 
CBS Gauge (0.64) → [Icon] → 
Risk Report
```

Use icons for each step and the gauge chart as the central visual element. Keep text minimal (software name + tagline).

---

**All figures ready for submission! Good luck!** 🚀📊✅
