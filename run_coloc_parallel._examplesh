#!/bin/bash


# Check if arguments were provided
if [ $# -ne 2 ]; then
    echo "Error: Wrong number of arguments supplied."
    echo "Usage: $0 gwas_dir eqtl_dir"
    echo "Example: $0 /mnt/project/harmonized_genuity_results /mnt/project/publically_available_supporting_files/rosmap_brain"
    exit 1
fi

# Input directories from command line arguments
GWAS_INPUT_DIR=$1
EQTL_INPUT_DIR=$2
RESULTS_DIR="/opt/notebooks/coloc_results"

# Create results and log directories
mkdir -p $RESULTS_DIR

# Log input parameters
echo "=== Analysis Parameters ==="
echo "GWAS Directory: $GWAS_INPUT_DIR"
echo "eQTL Directory: $EQTL_INPUT_DIR"
echo "Results Directory: $RESULTS_DIR"
echo "=========================="

# Loop through each GWAS file
for gwas_file in $GWAS_INPUT_DIR/*.regenie.tsv.gz; do
    gwas_name_prefix=$(basename "$gwas_file" .regenie.tsv.gz)
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Processing GWAS file: $gwas_name_prefix"

    # Loop through each eQTL file
    for eqtl_file in $EQTL_INPUT_DIR/*.all.tsv.gz; do
        eqtl_name_prefix=$(basename "$eqtl_file" .all.tsv.gz)
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Processing eQTL file: $eqtl_name_prefix"

        if [ -f "$eqtl_file" ]; then
            # Create output directory with timestamp
            output_dir="project-Gv45qjQ09Vk2p6X7q5xJ42PV:/analysis_KJ/coloc_gwas_eqtls/results/${gwas_name_prefix}_${CURRENT_USER}_$(date +%Y%m%d)"
            
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Submitting job for $gwas_name_prefix vs $eqtl_name_prefix"

             # Remove "/mnt/project/" from the path
             gwas_cleaned_path=${gwas_file#/mnt/project/}
             eqtl_cleaned_path=${eqtl_file#/mnt/project/}

            # Submit swiss-army-knife job
            dx run swiss-army-knife \
                -iin="project-Gv45qjQ09Vk2p6X7q5xJ42PV:/${gwas_cleaned_path}" \
                -iin="project-Gv45qjQ09Vk2p6X7q5xJ42PV:/${eqtl_cleaned_path}" \
                -iin="project-Gv45qjQ09Vk2p6X7q5xJ42PV:/publically_available_supporting_files/onek1k/oneK1K_samplesize.csv" \
                -iimage_file="project-Gv45qjQ09Vk2p6X7q5xJ42PV:/analysis_KJ/coloc_gwas_eqtls/code/coloc-analysis.tar" \
                -icmd="Rscript /opt/notebooks/codes/run_coloc_gene_base.r ${gwas_name_prefix}.regenie.tsv.gz ${eqtl_name_prefix}.all.tsv.gz oneK1K_samplesize.csv ${RESULTS_DIR}" \
                --instance-type "mem3_ssd2_v2_x8" \
                --destination="${output_dir}" \
                --brief \
                --yes

            # Check for results and upload
#            if ls "${RESULTS_DIR}"/*.txt 1> /dev/null 2>&1; then
#                echo "[$(date '+%Y-%m-%d %H:%M:%S')] Uploading results to ${output_dir}"
#                dx upload "${RESULTS_DIR}"/*.txt --destination "${output_dir}/"
#                rm "${RESULTS_DIR}"/*.txt
#            else
#                echo "[$(date '+%Y-%m-%d %H:%M:%S')] No results found for $gwas_name_prefix vs $eqtl_name_prefix"
#            fi
        else
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: File '$eqtl_file' does not exist or is non-readable."
        fi
    done
done

# Upload log file
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Uploading log file..."
#dx upload "$LOG_FILE" --destination "project-Gv45qjQ09Vk2p6X7q5xJ42PV:/analysis_KJ/coloc_gwas_eqtls/logs/"

echo "All coloc analyses completed."
