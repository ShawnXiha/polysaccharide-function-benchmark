$ErrorActionPreference = 'Stop'

function Write-Utf8NoBom {
    param(
        [string]$Path,
        [string]$Text
    )
    $full = Join-Path (Get-Location) $Path
    [System.IO.File]::WriteAllText($full, $Text, [System.Text.UTF8Encoding]::new($false))
}

$supp = Get-Content 'paper/supplementary_v1.tex' -Raw
$supp = $supp.Replace('$\\rightarrow$', '$\rightarrow$')
Write-Utf8NoBom 'paper/supplementary_v1.tex' $supp
Write-Utf8NoBom 'submission_packages/bmc_bioinformatics/supplementary_bmc_bioinformatics.tex' ($supp.Replace('Author names withheld for draft preparation', 'First Author, Second Author, Corresponding Author'))
Write-Utf8NoBom 'submission_packages/database/supplementary_database.tex' ($supp.Replace('Author names withheld for draft preparation', 'First Author, Second Author, Corresponding Author'))

$main = Get-Content 'paper/manuscript_v1.tex' -Raw

$authorBlock = @'
\author{First Author$^{1}$, Second Author$^{2}$, Corresponding Author$^{1,*}$\\
\small $^{1}$Affiliation 1, City, Country\\
\small $^{2}$Affiliation 2, City, Country\\
\small $^{*}$Correspondence: corresponding.author@email.example}
'@

$bmc = $main
$bmc = $bmc.Replace('\usepackage{tabularx}', "\usepackage{tabularx}`r`n\usepackage{setspace}`r`n\usepackage[left]{lineno}")
$bmc = $bmc.Replace('\author{Author names withheld for draft preparation}', $authorBlock)
$bmc = $bmc.Replace("\begin{document}`r`n\maketitle", "\begin{document}`r`n\doublespacing`r`n\linenumbers`r`n\maketitle")
$bmc = $bmc.Replace('\end{abstract}', "\end{abstract}`r`n`r`n\noindent\textbf{Keywords:} polysaccharide knowledge graph; function retrieval; DoLPHiN; meta-path baseline; ontology propagation; long-tail prediction")
$bmc = $bmc.Replace('\includegraphics[width=0.96\textwidth]{figures/', '\includegraphics[width=0.96\textwidth]{../../paper/figures/')
$bmc = $bmc.Replace('\section{Code and Artifact Availability}', '\section{Availability of data and materials}')
$bmc = $bmc.Replace(
    'The submission package is accompanied by a reproducibility bundle that includes the normalized KG export, the benchmark split definitions, the task-specific parent/child function hierarchy, the edge-level paired stability records, the case-study candidate tables, and the scripts used for graph construction, PyG export, retrieval, shallow baselines, GNN ablations, and figure generation. In the working repository these artifacts are organized under the graph-building modules, experiment directories, and paper-generation scripts; they will be released together with the public code archive and supplementary package at submission time. This release design is intended to make the paper reproducible as a benchmark resource rather than only interpretable as a prose description.',
    'The normalized KG export, benchmark split definitions, task-specific parent/child function hierarchy, paired edge-level stability records, the standalone supplementary PDF, and the benchmark scripts for graph construction, retrieval, shallow baselines, GNN ablations, and figure generation will be released through the public repository and supplementary package at submission time. Please insert the final archive URL here: \texttt{[INSERT-PUBLIC-REPOSITORY-URL]}. This release design is intended to make the paper reproducible as a benchmark resource rather than only interpretable as a prose description.'
)
$bmc = $bmc.Replace('\bibliography{references_placeholder}', '\bibliography{references}')
$bmc = $bmc.Replace('\section{Introduction}', "\section*{List of abbreviations}`r`nKG: knowledge graph; GNN: graph neural network; MRR: mean reciprocal rank; DOI: digital object identifier.`r`n`r`n\section{Introduction}")
$bmc = $bmc.Replace('\section{Conclusion}', "\section{Supplementary Materials}`r`nSupplementary Table S1 summarizes the biology-facing case-study evidence, and Supplementary Table S2 clarifies the interpretation of exact match in the GNN failure ablation. These materials are distributed as a separate supplementary PDF together with the submission package.`r`n`r`n\section{Conclusion}")
$bmc = $bmc.Replace(
    "\bibliographystyle{plain}`r`n\bibliography{references}",
    "\bibliographystyle{plain}`r`n\bibliography{references}`r`n`r`n\section*{Declarations}`r`n\textbf{Ethics approval and consent to participate} Not applicable.`r`n`r`n\textbf{Consent for publication} Not applicable.`r`n`r`n\textbf{Availability of data and materials} The normalized KG export, benchmark split definitions, task-specific parent/child function hierarchy, paired edge-level stability records, and supplementary benchmark tables will be released at: \texttt{[INSERT-PUBLIC-REPOSITORY-URL]}.`r`n`r`n\textbf{Competing interests} The authors declare that they have no competing interests.`r`n`r`n\textbf{Funding} Insert funding information here.`r`n`r`n\textbf{Authors' contributions} Insert author contribution statement here.`r`n`r`n\textbf{Acknowledgements} Insert acknowledgements here."
)
Write-Utf8NoBom 'submission_packages/bmc_bioinformatics/paper_bmc_bioinformatics.tex' $bmc

$db = $main
$db = $db.Replace('\author{Author names withheld for draft preparation}', $authorBlock)
$db = $db.Replace('\end{abstract}', "\end{abstract}`r`n`r`n\noindent\textbf{Database URL:} \texttt{[INSERT-DATABASE-URL]}. The public landing page should provide open access to the DoLPHiN-derived knowledge graph, benchmark data, and documentation.")
$db = $db.Replace('\section{Methods}', '\section{Materials and Methods}')
$db = $db.Replace('\section{Experiments}', '\section{Results}')
$db = $db.Replace('\section{Related Work}', '\subsection{Related context}')
$db = $db.Replace('\section{Limitations}', '\subsection{Limitations}')
$db = $db.Replace('\includegraphics[width=0.96\textwidth]{figures/', '\includegraphics[width=0.96\textwidth]{../../paper/figures/')
$db = $db.Replace('\section{Code and Artifact Availability}', '\section{Supplementary Data}')
$db = $db.Replace(
    'The submission package is accompanied by a reproducibility bundle that includes the normalized KG export, the benchmark split definitions, the task-specific parent/child function hierarchy, the edge-level paired stability records, the case-study candidate tables, and the scripts used for graph construction, PyG export, retrieval, shallow baselines, GNN ablations, and figure generation. In the working repository these artifacts are organized under the graph-building modules, experiment directories, and paper-generation scripts; they will be released together with the public code archive and supplementary package at submission time. This release design is intended to make the paper reproducible as a benchmark resource rather than only interpretable as a prose description.',
    'Supplementary Data include the normalized KG export, benchmark split definitions, the task-specific parent/child function hierarchy, paired edge-level stability records, the standalone supplementary PDF, case-study candidate tables, and the scripts used for graph construction, PyG export, retrieval, shallow baselines, GNN ablations, and figure generation. These assets will be released together with the public repository and database landing page at submission time.'
)
$db = $db.Replace('\bibliographystyle{plain}', '\bibliographystyle{unsrt}')
$db = $db.Replace('\bibliography{references_placeholder}', '\bibliography{references}')
$db = $db.Replace('\section{Conclusion}', "\section{Funding}`r`nInsert funding information here.`r`n`r`n\section{Acknowledgements}`r`nInsert acknowledgements here.`r`n`r`n\section{Conclusion}")
Write-Utf8NoBom 'submission_packages/database/paper_database.tex' $db

$bmcManifest = @'
# BMC Additional Files Manifest

Recommended upload set in addition to the main manuscript:

- Additional file 1: supplementary PDF (`supplementary_bmc_bioinformatics.pdf`)
  - Title: Supplementary tables for case-study evidence and GNN ablation interpretation
  - Description: Supplementary Table S1 summarizes biology-facing case-study evidence; Supplementary Table S2 clarifies why exact match is not the primary metric for the GNN failure ablation.

- Additional file 2: ontology stability summary (`.json` or `.csv`)
  - Title: Paired stability outputs for ontology variant
  - Description: Aggregated paired-seed significance results and edge-level paired evaluation summaries.

- Additional file 3: extended experiment tables (`.xlsx` or `.csv`)
  - Title: Extended benchmark and ablation results
  - Description: Seed-wise and auxiliary baseline tables not shown in the main text.

- Additional file 4: repository snapshot / schema docs (`.pdf` or `.txt`)
  - Title: KG schema and benchmark artifact map
  - Description: Node/edge schema, export layout, split definitions, and benchmark artifact organization.

Before upload, ensure each additional file is cited in sequence in the manuscript text as `Additional file N`.
'@
Write-Utf8NoBom 'submission_packages/bmc_bioinformatics/additional_files_manifest.md' $bmcManifest

$dbManifest = @'
# Database Additional Files Manifest

Recommended supplementary uploads:

- Supplementary Data 1: supplementary PDF (`supplementary_database.pdf`)
  - Contains Supplementary Table S1 on biology-facing case-study evidence and Supplementary Table S2 on GNN ablation interpretation.
- Supplementary Data 2: ontology stability outputs (`.csv` or `.json`)
- Supplementary Data 3: extended benchmark tables (`.xlsx` or `.csv`)
- Supplementary Data 4: KG schema and export documentation (`.pdf` or `.txt`)
- Supplementary Data 5: processed benchmark metadata and split definitions (`.csv` / `.json`)

For Database submission, supplementary files should be uploaded separately and referenced from the `Supplementary Data` section.
'@
Write-Utf8NoBom 'submission_packages/database/additional_files_manifest.md' $dbManifest
