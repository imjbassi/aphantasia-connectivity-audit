# OSF Secondary Data Preregistration — paste-ready draft

Project: Reduced frontoparietal–visual connectivity in aphantasia
Author: Jaiveer Bassi (independent researcher), jaiveerbassi@yahoo.com, ORCID 0009-0006-3633-3220
Template: OSF "Secondary Data Preregistration"

## Before you submit — outstanding decisions

These are the items marked [DECIDE] / [CONFIRM] in the working draft. The registration should not
be submitted until each is settled, because a preregistration that leaves a choice open gives the
choice back to the analyst.

1. **Primary hypothesis.** H1 (frontoparietal to early visual) or H2 (fusiform node to anterior
   prefrontal)? The manuscript audits the first, so H1 keeps the paper and the test aligned.
2. **Data access timing.** Confirm that no raw data have been seen or requested-and-received at
   the moment of submission. If data arrive first, use the "registration after data access"
   option and state what was looked at.
3. **Blinding.** Name the second person who will recode group labels, or arrange for the Bonn
   team to send labels withheld.
4. **Coordinates.** Spagna et al. (2021) fusiform peak, and the four prefrontal peaks from Milton
   et al. (2021), need the exact MNI values pasted into the ROI table.
5. **Software versions.** Pin the fMRIPrep version on the day of registration.

---

## 1. Title

Is resting-state connectivity between frontoparietal and visual cortex reduced in aphantasia?
A pre-registered reanalysis of Monzel et al. (2024).

## 2. Description

Reviews and theory papers describe aphantasia as a disconnection between frontoparietal control
regions and visual cortex. The published evidence for a difference from typical imagers is
task-based: a psychophysiological interaction from a fusiform seed in ten participants per group
(Liu et al., 2025), and parietal-to-early-visual coupling during working memory in seventeen per
group, with historical controls scanned on a different scanner (Wu & Yu, 2026). Comparisons made
at rest have not shown the reduction. Milton et al. (2021) found no region in which mid-range
controls were more strongly connected than aphantasic participants; Liu et al. (2025) found no
group difference in task-residual connectivity; Monzel et al. (2024) found no resting
hippocampal–visual difference and did not test frontal or parietal regions. No resting-state study
has run a pre-specified test of frontoparietal–visual connectivity in aphantasia against typical
imagers. This registration specifies that test.

## 3. Hypotheses

All directional: aphantasia lower than controls.

- **H1 (primary).** Mean resting-state functional connectivity between frontoparietal regions and
  early visual cortex (V1–V3) is lower in aphantasic participants than in controls.
- **H2 (secondary).** Connectivity between the left fusiform imagery node and left anterior
  prefrontal cortex is lower in aphantasic participants. This is Liu et al.'s (2025) task finding,
  tested at rest.
- **H3 (secondary).** Connectivity between the visual-occipital network and the prefrontal regions
  reported by Milton et al. (2021) (BA 9, 10, 11) is lower in aphantasic participants. Milton
  et al. reported this for hyperphantasic against aphantasic participants only.

## 4. Data

**Source.** Monzel et al. (2024), eLife 13:RP94916. Raw data requested from the senior author under
the paper's data statement, which offers them to scientific collaborators for non-commercial
research.

**Sample.** 14 aphantasic and 16 control participants after the original authors excluded one
aphantasic participant for technical problems. Both groups came from the Aphantasia Research
Project Bonn database and were matched on age, sex, education and IQ. The paper states no VVIQ
inclusion rule. Group means were 16.57 and 62.94.

**Acquisition, as published.** 3T Siemens Skyra, 32-channel head coil. Resting state: eyes closed,
3.5 mm isotropic EPI, TR 2 s, TE 30 ms, 190 volumes, acquired before the memory task. 0.8 mm
MEMPRAGE T1 and a two-echo gradient-echo fieldmap.

**Prior knowledge of the data.** I have read the published paper and its eLife reviews. I know that
there was no resting-state group difference between right hippocampus and visual cortex, that there
was a task-based group difference in hippocampal–visual coupling, and that resting
hippocampal–visual connectivity correlated with visualisation scores. I have not seen the raw
images, and I have not seen or computed any frontal, parietal or fusiform connectivity value from
this dataset. The public Dryad file holds extracted hippocampal–visual values only, and I have not
opened it.

**Regions of interest.** All come from atlases or other studies, never from this dataset.

| Set | Definition | Source |
|---|---|---|
| Early visual cortex (H1) | Bilateral V1, V2, V3 (dorsal and ventral), maximum-probability map | Wang et al. (2015) probabilistic atlas |
| Frontoparietal (H1) | Parcels in the Control A/B and Dorsal Attention A/B networks | Schaefer-400 with Yeo 17-network labels |
| Fusiform imagery node (H2) | 6 mm sphere at the left fusiform peak | Spagna et al. (2021) meta-analysis [coordinates] |
| Left anterior PFC (H2) | 6 mm sphere at MNI −23, 54, 8 | Liu et al. (2025), Table S10 |
| Visual-occipital network (H3) | Visual Central and Visual Peripheral networks | Schaefer-400 with Yeo 17-network labels |
| Prefrontal targets (H3) | 6 mm spheres at the four prefrontal peaks | Milton et al. (2021) resting-state table [coordinates] |
| Negative control | Bilateral primary auditory cortex (Te1.0) | Jülich atlas |

Any frontoparietal parcel that overlaps the Wang visual field maps (V1–V3A/B, hV4) by more than
10% of its voxels is dropped from the frontoparietal set.

**Outcome measures.** Pearson correlations between mean ROI time series, Fisher z-transformed.

- H1: the mean z across all frontoparietal × early-visual ROI pairs, one number per participant.
- H2: z for the single pair.
- H3: the mean z between the visual network time series and the four prefrontal spheres.
- Negative control: the mean z between early visual cortex and primary auditory cortex; no group
  difference predicted.

**Covariates.** Age, sex, mean framewise displacement.

## 5. Analysis plan

**Preprocessing.** Conversion to BIDS with dcm2niix and HeuDiConv, checked with the BIDS validator.
fMRIPrep [version pinned at registration] with fieldmap distortion correction, output in
MNI152NLin2009cAsym at 2 mm. Denoising in nilearn with 24 motion parameters, the first five
anatomical CompCor components each from white matter and CSF, a cosine high-pass filter at
0.008 Hz, and removal of non-steady-state volumes flagged by fMRIPrep. Censoring at framewise
displacement above 0.5 mm. No smoothing and no global signal regression in the primary analysis.
Visual check of every fMRIPrep report before unblinding.

**Exclusions.** Mean framewise displacement above 0.3 mm; fewer than 120 volumes after censoring;
failed registration or distortion correction; early visual coverage below 80% of ROI voxels. All
decided blind to group; no imputation. If fewer than 12 remain in either group, everything is
reported as descriptive only.

**Blinding.** Group labels recoded to A and B by a second person before data transfer;
preprocessing, quality control and exclusions completed and analysis code frozen at a commit hash
before unblinding.

**Model.** Ordinary least squares for each outcome: z ~ group + age + sex + mean FD.

**Primary test.** One-sided t-test on the group coefficient at α = .05, reported alongside the
two-sided p, Hedges' g with a 95% CI, and a one-sided JZS Bayes factor with Cauchy scale 0.707.

**Secondary tests.** H2 and H3 with the same model, Holm-corrected across the two.

**Inference rules.**

| Outcome | Conclusion |
|---|---|
| One-sided p < .05 and BF > 3 | Supports reduced resting connectivity |
| One-sided p < .05 but BF ≤ 3 | Weak support, reported as such |
| p ≥ .05 | Inconclusive; never reported as evidence of absence |
| Negative control differs (two-sided p < .05) | Any H1 effect is treated as non-specific |

**Robustness checks, reported whatever the result.** Welch test without covariates; permutation
test with 10,000 label shuffles; with global signal regression; censoring at 0.2 mm; frontoparietal
set split into Control and Dorsal Attention networks.

**Exploratory, labelled as such.** Seed-to-voxel maps from early visual cortex with threshold-free
cluster enhancement and family-wise error p < .05; correlation of the H1 measure with VVIQ within
the control group.

**Power.** At 14 versus 16, the smallest detectable effect at 80% power (one-sided) is d = 0.93;
power at d = 0.5, 0.8 and 1.0 is .38, .69 and .85; the Bayes factor for the null at an observed
difference of exactly zero is 2.9; the narrowest testable equivalence bounds are ±1.10.

**Pooled analysis, only if the Exeter data are shared.** The same pipeline is applied and the sites
pooled: z ~ group + site + age + sex + FD, with a group × site interaction check. At roughly 35 per
group the smallest detectable effect falls to d = 0.60 (one-sided) and a true null yields a Bayes
factor of about 4. Registered as an amendment before the Exeter data are accessed.

## 6. Other

**Limitations, stated in advance.** Eyes-closed rest allows drowsiness, which changes visual-cortex
connectivity. Group assignment relies on self-report. The sample was recruited through one
aphantasia research database.

**Deviations.** Any departure from this plan is reported in a deviations table with its reason,
together with the result under the original plan where that can still be computed.

**Sharing.** Code is public at registration. Derived ROI time series and connectivity values are
shared if the data-use agreement allows.
