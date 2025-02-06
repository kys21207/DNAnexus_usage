import gwaslab as gl
import argparse
import os
import re
import multiprocessing

parser = argparse.ArgumentParser(
                    prog='gather_sumstats_and_plot.py',
                    description='Combine split chromosomes from regenie',
                    epilog='Pass the GWAS file, outdir of the phenotype')

parser.add_argument('--gwas_file')
parser.add_argument('--plot_outdir', nargs='?')
parser.add_argument('--gwas_formatted_outdir')
parser.add_argument('--sumstats_in_format')
parser.add_argument('--out_name')
parser.add_argument('--mondo_id', nargs='?')
parser.add_argument('--build')

args = parser.parse_args()
out_name = args.out_name
gwas_outpath = os.path.dirname(args.gwas_formatted_outdir) + "/"
numb_cores  = multiprocessing.cpu_count() - 2

# Read in the summary statistics
mysumstats = gl.Sumstats(sumstats = args.gwas_file,fmt = args.sumstats_in_format, build= args.build)

# Perform some quality checks, including the removal of indels
mysumstats.basic_check(remove = True)
mysumstats.fix_chr(remove = True)
mysumstats.filter_snp(inplace = True)
mysumstats.fill_data(to_fill=["P"], extreme=True)
mysumstats.fill_data(to_fill=["MLOG10P"], extreme=True)

# If not present, download the correct rsids set for adding RSIDSs
gl.download_ref("1kg_dbsnp151_hg" + args.build + "_auto")
mysumstats.assign_rsid(ref_rsid_tsv ="/home/dnanexus/.gwaslab/1kg_dbsnp151_hg" + str(args.build) + "_auto.txt.gz", n_cores = numb_cores)

# Export the cleaned phenotypes with rsids
mysumstats.to_format(gwas_outpath + out_name, fmt = args.sumstats_in_format, cols = ["rsID"])

# Ignore the distance based clumping for now.
# mysumstats_lead = mysumstats.get_lead(build = "38",sig_level = 1e-5,gls = True,anno = True,windowsizekb = 250)
# mysumstats_lead.to_format(gwas_outpath +  out_name + "_lead_variants", cols = ["P", "LOCATION", "GENE"], fmt = "gwaslab")

# Mondo id will not work on genuity due to firewall issues, but can be used on dnanexus
if args.mondo_id:
    mysumstats_lead.get_novel(
        efo = args.mondo_id,
        sig_level = 1e-5
    ).to_csv(
        gwas_outpath + out_name + "_replicated_variants.tsv",
        index = False,
        sep = "\t"
    )

# If you want manhattan and qq plots, then add that flag in script submission
if args.plot_outdir:
    plot_outpath = os.path.dirname(args.plot_outdir) + "/"
    # Plot with MLOG
    mysumstats.plot_mqq(save = plot_outpath + out_name + "_plot.png", save_args={"dpi":400,"facecolor":"white"},skip = 1,scaled = True,sig_level = 5e-6,cut = 15,build = "38",stratified = True,suggestive_sig_level = 5e-8, suggestive_sig_line = True,suggestive_sig_line_color = "red", anno = "GENENAME")
  
